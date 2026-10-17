
import json

from evidence_tool.cli import main


def test_create_command_success(tmp_path, monkeypatch):
    evidence_dir = tmp_path / "evidence"
    evidence_dir.mkdir()
    (evidence_dir / "sample.txt").write_text(
        "synthetic evidence",
        encoding="utf-8",
    )

    manifest_path = tmp_path / "manifest.json"

    monkeypatch.setattr(
        "sys.argv",
        [
            "evidence-tool",
            "create",
            "--base-dir",
            str(evidence_dir),
            "--files",
            "sample.txt",
            "--output",
            str(manifest_path),
        ],
    )

    assert main() == 0
    assert manifest_path.is_file()

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert len(manifest["files"]) == 1
    assert manifest["files"][0]["path"] == "sample.txt"


def test_verify_command_detects_modified_file(tmp_path, monkeypatch):
    evidence_dir = tmp_path / "evidence"
    evidence_dir.mkdir()

    evidence_file = evidence_dir / "sample.txt"
    evidence_file.write_text("original content", encoding="utf-8")

    manifest_path = tmp_path / "manifest.json"

    monkeypatch.setattr(
        "sys.argv",
        [
            "evidence-tool",
            "create",
            "--base-dir",
            str(evidence_dir),
            "--files",
            "sample.txt",
            "--output",
            str(manifest_path),
        ],
    )
    assert main() == 0

    evidence_file.write_text("modified content", encoding="utf-8")

    monkeypatch.setattr(
        "sys.argv",
        [
            "evidence-tool",
            "verify",
            "--base-dir",
            str(evidence_dir),
            "--manifest",
            str(manifest_path),
        ],
    )

    assert main() == 1


def test_verify_command_missing_manifest_returns_error(
    tmp_path,
    monkeypatch,
    capsys,
):
    evidence_dir = tmp_path / "evidence"
    evidence_dir.mkdir()

    missing_manifest = tmp_path / "does-not-exist.json"

    monkeypatch.setattr(
        "sys.argv",
        [
            "evidence-tool",
            "verify",
            "--base-dir",
            str(evidence_dir),
            "--manifest",
            str(missing_manifest),
        ],
    )

    assert main() == 2
    assert "ERROR:" in capsys.readouterr().err
