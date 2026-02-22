# src/harness/report.py

from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime


def generate_report(audit_log_path: Path, output_dir: Path):
    """
    Generates a clean, single-run authorization report.

    IMPORTANT:
    - Only reads the current run's audit file
    - Overwrites previous report
    - Produces a human-readable artifact
    """
    output_dir = Path(output_dir)
    report_file = output_dir / "authorization_report.txt"

    # Always overwrite old report
    report_lines: list[str] = []
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%SZ")

    report_lines.append("AI ACTION AUTHORIZATION TEST REPORT")
    report_lines.append("===================================")
    report_lines.append(f"Generated (UTC): {now}")
    report_lines.append("")

    audit_path = Path(audit_log_path)
    if not audit_path.exists():
        report_lines.append("No audit log found.")
    else:
        with open(audit_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    continue

                matrix_id = entry.get("matrix_id", "unknown")
                decision = entry.get("decision", "unknown")
                reason = entry.get("reason", "")

                report_lines.append(f"Matrix: {matrix_id}")
                report_lines.append(f"Decision: {decision}")
                report_lines.append(f"Reason: {reason}")

                signals = entry.get("signals", [])
                # Normalize signals (list expected)
                if isinstance(signals, str):
                    signals = [signals]
                if signals:
                    report_lines.append(f"Signals Detected: {', '.join(signals)}")
                else:
                    report_lines.append("Signals Detected: (none)")

                report_lines.append("")

    report_lines.append("----")
    report_lines.append(
        "This report was generated using the AI Action Authorization Test Harness."
    )
    report_lines.append(
        "For questions about authorization modeling or implementation approaches, contact: celestinestudiosllc@gmail.com"
    )

    with open(report_file, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))

    print(f"Authorization report written to: {report_file}")