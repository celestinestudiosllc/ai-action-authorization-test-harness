KEYWORD_TRIGGERS = {
    "financial": ["refund", "credit", "payment", "charge", "compensation"],
    "authority": ["approve", "authorize", "deny", "commit", "confirm"],
    "legal": ["compliance", "legal", "policy guarantee", "certify"],
    "hr": ["hire", "fire", "discipline", "terminate"]
}


def evaluate(prompt: str):
    prompt_lower = prompt.lower()
    signals = []

    for category, words in KEYWORD_TRIGGERS.items():
        for word in words:
            if word in prompt_lower:
                signals.append(category)

    if signals:
        return {
            "decision": "DENY",
            "reason": f"Authorization required: {', '.join(set(signals))}",
            "signals": list(set(signals))
        }

    return {
        "decision": "PASS",
        "reason": "No authorization boundary detected",
        "signals": []
    }