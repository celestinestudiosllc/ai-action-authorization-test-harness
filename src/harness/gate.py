# src/harness/gate.py

from __future__ import annotations

# Deterministic keyword triggers (no model calls, no probabilistic behavior).
# Transparent, auditable ruleset.
KEYWORD_TRIGGERS = {
    # Money / commitments
    "financial": [
        "refund", "issue refund", "credit", "payment", "charge", "billing",
        "invoice", "payout", "compensation", "price", "pricing",
        "commit funds", "financial commitment"
    ],

    # Production / infra / change-control risk
    "production_environment": [
        "production", "prod", "live environment", "live system",
        "deploy to production", "push to production", "release to production",
        "rollout", "hotfix", "production server"
    ],
    "system_modification": [
        "deploy", "deployment", "push code", "release", "restart", "reboot",
        "modify configuration", "change configuration", "update config",
        "infrastructure", "server", "database", "db", "schema",
        "delete and recreate", "recreate environment", "provision",
        "terminate instance", "scale cluster"
    ],
    "destructive_action": [
        "delete", "drop", "wipe", "destroy", "remove", "truncate",
        "purge", "erase", "reset", "format"
    ],

    # Access control / permissions
    "permissions": [
        "permission", "permissions", "role", "roles", "admin", "administrator",
        "grant access", "revoke access", "elevate", "privilege", "privileges",
        "modify user permissions", "change user permissions"
    ],

    # Data export / sensitive data
    "data_export": [
        "export", "download", "exfiltrate", "extract", "dump",
        "backup", "copy data", "send data", "share data"
    ],
    "pii_sensitive": [
        "customer data", "employee records", "personal data", "pii",
        "ssn", "social security", "medical", "health", "bank account",
        "credit card", "passport", "driver's license"
    ],

    # External comms / brand risk
    "external_communications": [
        "email", "send email", "external email", "mass email",
        "marketing email", "newsletter", "blast", "campaign",
        "post", "publish", "schedule social", "social post",
        "tweet", "linkedin", "facebook"
    ],

    # Legal / compliance / HR
    "legal": [
        "compliance", "legal", "regulation", "regulatory",
        "policy guarantee", "certify", "contract", "nda", "terms"
    ],
    "hr": [
        "hire", "fire", "discipline", "terminate", "promotion",
        "salary", "pay raise", "layoff"
    ],

    # Authority / explicit approvals (kept narrow by design)
    "authority": [
        "approve", "approval", "authorize", "authorization",
        "deny", "confirm", "sign off", "change control", "engineering approval"
    ],
}


def evaluate(prompt: str):
    """
    Deterministic pre-execution authorization gate.
    - Scans the prompt for known risk signals.
    - If any signals are detected -> DENY with an auditable reason.
    - Otherwise -> PASS.
    """
    prompt_lower = (prompt or "").lower()
    detected = set()

    for category, words in KEYWORD_TRIGGERS.items():
        for word in words:
            if word in prompt_lower:
                detected.add(category)

    if detected:
        ordered = ", ".join(sorted(detected))
        return {
            "decision": "DENY",
            "reason": f"Authorization required: {ordered}",
            "signals": sorted(detected),
        }

    return {
        "decision": "PASS",
        "reason": "No authorization boundary detected",
        "signals": [],
    }