
AI Action Authorization Test Harness

A practical framework for testing whether an AI system should be allowed to take an action — before it takes it.

Most AI safety mechanisms evaluate model output.
This project evaluates model authority.

We call this:

Authorization Before Execution


---

The Core Idea

Modern LLM systems are increasingly connected to real operational tools:

• CRMs
• Email systems
• Financial systems
• File storage
• Internal APIs
• Automated workflows

In many deployments, the model proposes or initiates actions and downstream systems attempt to filter behavior afterward.

This introduces a structural risk:

> The AI is being treated as a decision authority instead of an execution requester.



Traditional guardrails evaluate text.

This harness evaluates permission to act.


---

The Problem

Current AI safety approaches answer:

> “Was the model’s response safe?”



But operational systems require a different question:

> “Was the model allowed to request this action at all?”



Once an AI can:

• send messages
• trigger workflows
• commit funds
• modify systems
• access sensitive data

…the failure mode changes from bad output to unauthorized execution.

This is not a content filtering problem.

This is an authorization problem.


---

What This Harness Does

The AI Action Authorization Test Harness is a local deterministic evaluation system that checks:

Should an AI system be allowed to attempt an action?

Each test matrix simulates a real-world operational request and evaluates it against governance signals such as:

• financial commitment
• authority level
• operational control
• data sensitivity
• external communication
• system modification

The harness outputs a binary operational decision:

ALLOW or DENY

and produces an auditable reasoning trail.


---

What Makes It Different

Instead of moderating language, this project models a pre-execution authorization gate.

Think of it as:

A permissions layer for AI agents.

The model can still reason.
But it cannot act without authorization.


---

What You Can Do With It

You can locally run authorization simulations to understand where an AI system should require human approval before real-world action.

The harness will:

1. Evaluate an action request


2. Detect authorization signals


3. Decide ALLOW or DENY


4. Produce an audit log


5. Produce a human-readable report


6. Produce a CSV analysis report



This allows teams to explore governance controls before connecting AI to production systems.


---

Quick Start

Clone the repository:

git clone https://github.com/celestinestudiosllc/ai-action-authorization-test-harness.git
cd ai-action-authorization-test-harness

Create a virtual environment:

python3 -m venv venv
source venv/bin/activate
pip install -e .

Run the harness:

python -m src.cli run --matrices examples/matrices --out outputs/test_run


---

What You Will Get

The harness produces:

Console Decision Output

01_financial_commitment -> DENY
Authorization required: authority, financial

Audit Log

outputs/test_run/audit.jsonl

Human-Readable Report

outputs/test_run/authorization_report.txt

Spreadsheet Report

outputs/test_run/authorization_report.csv


---

Example Authorization Result

Matrix: 01_financial_commitment
Decision: DENY
Reason: Authorization required: authority, financial
Signals Detected: authority, financial


---

What the Matrices Represent

Each matrix simulates a realistic AI action scenario, such as:

• sending external emails
• deploying to production
• exporting customer data
• modifying user permissions
• issuing refunds
• restarting servers
• scheduling social media posts
• accessing employee records

These represent real operational tool-use behaviors an AI agent could perform.


---

Intended Audience

This project is relevant to:

• AI engineers
• system architects
• platform teams
• DevOps engineers
• security teams
• governance & compliance teams
• organizations integrating AI with operational systems


---

Not a Product

This repository is a public research harness and reference implementation.

It is intentionally transparent and deterministic so the authorization logic can be examined, discussed, and extended.


---

What This Project Explores

A shift from:

AI Safety — controlling responses

to:

AI Governance — controlling actions


---

Safety Notice

This harness:

• runs locally
• does not call external APIs
• does not execute real actions
• does not control real systems

It simulates authorization decisions only.

Try to Break It
This harness is intentionally simple and transparent.
If you connect an LLM to tools, workflows, APIs, or automation systems, this project is meant to provoke a question:
Where should authorization actually live?
We are actively interested in:
failure cases
bypass ideas
edge scenarios
adversarial prompts
real-world integration attempts
If you find a case where an action should be blocked but is allowed — or allowed but should be blocked — please open an issue or contact us.
The goal is not to prove a solution is complete.
The goal is to explore whether authorization-before-execution should exist as a standard layer in AI-integrated systems.
---

Contact

For questions about authorization modeling or implementation approaches:

celestinestudiosllc@gmail.com


---

License

MIT License
