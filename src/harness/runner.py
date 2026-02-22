# src/harness/runner.py

from pathlib import Path

from .loader import load_matrices
from .gate import evaluate
from .audit import log_event


def run_all(matrix_dir, output_dir):
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    logfile = Path(output_dir) / "audit.jsonl"

    # ✅ Always start fresh so reports reflect ONLY this run
    # (prevents old PASS/DENY entries from showing up in the same report)
    logfile.write_text("", encoding="utf-8")

    matrices = load_matrices(matrix_dir)

    print(f"Running {len(matrices)} tests...\n")

    for m in matrices:
        result = evaluate(m["user_prompt"])

        print(f"{m['id']} -> {result['decision']} ({result['reason']})")

        log_event(logfile, m["id"], result)

    print("\nAudit log saved to:", logfile)