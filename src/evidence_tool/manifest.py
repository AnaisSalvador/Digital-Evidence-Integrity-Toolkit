
import json
import re
from pathlib import Path
from typing import Iterable

from evidence_tool.hasher import calculate_sha256


def _validate_manifest(manifest: dict) -> None:

    if not isinstance(manifest, dict):
        raise ValueError("Manifest must contain a JSON object")

    if (
        type(manifest.get("schema_version")) is not int
        or manifest["schema_version"] != 1
        or manifest.get("algorithm") != "SHA-256"
        or not isinstance(manifest.get("files"), list)
    ):
        raise ValueError("Invalid manifest structure")

    for record in manifest["files"]:
        if not isinstance(record, dict):
            raise ValueError("Each file record must be a JSON object")

        path = record.get("path")
        size = record.get("size_bytes")
        sha256 = record.get("sha256")

        if not isinstance(path, str) or not path.strip():
            raise ValueError("Each file record must have a valid path")

        if (
            type(size) is not int
            or size < 0
        ):
            raise ValueError("File size must be a non-negative integer")

        if (
            not isinstance(sha256, str)
            or re.fullmatch(r"[0-9a-fA-F]{64}", sha256) is None
        ):
            raise ValueError("Each file record must have a valid SHA-256 hash")


def create_manifest(
    file_paths: Iterable[str | Path],
    base_dir: str | Path,
) -> dict:

    base = Path(base_dir).resolve()
    records = []

    for file_path in file_paths:
        path = Path(file_path)

        if not path.is_absolute():
            path = base / path

        path = path.resolve()

        try:
            relative_path = path.relative_to(base)
        except ValueError:
            raise ValueError(
                f"File must be inside the evidence directory: {path}"
            ) from None

        file_hash = calculate_sha256(path)

        records.append({
            "path": relative_path.as_posix(),
            "size_bytes": path.stat().st_size,
            "sha256": file_hash,
        })

    manifest = {
        "schema_version": 1,
        "algorithm": "SHA-256",
        "files": records,
    }

    _validate_manifest(manifest)
    return manifest


def save_manifest(manifest: dict, output_path: str | Path) -> None:

    _validate_manifest(manifest)

    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)

    with destination.open("w", encoding="utf-8") as file:
        json.dump(manifest, file, indent=2)
        file.write("\n")


def load_manifest(manifest_path: str | Path) -> dict:

    path = Path(manifest_path)

    with path.open("r", encoding="utf-8") as file:
        manifest = json.load(file)
    _validate_manifest(manifest)
    return manifest



def verify_manifest(
    manifest: dict,
    base_dir: str | Path,
) -> list[dict]:
    """Verify files against their recorded SHA-256 hashes."""
    _validate_manifest(manifest)

    base = Path(base_dir).resolve()
    results = []

    for record in manifest["files"]:
        relative_path = Path(record["path"])

        if relative_path.is_absolute():
            raise ValueError("Manifest paths must be relative")

        file_path = (base / relative_path).resolve()

        try:
            file_path.relative_to(base)
        except ValueError:
            raise ValueError(
                f"Manifest path escapes evidence directory: {record['path']}"
            ) from None

        if not file_path.is_file():
            status = "MISSING"
        else:
            current_hash = calculate_sha256(file_path)
            status = (
                "MATCH"
                if current_hash == record["sha256"]
                else "MISMATCH"
            )

        results.append({
            "path": record["path"],
            "status": status,
        })

    return results


