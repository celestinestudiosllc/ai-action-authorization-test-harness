from .loader import load_matrices
from .gate import evaluate
from .audit import log_event
from pathlib import Path

def run_all(matrix_dir, output_dir):
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    logfile = Path(output_dir) / "audit.jsonl"

    matrices = load_matrices(matrix_dir)

    print(f"Running {len(matrices)} tests...\n")

    for m in matrices:
        result = evaluate(m["user_prompt"])

        print(f"{m['id']} -> {result['decision']} ({result['reason']})")

        log_event(logfile, m["id"], result)

    print("\nAudit log saved to:", logfile)