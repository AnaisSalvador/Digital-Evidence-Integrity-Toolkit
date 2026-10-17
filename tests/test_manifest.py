

import json

import pytest

from evidence_tool.manifest import load_manifest, save_manifest

import hashlib

from evidence_tool.manifest import create_manifest


def test_create_manifest(tmp_path):
    evidence_file = tmp_path / "evidence.txt"
    evidence_file.write_bytes(b"hello")

    manifest = create_manifest(
        ["evidence.txt"],
        base_dir=tmp_path,
    )

    assert manifest["schema_version"] == 1
    assert manifest["algorithm"] == "SHA-256"
    assert len(manifest["files"]) == 1

    record = manifest["files"][0]

    assert record["path"] == "evidence.txt"
    assert record["size_bytes"] == 5
    assert record["sha256"] == hashlib.sha256(
        b"hello"
    ).hexdigest()



def test_save_and_load_manifest(tmp_path):
    evidence_file = tmp_path / "evidence.txt"
    evidence_file.write_bytes(b"hello")

    manifest = create_manifest(
        ["evidence.txt"],
        base_dir=tmp_path,
    )

    output_file = tmp_path / "output" / "manifest.json"
    save_manifest(manifest, output_file)

    loaded = load_manifest(output_file)

    assert loaded == manifest
    assert json.loads(output_file.read_text(encoding="utf-8")) == manifest


def test_reject_invalid_manifest_structure(tmp_path):
    manifest_file = tmp_path / "invalid.json"
    manifest_file.write_text(
        '{"schema_version": 99, "algorithm": "SHA-256", "files": []}',
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Invalid manifest structure"):
        load_manifest(manifest_file)


def test_reject_invalid_sha256_hash():
    from evidence_tool.manifest import verify_manifest

    manifest = {
        "schema_version": 1,
        "algorithm": "SHA-256",
        "files": [
            {
                "path": "evidence.txt",
                "size_bytes": 10,
                "sha256": "not-a-valid-hash",
            }
        ],
    }

    with pytest.raises(ValueError, match="valid SHA-256 hash"):
        verify_manifest(manifest, ".")


def test_reject_negative_file_size():
    from evidence_tool.manifest import verify_manifest

    manifest = {
        "schema_version": 1,
        "algorithm": "SHA-256",
        "files": [
            {
                "path": "evidence.txt",
                "size_bytes": -1,
                "sha256": "a" * 64,
            }
        ],
    }

    with pytest.raises(ValueError, match="non-negative integer"):
        verify_manifest(manifest, ".")


def test_reject_non_object_file_record():
    from evidence_tool.manifest import verify_manifest

    manifest = {
        "schema_version": 1,
        "algorithm": "SHA-256",
        "files": ["evidence.txt"],
    }

    with pytest.raises(ValueError, match="JSON object"):
        verify_manifest(manifest, ".")
