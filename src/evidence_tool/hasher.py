
import hashlib
from pathlib import Path


def calculate_sha256(file_path: str | Path) -> str:
    """Calculate the SHA-256 hash of a file."""
    path = Path(file_path)

    if not path.is_file():
        raise FileNotFoundError(f"File not found: {path}")

    digest = hashlib.sha256()

    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)

    return digest.hexdigest()
