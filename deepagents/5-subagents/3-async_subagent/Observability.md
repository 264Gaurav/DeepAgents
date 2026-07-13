# Observability with LangSmith & Logfire

## Overview

Modern AI applications require observability at multiple levels.

This project uses two complementary platforms:

* **LangSmith** – LLM, Agent, LangChain and LangGraph tracing
* **Logfire** – OpenTelemetry visualization, structured logs, spans, performance metrics and application monitoring

Together they provide complete visibility into your AI system.

---

# Architecture

```text
                    User
                      │
                      ▼
              Supervisor Agent
                      │
        ┌─────────────┴─────────────┐
        │                           │
        ▼                           ▼
 Async Researcher             Async Coder
        │                           │
        ▼                           ▼
  Web Search Tool            Code Generation
        │                           │
        ▼                           ▼
     LangGraph Nodes         LangGraph Nodes
        │                           │
        └─────────────┬─────────────┘
                      │
        LangSmith OpenTelemetry
                      │
               OpenTelemetry
                      │
              ┌───────┴────────┐
              │                │
              ▼                ▼
         LangSmith         Logfire
```

---

# Responsibilities

## LangSmith

LangSmith is responsible for AI tracing.

It automatically captures:

* Prompt templates
* User messages
* Chat history
* Tool calls
* Agent execution
* LangGraph nodes
* Async SubAgents
* Token usage
* Latency
* LLM responses
* Errors

LangSmith should be considered the primary debugging tool for AI workflows.

---

## Logfire

Logfire is responsible for application observability.

It captures:

* OpenTelemetry traces
* Structured logs
* Custom spans
* Exceptions
* Performance timings
* Request lifecycle
* Async task lifecycle

Logfire should be considered the primary monitoring tool.

---

# Why Both?

| Feature         | LangSmith | Logfire         |
| --------------- | --------- | --------------- |
| Prompt tracing  | ✅         | Through OTEL    |
| Tool calls      | ✅         | Through OTEL    |
| LangGraph nodes | ✅         | Through OTEL    |
| Async SubAgents | ✅         | Through OTEL    |
| Token usage     | ✅         | Span attributes |
| Structured logs | ❌         | ✅               |
| Exceptions      | Partial   | ✅               |
| Performance     | Partial   | ✅               |
| Custom spans    | ❌         | ✅               |

---

# Installation

```bash
pip install \
deepagents \
langgraph \
langgraph-cli \
langgraph-prebuilt \
langsmith \
"logsmith[otel]" \
logfire
```

or

```bash
pip install -U deepagents langgraph langgraph-cli langgraph-prebuilt langsmith "langsmith[otel]" logfire
```

The OpenTelemetry integration requires the LangSmith package with OTEL support.

---

# Environment Variables

Create a `.env` file.

```env
LANGSMITH_API_KEY=xxxxxxxxxxxxxxxx

LANGSMITH_PROJECT=DeepAgents-Async

LANGSMITH_TRACING=true

LANGSMITH_OTEL_ENABLED=true

LANGSMITH_OTEL_ONLY=true

LOGFIRE_TOKEN=xxxxxxxxxxxxxxxx
```

---

# observability.py

The environment variables must be configured **before importing LangChain or LangGraph**, otherwise OpenTelemetry instrumentation will not be installed.

```python
import os
from dotenv import load_dotenv

load_dotenv()

os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_OTEL_ENABLED"] = "true"
os.environ["LANGSMITH_OTEL_ONLY"] = "true"

import logfire

logfire.configure(
    service_name="deepagents"
)
```

---

# Important Import Order

Correct:

```python
import observability

from langgraph.prebuilt import create_react_agent
```

Wrong:

```python
from langgraph.prebuilt import create_react_agent

import observability
```

Instrumentation happens during import.

---

# Graph Structure

```text
Supervisor

├── Researcher

│      ├── Tavily

│      └── LLM

├── Coder

│      └── LLM

└── Web Search

       └── Tavily
```

Every graph appears independently inside LangSmith.

The corresponding OpenTelemetry spans are exported to Logfire.

---

# Current LangGraph Flow

```
User

↓

Supervisor

↓

Launch AsyncSubAgent

↓

Researcher

↓

Tool Call

↓

LLM

↓

Return Result
```

This entire execution becomes one trace with nested spans.

---

# Logfire

Logfire version 4.x **does not** expose:

```python
logfire.instrument_langchain()
```

Do **not** use this API.

LangChain and LangGraph tracing now rely on LangSmith's OpenTelemetry integration instead.

---

# Adding Application Logs

```python
import logfire

logfire.info(
    "Launching async task",
    graph="researcher",
    task_id=task_id
)
```

---

# Recording Exceptions

```python
try:
    ...
except Exception:
    logfire.exception("Research failed")
```

---

# Custom Spans

```python
import logfire

with logfire.span("internet_search"):
    result = internet_search(query)
```

---

# Async Task Monitoring

```python
logfire.info(
    "Task started",
    graph="researcher",
    thread_id=thread_id,
    task_id=task_id,
)
```

```python
logfire.info(
    "Task completed",
    graph="researcher",
    thread_id=thread_id,
    task_id=task_id,
)
```

---

# Metadata

Recommended metadata:

* graph_id
* thread_id
* task_id
* user_id
* session_id
* request_id

These greatly simplify filtering and correlation.

---

# What Should Appear in LangSmith?

```
Supervisor

├── Researcher

│      ├── Tool

│      ├── Prompt

│      ├── LLM

│      └── Response

├── Web Search

│      └── Tavily

└── Coder

       └── LLM
```

---

# What Should Appear in Logfire?

```
Trace

Supervisor

│

├── Researcher

│      ├── Tool

│      ├── LLM

│      └── Span

│

├── Web Search

│      └── Span

│

└── Coder

       └── Span
```

---

# Troubleshooting

## No traces in LangSmith

Verify:

* `LANGSMITH_API_KEY`
* `LANGSMITH_TRACING=true`
* Correct project name

---

## No traces in Logfire

Check:

* `LOGFIRE_TOKEN`
* `logfire auth`
* `logfire.configure()` is called exactly once
* `observability.py` is imported before LangChain/LangGraph
* `langsmith[otel]` is installed
* `LANGSMITH_OTEL_ENABLED=true`
* `LANGSMITH_OTEL_ONLY=true`

Remember that Logfire visualizes OpenTelemetry spans; it does not instrument LangChain by itself in recent releases.

---

## `instrument_langchain()` Not Found

Expected.

Recent Logfire releases removed this API.

Use the LangSmith OpenTelemetry integration instead.

---

# Best Practices

* Configure observability once in a shared `observability.py`.
* Import `observability` before any LangChain/LangGraph modules.
* Use LangSmith for AI debugging.
* Use Logfire for application monitoring and custom spans.
* Add meaningful metadata (`graph_id`, `thread_id`, `task_id`) to logs and spans.
* Wrap long-running or external operations (searches, database calls, APIs) in `logfire.span()` for additional visibility.

---

# References

* LangSmith OpenTelemetry Guide
* Logfire LangChain/LangGraph Integration
* LangGraph Documentation
* DeepAgents Documentation
