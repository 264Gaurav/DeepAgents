import os
from typing import Literal

import observability

from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool
from tavily import TavilyClient

from model import model

api_key = os.getenv("TAVILY_API_KEY")

if not api_key:
    raise RuntimeError("TAVILY_API_KEY environment variable is not set.")

tavily_client = TavilyClient(api_key=api_key)


@tool
def internet_search(
    query: str,
    max_results: int = 5,
    topic: Literal["general", "news", "finance"] = "general",
    include_raw_content: bool = False,
):
    """
    Search the internet using Tavily.

    Use this tool whenever you need:
    - Current events
    - Latest news
    - Recent information
    - Web search results
    - Information beyond the model's knowledge cutoff
    """
    return tavily_client.search(
        query=query,
        max_results=max_results,
        topic=topic,
        include_raw_content=include_raw_content,
    )


graph = create_react_agent(
    model=model,
    tools=[internet_search],
    prompt="""
You are an expert web search and information retrieval agent.

Responsibilities:
- Search the web for accurate and up-to-date information.
- Prefer authoritative and trustworthy sources.
- Summarize findings clearly.
- Include source URLs when available.
- Clearly distinguish verified facts from uncertainty.
"""
)