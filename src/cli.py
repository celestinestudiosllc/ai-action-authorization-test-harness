# src/cli.py

import argparse
import os
from pathlib import Path

from harness.runner import run_all
from harness.report import generate_report


def main():
    parser = argparse.ArgumentParser(
        description="AI Action Authorization Test Harness"
    )

    parser.add_argument(
        "run",
        nargs="?",
        help="Run the authorization test matrices"
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

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Run tests (runner is responsible for writing audit.jsonl)
    run_all(args.matrices, str(out_dir))

    # After running, generate report from the audit log created THIS run
    audit_log = out_dir / "audit.jsonl"

    if audit_log.exists():
        generate_report(audit_log, out_dir)
        print(f"\nAuthorization report written to: {out_dir / 'authorization_report.txt'}")
    else:
        print("No audit log found — report not generated.")


if __name__ == "__main__":
    main()