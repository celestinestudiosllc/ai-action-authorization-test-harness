import argparse
import os

from harness.runner import run_all
from report import generate_report


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
        help="Directory containing matrix test definitions"
    )

    parser.add_argument(
        "--out",
        required=True,
        help="Output directory for logs and reports"
    )

    args = parser.parse_args()

    # Run tests
    run_all(args.matrices, args.out)

    # After running, generate report
    audit_log = os.path.join(args.out, "audit.jsonl")

    if os.path.exists(audit_log):
        generate_report(audit_log, args.out)
        print(f"\nAuthorization report generated: {args.out}/authorization_report.txt")
    else:
        print("No audit log found — report not generated.")


if __name__ == "__main__":
    main()