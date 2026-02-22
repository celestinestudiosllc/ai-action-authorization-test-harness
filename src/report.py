import json
from datetime import datetime
from pathlib import Path

def generate_report(audit_log_path, out_dir):
    out_dir = Path(out_dir)
    audit_log_path = Path(audit_log_path)

    report_lines = []
    report_lines.append("AI ACTION AUTHORIZATION TEST REPORT")
    report_lines.append("===================================")
    report_lines.append(f"Generated (UTC): {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%SZ')}")
    report_lines.append("")

    if not audit_log_path.exists():
        report_lines.append("No audit log found.")
    else:
        with open(audit_log_path, "r") as f:
            for line in f:
                entry = json.loads(line)

                report_lines.append(f"Matrix: {entry.get('matrix_id', 'unknown')}")
                report_lines.append(f"Decision: {entry.get('decision', 'unknown')}")
                report_lines.append(f"Reason: {entry.get('reason', 'n/a')}")
                signals = ", ".join(entry.get("signals", []))
                report_lines.append(f"Signals Detected: {signals}")
                report_lines.append("")

    report_lines.append("----")
    report_lines.append("This report was generated using the AI Action Authorization Test Harness.")
    report_lines.append("For questions about authorization modeling or implementation approaches, contact: celestinestudiosllc@gmail.com")

    output_file = out_dir / "authorization_report.txt"
    with open(output_file, "w") as f:
        f.write("\n".join(report_lines))

    print(f"Authorization report written to: {output_file}")