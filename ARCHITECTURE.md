AI Action Authorization — Conceptual Architecture

This project demonstrates a separation between two roles that are often conflated in AI systems:

planning and authority.

Large language models are excellent planners.
They can determine how an action should be performed.

However, real-world systems require a separate question:

Is the action allowed to be performed at all?

The harness models an architectural boundary:

AI Model → Action Request → Authorization Layer → External System

The model may propose an action.
The authorization layer decides whether the action may proceed.

The model never directly controls external systems.

This architecture treats the AI as:

an intelligent requester

not

an authorized actor

The goal is not to make the model safer by improving its behavior.

The goal is to make the system safer by removing authority from the model.

In this design, failures in model reasoning, prompt injection, or hallucination cannot directly produce real-world consequences because execution is gated by an independent authorization layer.
