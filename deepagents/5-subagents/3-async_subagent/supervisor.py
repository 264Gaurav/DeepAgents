import observability

from deepagents import (
    AsyncSubAgent,
    create_deep_agent,
)

from langchain.chat_models import init_chat_model
from model import model

graph = create_deep_agent(
    model=model,
    system_prompt="""
You are an intelligent supervisor.

Your responsibilities:

- Delegate research tasks to the Researcher.
- Delegate programming tasks to the Coder.
- Delegate internet searches to the Web Search agent.
- Choose the most appropriate subagent based on the user's request.
- Launch long-running work asynchronously whenever possible.
- Never wait for async task completion.
- After launching an async task, immediately return control to the user.
- Do not call check_async_task immediately after launching.
""",
    subagents=[
        AsyncSubAgent(
            name="researcher",
            description="Researches information",
            graph_id="researcher",
        ),
        AsyncSubAgent(
            name="coder",
            description="Writes code",
            graph_id="coder",
        ),
        AsyncSubAgent(
            name="web_search",
            description="Searches the web for latest information",
            graph_id="web_search",
        ),
    ],
)