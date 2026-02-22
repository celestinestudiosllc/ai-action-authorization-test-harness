# src/harness/audit.py

from __future__ import annotations

import json
from datetime import datetime, timezone

try:
    # Python 3.8+
    from importlib.metadata import version as pkg_version
except Exception:  # pragma: no cover
    pkg_version = None  # type: ignore


def _get_harness_version() -> str:
    """
    Resolve the harness version from installed package metadata.
    Falls back safely if metadata is unavailable.
    """
    if pkg_version is None:
        return "unknown"

    # Package name must match pyproject [project].name
    pkg_name = "ai-action-authorization-test-harness"
    try:
        return pkg_version(pkg_name)
    except Exception:
        return "unknown"


def log_event(logfile, matrix_id, result):
    entry = {
        "timestamp_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        "matrix_id": matrix_id,
        "decision": result["decision"],
        "reason": result["reason"],
        "signals": result.get("signals", []),
        "harness_version": _get_harness_version(),
    }

    with open(logfile, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")