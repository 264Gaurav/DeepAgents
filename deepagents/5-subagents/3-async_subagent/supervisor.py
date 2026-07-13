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

Delegate research to the researcher.

Delegate programming to the coder.

After launching an async task,
return immediately.

Never wait for completion.
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
    ],
)