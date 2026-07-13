# Observability with LangSmith & Logfire

## Overview

Observability is essential when building production-grade AI agents. It helps you understand **what your agents are doing, why they made certain decisions, how long tasks take, and where failures occur**.

This project uses two complementary observability tools:

* **LangSmith** – AI/LLM tracing, prompts, tool calls, and graph execution.
* **Logfire** – Application logs, spans, timings, and exceptions.

> **Recommendation:** Use **both** together. LangSmith helps debug AI behavior, while Logfire helps monitor application performance and reliability.

---

# Observability Architecture

```text
                        User
                          │
                          ▼
                Supervisor Agent
                          │
             ┌────────────┴────────────┐
             │                         │
             ▼                         ▼
      Async Researcher          Async Coder
             │                         │
             ▼                         ▼
       LangSmith Trace          LangSmith Trace
             │                         │
             ▼                         ▼
        Tool Calls                Tool Calls
             │                         │
             ▼                         ▼
        Logfire Logs             Logfire Logs
             │                         │
             └──────────┬──────────────┘
                        ▼
               Observability Dashboard
```

---

# Why Use Both?

| Feature              | LangSmith | Logfire |
| -------------------- | --------- | ------- |
| Prompt inspection    | ✅         | ❌       |
| LLM responses        | ✅         | ❌       |
| Tool execution       | ✅         | Partial |
| Graph execution      | ✅         | ❌       |
| Token usage          | ✅         | ❌       |
| Structured logs      | ❌         | ✅       |
| Exceptions           | Limited   | ✅       |
| Performance metrics  | Partial   | ✅       |
| Custom spans         | ❌         | ✅       |
| Async task lifecycle | Partial   | ✅       |

---

# LangSmith

## What It Captures

* Prompt templates
* User messages
* LLM responses
* Tool invocations
* Graph execution
* Token usage
* Latency
* Errors
* Agent hierarchy

---

## Installation

```bash
pip install langsmith
```

---

## Environment Variables

Create a `.env` file.

```env
LANGSMITH_API_KEY=YOUR_API_KEY
LANGSMITH_TRACING=true
LANGSMITH_PROJECT=DeepAgents-Async
```

Load environment variables:

```python
from dotenv import load_dotenv
load_dotenv()
```

No additional setup is required. LangChain and LangGraph automatically send traces when tracing is enabled.

---

## What You'll See

Example hierarchy:

```text
Supervisor

│

├── Launch Async Researcher

│

└── Return Immediately



Researcher Graph

│

├── Prompt

├── Tool

├── LLM

└── Response
```

Each AsyncSubAgent creates its own trace, making it easier to inspect independently.

---

# Logfire

## What It Captures

* Structured logs
* Application spans
* Execution timings
* Exceptions
* Custom events
* Metadata

Logfire complements LangSmith by observing your application rather than the LLM.

---

## Installation

```bash
pip install logfire
```

---

## Authentication

Authenticate once:

```bash
logfire auth
```

or

```bash
python -m logfire auth
```

Alternatively, configure a project write token.

```env
LOGFIRE_TOKEN=YOUR_LOGFIRE_TOKEN
```

---

# observability.py

Create a shared module.

```python
from dotenv import load_dotenv
import logfire

load_dotenv()

logfire.configure(
    service_name="deepagents"
)
```

Import this module before creating any graph.

Example:

```python
import observability

from langgraph.prebuilt import create_react_agent
```

---

# Logging Information

```python
import logfire

logfire.info(
    "Launching async researcher",
    graph="researcher",
    user="demo"
)
```

---

# Logging Errors

```python
try:
    ...
except Exception:
    logfire.exception("Research failed")
```

---

# Custom Spans

```python
with logfire.span("research_task"):
    result = await graph.ainvoke(inputs)
```

Nested spans:

```text
research_task

├── search

├── summarize

└── return
```

---

# Async Task Lifecycle

Example:

```python
logfire.info(
    "Task launched",
    task_id=task_id
)

...

logfire.info(
    "Task completed",
    task_id=task_id
)
```

---

# Recommended Metadata

Use consistent metadata across all graphs.

```python
logfire.info(
    "Task started",
    graph_id="researcher",
    thread_id=thread_id,
    task_id=task_id,
    agent="researcher"
)
```

Useful identifiers:

* graph_id
* thread_id
* task_id
* agent
* user_id
* session_id

---

# Recommended Project Structure

```text
project/

observability.py

model.py

supervisor.py
researcher.py
coder.py
web_search.py

langgraph.json

README.md
Observability_Readme.md
```

---

# Import Order

Always initialize observability before creating graphs.

```python
import observability

from model import model

from langgraph.prebuilt import create_react_agent
```

---

# Best Practices

* Initialize observability only once.
* Use a shared `observability.py`.
* Keep LangSmith enabled in development.
* Use structured Logfire logs instead of `print()`.
* Include metadata such as `thread_id`, `graph_id`, and `task_id`.
* Create spans around long-running operations.
* Log exceptions with `logfire.exception()`.

---

# Current Logfire Note

Recent versions of Logfire (v4.x and later) **do not provide** `logfire.instrument_langchain()`.

If you're using Logfire 4.x:

```python
import logfire

logfire.configure(
    service_name="deepagents"
)
```

is sufficient for initialization.

For detailed LLM and LangGraph execution traces, rely on **LangSmith**.

---

# End-to-End Flow

```text
User

│

▼

Supervisor

│

├────────────── LangSmith Trace

│

├────────────── Logfire Span

│

├────────────── Launch Async Researcher

│

▼

Researcher Graph

│

├────────────── LangSmith Trace

│

├────────────── Tool Execution

│

├────────────── LLM Response

│

└────────────── Logfire Events

│

▼

Task Completed
```

---

# Summary

| Component | Responsibility                                                         |
| --------- | ---------------------------------------------------------------------- |
| LangSmith | Prompt tracing, graph execution, tool calls, token usage, AI debugging |
| Logfire   | Application logs, structured events, spans, timings, exceptions        |
| Combined  | Complete observability for production-grade DeepAgents applications    |

By combining LangSmith and Logfire, you gain visibility into both **AI decision-making** and **application behavior**, making it significantly easier to debug, monitor, and operate asynchronous multi-agent systems in development and production.
