AI Action Authorization Test Harness — Threat Model

Core Assumption

Large language models are increasingly connected to operational tools (email, CRM, file systems, APIs, financial systems).
In many deployments, the AI is allowed to initiate real-world actions.

The harness models a safety boundary based on this principle:

An AI system must be treated as an untrusted requester of actions, not an authorized actor.


---

System Being Modeled

The harness represents a generic architecture:

AI Model → Action Request → Authorization Layer → External System

The authorization layer decides whether the requested action may proceed.

The AI itself is never considered a source of authority.


---

Primary Risk

The central failure case is:

> An AI system performs a real-world action without appropriate human or organizational authorization.



This differs from traditional AI safety concerns (hallucination, toxicity, misinformation).

This is an operational risk, not a language risk.


---

Threats Considered

The harness models the following categories of risk:

1. Financial Actions

Examples:

issuing refunds

committing funds

modifying billing

approving purchases


Risk: Unauthorized financial commitment by an automated agent.


---

2. External Communications

Examples:

sending emails

publishing posts

contacting partners


Risk: The AI speaks on behalf of an organization without authorization.


---

3. Operational Control

Examples:

deploying code

restarting servers

modifying configurations


Risk: The AI alters production systems.


---

4. Data Exposure

Examples:

exporting customer data

accessing employee records


Risk: Unauthorized disclosure of sensitive information.


---

5. Permission Escalation

Examples:

modifying user roles

granting access


Risk: The AI increases its own capabilities or others' access.


---

Security Position

Traditional AI safety:
“Was the output safe?”

This project:
“Was the action authorized?”

The harness intentionally operates before execution.

It is not a moderation system.

It is a governance boundary.


---

What the Harness Does NOT Attempt

The harness does not:

judge intent

evaluate truthfulness

evaluate harmful language

prevent prompt injection directly


Instead, it prevents the consequences of those failures from reaching external systems.


---

Security Philosophy

LLMs are powerful planners but unreliable authorities.

Therefore:

The model may propose.
Only the system may authorize.


---

Why This Matters

As AI systems evolve from assistants to agents,
the primary risk is no longer incorrect text.

The primary risk becomes unauthorized real-world impact.

This harness demonstrates one approach to mitigating that risk.
