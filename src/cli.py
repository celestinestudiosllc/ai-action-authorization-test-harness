# src/cli.py

import argparse
from pathlib import Path

from harness.runner import run_all
from harness.report import generate_report


def main():

    parser = argparse.ArgumentParser(
        description="AI Action Authorization Test Harness"
    )

    parser.add_argument(
        "command",
        nargs="?",
        help="Command to run (use 'run' to execute test matrices)"
    )

    parser.add_argument(
        "--matrices",
        required=True,
        help="Directory or YAML file containing matrix test definitions"
    )

    parser.add_argument(
        "--out",
        required=True,
        help="Output directory for logs and reports"
    )

    args = parser.parse_args()

    # Ensure command was provided
    if args.command != "run":
        print("Usage: python src/cli.py run --matrices <path> --out <path>")
        return

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Run test harness
    run_all(args.matrices, str(out_dir))

    # Generate report from this run
    audit_log = out_dir / "audit.jsonl"

    if audit_log.exists():
        generate_report(audit_log, out_dir)
    else:
        print("No audit log found — report not generated.")


if __name__ == "__main__":
    main()