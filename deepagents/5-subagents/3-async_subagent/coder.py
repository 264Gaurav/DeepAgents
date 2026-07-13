import observability
from langgraph.prebuilt import create_react_agent
from model import model

graph = create_react_agent(
    model=model,
    tools=[],
    prompt="""
You are a senior software engineer.

Write production-grade code.

Explain design decisions.
"""
)