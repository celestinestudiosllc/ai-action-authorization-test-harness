# src/harness/report.py

from __future__ import annotations

import csv
import json
from pathlib import Path
from datetime import datetime
from collections import Counter
from typing import Any


def _safe_list(value: Any) -> list[str]:
    """Normalize signals into a list[str]."""
    if value is None:
        return []
    if isinstance(value, list):
        return [str(x) for x in value if x is not None]
    if isinstance(value, str):
        return [value]
    return [str(value)]


def _write_txt(path: Path, lines: list[str]) -> None:
    """
    Write a text report with a trailing newline for clean terminal output.
    """
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def generate_report(audit_log_path: Path, output_dir: Path):
    """
    Generates clean, single-run authorization reports.

    Outputs:
      - authorization_report.txt  (human readable)
      - authorization_report.csv  (spreadsheet friendly)

    IMPORTANT:
    - Only reads the current run's audit file
    - Overwrites previous reports
    - Produces auditable artifacts
    """
    output_dir = Path(output_dir)
    txt_file = output_dir / "authorization_report.txt"
    csv_file = output_dir / "authorization_report.csv"

    report_lines: list[str] = []
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%SZ")

    report_lines.append("AI ACTION AUTHORIZATION TEST REPORT")
    report_lines.append("===================================")
    report_lines.append(f"Generated (UTC): {now}")
    report_lines.append("")

    audit_path = Path(audit_log_path)
    if not audit_path.exists():
        report_lines.append("No audit log found.")
        # Write TXT
        _write_txt(txt_file, report_lines)
        # Write CSV (header only)
        with open(csv_file, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(
                [
                    "timestamp_utc",
                    "matrix_id",
                    "matrix_title",
                    "decision",
                    "reason",
                    "signals",
                    "harness_version",
                ]
            )
        print(f"Authorization report written to: {txt_file}")
        print(f"Authorization CSV written to: {csv_file}")
        return

    # Load audit entries
    entries: list[dict[str, Any]] = []
    with open(audit_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
                if isinstance(entry, dict):
                    entries.append(entry)
            except json.JSONDecodeError:
                continue

    if not entries:
        report_lines.append("Audit log exists but contains no readable entries.")
        _write_txt(txt_file, report_lines)
        with open(csv_file, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(
                [
                    "timestamp_utc",
                    "matrix_id",
                    "matrix_title",
                    "decision",
                    "reason",
                    "signals",
                    "harness_version",
                ]
            )
        print(f"Authorization report written to: {txt_file}")
        print(f"Authorization CSV written to: {csv_file}")
        return

    # Summary stats
    total = len(entries)
    decisions = [str(e.get("decision", "unknown")).upper() for e in entries]
    deny_count = sum(1 for d in decisions if d == "DENY")
    pass_count = sum(1 for d in decisions if d == "PASS")
    unknown_count = total - deny_count - pass_count
    deny_rate = (deny_count / total) * 100.0 if total else 0.0

    report_lines.append("SUMMARY")
    report_lines.append("-------")
    report_lines.append(f"Total Matrices: {total}")
    report_lines.append(f"DENY: {deny_count}")
    report_lines.append(f"PASS: {pass_count}")
    if unknown_count:
        report_lines.append(f"UNKNOWN: {unknown_count}")
    report_lines.append(f"DENY Rate: {deny_rate:.1f}%")
    report_lines.append("")

    # Signal frequency (DENY only)
    signal_counter: Counter[str] = Counter()
    for e in entries:
        if str(e.get("decision", "")).upper() == "DENY":
            for s in _safe_list(e.get("signals", [])):
                signal_counter[s] += 1

    if signal_counter:
        report_lines.append("DENY SIGNAL FREQUENCY")
        report_lines.append("---------------------")
        for sig, count in signal_counter.most_common():
            report_lines.append(f"{sig}: {count}")
        report_lines.append("")

    # Sort entries: DENY first, then PASS, then unknown
    def sort_key(e: dict[str, Any]) -> tuple[int, str]:
        d = str(e.get("decision", "")).upper()
        bucket = 0 if d == "DENY" else 1 if d == "PASS" else 2
        mid = str(e.get("matrix_id", ""))
        return (bucket, mid)

    entries_sorted = sorted(entries, key=sort_key)

    # DETAILS (TXT)
    report_lines.append("DETAILS")
    report_lines.append("-------")

    for e in entries_sorted:
        matrix_id = str(e.get("matrix_id", "unknown"))
        matrix_title = e.get("matrix_title")
        decision = str(e.get("decision", "unknown")).upper()
        reason = str(e.get("reason", ""))

        if matrix_title:
            report_lines.append(f"Matrix: {matrix_id} — {matrix_title}")
        else:
            report_lines.append(f"Matrix: {matrix_id}")

        report_lines.append(f"Decision: {decision}")
        report_lines.append(f"Reason: {reason}")

        signals = _safe_list(e.get("signals", []))
        if signals:
            report_lines.append(f"Signals Detected: {', '.join(signals)}")
        else:
            report_lines.append("Signals Detected: (none)")

        report_lines.append("")

    report_lines.append("----")
    report_lines.append("This report was generated using the AI Action Authorization Test Harness.")
    report_lines.append(
        "For questions about authorization modeling or implementation approaches, contact: celestinestudiosllc@gmail.com"
    )

    # Write TXT (overwrite)
    _write_txt(txt_file, report_lines)

    # Write CSV (overwrite)
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(
            [
                "timestamp_utc",
                "matrix_id",
                "matrix_title",
                "decision",
                "reason",
                "signals",
                "harness_version",
            ]
        )
        for e in entries_sorted:
            w.writerow(
                [
                    e.get("timestamp_utc", ""),
                    e.get("matrix_id", ""),
                    e.get("matrix_title", ""),
                    str(e.get("decision", "")).upper(),
                    e.get("reason", ""),
                    ", ".join(_safe_list(e.get("signals", []))),
                    e.get("harness_version", ""),
                ]
            )

    print(f"Authorization report written to: {txt_file}")
    print(f"Authorization CSV written to: {csv_file}")