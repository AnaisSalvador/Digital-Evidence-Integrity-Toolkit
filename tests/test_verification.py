
import pytest

from evidence_tool.manifest import create_manifest, verify_manifest

from evidence_tool.manifest import verify_manifest


def test_verify_unchanged_file(tmp_path):
    evidence_file = tmp_path / "evidence.txt"
    evidence_file.write_bytes(b"original evidence")

    manifest = create_manifest(
        ["evidence.txt"],
        base_dir=tmp_path,
    )

    results = verify_manifest(manifest, tmp_path)

    assert results == [
        {"path": "evidence.txt", "status": "MATCH"}
    ]


def test_detect_modified_file(tmp_path):
    evidence_file = tmp_path / "evidence.txt"
    evidence_file.write_bytes(b"original evidence")

    manifest = create_manifest(
        ["evidence.txt"],
        base_dir=tmp_path,
    )

    evidence_file.write_bytes(b"modified evidence")

    results = verify_manifest(manifest, tmp_path)

    assert results == [
        {"path": "evidence.txt", "status": "MISMATCH"}
    ]


def test_detect_missing_file(tmp_path):
    evidence_file = tmp_path / "evidence.txt"
    evidence_file.write_bytes(b"original evidence")

    manifest = create_manifest(
        ["evidence.txt"],
        base_dir=tmp_path,
    )

    evidence_file.unlink()

    results = verify_manifest(manifest, tmp_path)

    assert results == [
        {"path": "evidence.txt", "status": "MISSING"}
    ]


def test_reject_path_traversal(tmp_path):
    evidence_dir = tmp_path / "evidence"
    evidence_dir.mkdir()

    outside_file = tmp_path / "outside.txt"
    outside_file.write_text("not evidence", encoding="utf-8")

    manifest = {
        "schema_version": 1,
        "algorithm": "SHA-256",
        "files": [
            {
                "path": "../outside.txt",
                "size_bytes": outside_file.stat().st_size,
                "sha256": "a" * 64,
            }
        ],
    }

    with pytest.raises(ValueError, match="escapes evidence directory"):
        verify_manifest(manifest, evidence_dir)
