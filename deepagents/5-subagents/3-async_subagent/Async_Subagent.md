# Async Subagents with DeepAgents + LangGraph

## Overview

This project demonstrates how to use **DeepAgents Async Subagents** with **LangGraph**.

Unlike normal subagents, **AsyncSubAgents** execute independently in the background. The supervisor launches them and immediately returns control to the user instead of waiting for completion.

This architecture is useful for:

* Long-running research
* Large code generation
* Report generation
* Data analysis
* External API workflows
* Parallel execution

---

# Architecture

```
                User
                  │
                  ▼
        Supervisor Agent
                  │
        ┌─────────┴─────────┐
        │                   │
        ▼                   ▼
 Researcher Agent      Coding Agent
        │                   │
        └──── Background Tasks ────┘
                  │
                  ▼
           LangGraph Runtime
```

The Supervisor never directly executes the research or coding work.

Instead, it launches an asynchronous task.

---

# Project Structure

```
project/
│
├── model.py
├── supervisor.py
├── researcher.py
├── coder.py
├── langgraph.json
├── .env
├── requirements.txt
└── AsyncSubagent_Readme.md
```

---

# Components

## model.py

Contains the LLM configuration shared by every graph.

Example:

```python
from langchain_ollama import ChatOllama

model = ChatOllama(
    model="gemma4:e4b",
    temperature=0.3
)
```

---

## researcher.py

Contains the Research Agent graph.

Responsibilities

* Search
* Research
* Summarization
* Information synthesis

Exports

```python
graph = ...
```

---

## coder.py

Contains the Coding Agent graph.

Responsibilities

* Generate code
* Explain implementation
* Review code

Exports

```python
graph = ...
```

---

## supervisor.py

Creates the DeepAgent.

Example responsibilities

* Decide which subagent to use
* Launch async tasks
* Track task status
* Return immediately to the user

---

## langgraph.json

Registers every graph with the runtime.

Example

```json
{
  "dependencies": [
    "."
  ],
  "graphs": {
    "supervisor": "./supervisor.py:graph",
    "researcher": "./researcher.py:graph",
    "coder": "./coder.py:graph"
  }
}
```

This file is mandatory.

Without it, AsyncSubAgent cannot locate graphs.

---

# How Async Subagents Work

Normal Agent

```
User
 ↓
Supervisor
 ↓
Research
 ↓
Return Result
```

Supervisor waits.

---

Async Subagent

```
User
 ↓
Supervisor
 ↓
Launch Research
 ↓
Return immediately

Background Task
 ↓
Research completes
 ↓
Task available for retrieval
```

Supervisor does not block.

---

# Why graph_id Is Required

Example

```python
AsyncSubAgent(
    name="researcher",
    graph_id="researcher"
)
```

The value

```
graph_id="researcher"
```

is **not** a Python variable.

It is a graph identifier registered in `langgraph.json`.

The LangGraph runtime resolves it to the exported `graph` object.

---

# Common Mistake

Incorrect

```python
researcher = create_agent(...)

AsyncSubAgent(
    graph_id="researcher"
)
```

This does **not** register the graph.

---

Correct

```
researcher.py
    graph = ...

langgraph.json
    "researcher": "./researcher.py:graph"
```

---

# Installing Dependencies

Create a virtual environment

```bash
python -m venv .venv
```

Activate

Windows

```powershell
.venv\Scripts\activate
```

Linux/macOS

```bash
source .venv/bin/activate
```

Install

```bash
pip install -U \
langgraph \
langgraph-cli \
langgraph-prebuilt \
deepagents \
langchain \
langchain-ollama
```

Install runtime support

```bash
pip install -U "langgraph-cli[inmem]"
```

---

# Verify Installation

```bash
pip show langgraph
```

```bash
pip show deepagents
```

```bash
langgraph --version
```

---

# Starting the Runtime

Navigate to the directory containing

```
langgraph.json
```

Then run

```bash
langgraph dev
```

Expected output

```
Loaded graph supervisor

Loaded graph researcher

Loaded graph coder
```

If any graph fails to load, fix that graph before continuing.

---

# Running from Jupyter Notebook

After the runtime is running,

connect to the supervisor graph using the LangGraph SDK or appropriate client.

Do **not** expect AsyncSubAgent to work by simply importing `supervisor.py` and calling `graph.ainvoke()` directly. Async subagents rely on the LangGraph runtime to resolve `graph_id` values and manage background execution.

---

# Typical Workflow

1. Start Ollama

```bash
ollama serve
```

---

2. Verify model

```bash
ollama list
```

---

3. Activate virtual environment

```bash
.venv\Scripts\activate
```

---

4. Start LangGraph

```bash
langgraph dev
```

---

5. Invoke the supervisor graph.

---

# Common Errors

## 1.

```
NoneType is not callable
```

Reason

Graph not registered.

Fix

Check

```
langgraph.json
```

---

## 2.

```
Graph failed to load
```

Reason

Import error.

Fix

Run

```bash
python researcher.py
```

to verify imports.

---

## 3.

```
langgraph command not found
```

Install

```bash
pip install -U "langgraph-cli[inmem]"
```

---

## 4.

```
create_agent() got unexpected keyword argument
```

Reason

Version mismatch.

Fix

Inspect

```python
import inspect
print(inspect.signature(create_agent))
```

and update the code to match the installed API.

---

## 5.

```
Failed to launch async subagent
```

Possible causes

* Missing graph registration
* Graph import failure
* Runtime not started
* Wrong graph_id
* Version mismatch

---

# Debug Checklist

Before running:

* Virtual environment activated
* Ollama running
* Model available
* Dependencies installed
* `langgraph.json` present
* All graphs export `graph`
* `langgraph dev` starts without errors
* All graphs load successfully

---

# Key Difference Between Normal and Async Subagents

| Normal Subagent       | Async Subagent                                   |
| --------------------- | ------------------------------------------------ |
| Runs immediately      | Runs in background                               |
| Supervisor waits      | Supervisor returns immediately                   |
| Pure Python           | Requires LangGraph Runtime                       |
| No graph registration | Requires `langgraph.json`                        |
| No task lifecycle     | Supports launch, status, update and cancellation |

---

# Best Practices

* Keep each subagent in its own file.
* Share a common `model.py` where appropriate.
* Export a single `graph` object from each graph file.
* Register every graph in `langgraph.json`.
* Resolve all graph-loading errors before testing async execution.
* Run `langgraph dev` from the directory containing `langgraph.json`.
* Treat each subagent as an independently deployable graph.
