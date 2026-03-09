# src/harness/runner.py

from __future__ import annotations

import time
from pathlib import Path

from .loader import load_matrices
from .gate import evaluate
from .audit import log_event


# Terminal colors
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"

FLASH = "\033[5m"


def format_result(index: int, total: int, matrix_id: str, decision: str, reason: str) -> str:
    decision = decision.upper()

    if decision == "PASS":
        status = f"{FLASH}{GREEN}PASS{RESET}"
    elif decision == "DENY":
        status = f"{RED}DENY{RESET}"
    else:
        status = f"{YELLOW}{decision}{RESET}"

    counter = f"[{index}/{total}]"

    return f"{counter:<8} {matrix_id:<30} -> {status}   ({reason})"


def run_all(matrix_dir, output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    logfile = output_dir / "audit.jsonl"

    # Start fresh each run
    logfile.write_text("", encoding="utf-8")

    matrices = load_matrices(matrix_dir)

    total_tests = len(matrices)

    print("")
    print("AI ACTION AUTHORIZATION TEST HARNESS")
    print("====================================")
    print(f"Running {total_tests} tests...\n")

    pass_count = 0
    deny_count = 0
    other_count = 0

    for idx, m in enumerate(matrices, start=1):
        matrix_id = m.get("id", "unknown")
        matrix_title = m.get("title", "")

        result = evaluate(m.get("user_prompt", ""))

        decision = result["decision"].upper()

        if decision == "PASS":
            pass_count += 1
        elif decision == "DENY":
            deny_count += 1
        else:
            other_count += 1

        print(format_result(idx, total_tests, matrix_id, decision, result["reason"]))

        # pause briefly so PASS visually lands
        if decision == "PASS":
            time.sleep(0.8)

        try:
            log_event(logfile, matrix_id, matrix_title, result)
        except TypeError:
            log_event(logfile, matrix_id, result)

    total = pass_count + deny_count + other_count

    print("\n------------------------------------")
    print("RUN SUMMARY")
    print("-----------")
    print(f"Total Tests : {total}")
    print(f"{RED}DENY{RESET}        : {deny_count}")
    print(f"{GREEN}PASS{RESET}        : {pass_count}")

    if other_count:
        print(f"{YELLOW}OTHER{RESET}       : {other_count}")

    print("\nAudit log saved to:", logfile)