# src/harness/runner.py

from __future__ import annotations

from pathlib import Path

from .loader import load_matrices
from .gate import evaluate
from .audit import log_event


def run_all(matrix_dir, output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    logfile = output_dir / "audit.jsonl"

    # ✅ Always start fresh so reports reflect ONLY this run
    logfile.write_text("", encoding="utf-8")

    matrices = load_matrices(matrix_dir)

    print(f"Running {len(matrices)} tests...\n")

    for m in matrices:
        matrix_id = m.get("id", "unknown")
        matrix_title = m.get("title", "")

        result = evaluate(m.get("user_prompt", ""))

        print(f"{matrix_id} -> {result['decision']} ({result['reason']})")

        # Prefer upgraded audit signature: log_event(logfile, matrix_id, title, result)
        try:
            log_event(logfile, matrix_id, matrix_title, result)
        except TypeError:
            # Backward compat: log_event(logfile, matrix_id, result)
            log_event(logfile, matrix_id, result)

    print("\nAudit log saved to:", logfile)