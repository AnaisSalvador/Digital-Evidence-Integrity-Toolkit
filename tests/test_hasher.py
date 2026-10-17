
import hashlib

import pytest

from evidence_tool.hasher import calculate_sha256


def test_calculate_sha256(tmp_path):
    file_path = tmp_path / "evidence.txt"
    file_path.write_bytes(b"hello")

    expected = hashlib.sha256(b"hello").hexdigest()

    assert calculate_sha256(file_path) == expected


def test_empty_file(tmp_path):
    file_path = tmp_path / "empty.bin"
    file_path.write_bytes(b"")

    expected = hashlib.sha256(b"").hexdigest()

    assert calculate_sha256(file_path) == expected


def test_missing_file(tmp_path):
    file_path = tmp_path / "missing.txt"

    with pytest.raises(FileNotFoundError):
        calculate_sha256(file_path)
