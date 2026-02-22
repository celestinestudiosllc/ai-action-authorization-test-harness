# src/harness/audit.py

import json
from datetime import datetime, timezone


def log_event(logfile, matrix_id, result):
    entry = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "matrix_id": matrix_id,
        "decision": result.get("decision", "UNKNOWN"),
        "reason": result.get("reason", ""),
        "signals": result.get("signals", []),
        "harness_version": "0.1.0",
    }

    with open(logfile, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")