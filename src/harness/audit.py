import json
from datetime import datetime

def log_event(logfile, matrix_id, result):
    entry = {
        "timestamp_utc": datetime.utcnow().isoformat() + "Z",
        "matrix_id": matrix_id,
        "decision": result["decision"],
        "reason": result["reason"],
        "signals": result["signals"],
        "harness_version": "0.1.0"
    }

    with open(logfile, "a") as f:
        f.write(json.dumps(entry) + "\n")