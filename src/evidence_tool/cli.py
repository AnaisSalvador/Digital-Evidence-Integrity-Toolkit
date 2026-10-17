
import argparse
import sys

from evidence_tool.manifest import (
    create_manifest,
    load_manifest,
    save_manifest,
    verify_manifest,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Digital Evidence Integrity Toolkit"
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    create_parser = subparsers.add_parser(
        "create",
        help="Create an evidence integrity manifest",
    )
    create_parser.add_argument(
        "--base-dir",
        required=True,
        help="Root directory containing the evidence",
    )
    create_parser.add_argument(
        "--files",
        nargs="+",
        required=True,
        help="Relative paths of the evidence files",
    )
    create_parser.add_argument(
        "--output",
        required=True,
        help="Path where the JSON manifest will be saved",
    )

    verify_parser = subparsers.add_parser(
        "verify",
        help="Verify evidence against a manifest",
    )
    verify_parser.add_argument(
        "--base-dir",
        required=True,
        help="Root directory containing the evidence",
    )
    verify_parser.add_argument(
        "--manifest",
        required=True,
        help="Path to the JSON manifest",
    )

    args = parser.parse_args()

    try:
        if args.command == "create":
            manifest = create_manifest(
                args.files,
                base_dir=args.base_dir,
            )
            save_manifest(manifest, args.output)

            print(f"Manifest created: {args.output}")
            print(f"Files recorded: {len(manifest['files'])}")
            return 0

        manifest = load_manifest(args.manifest)
        results = verify_manifest(manifest, args.base_dir)

        for result in results:
            print(f"{result['status']}: {result['path']}")

        failed = sum(
            result["status"] != "MATCH"
            for result in results
        )
        print(
            f"\nVerification complete: "
            f"{len(results) - failed} MATCH, {failed} issue(s)"
        )

        return 1 if failed else 0

    except (OSError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
