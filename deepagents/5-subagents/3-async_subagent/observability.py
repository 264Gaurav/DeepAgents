import os
from dotenv import load_dotenv
import logfire

load_dotenv()

# Must be set BEFORE importing LangChain/LangGraph
os.environ["LANGSMITH_OTEL_ENABLED"] = "true"
os.environ["LANGSMITH_OTEL_ONLY"] = "true"
os.environ["LANGSMITH_TRACING"] = "true"




def scrubbing_callback(m: logfire.ScrubMatch):
    if m.path == ('attributes', 'langsmith.metadata.langgraph_auth_user_id'):
        return m.value

    if (
        m.path == ('attributes', 'gen_ai.prompt', 'messages', 8, 'content')
        and m.pattern_match.group(0) == 'auth'
    ):
        return m.value

    if (
        m.path == ('attributes', 'gen_ai.prompt', 'messages', 9, 'content')
        and m.pattern_match.group(0) == 'auth'
    ):
        return m.value

    if (
        m.path == ('attributes', 'all_messages_events', 8, 'content')
        and m.pattern_match.group(0) == 'auth'
    ):
        return m.value

    if (
        m.path == ('attributes', 'all_messages_events', 9, 'content')
        and m.pattern_match.group(0) == 'auth'
    ):
        return m.value
    
    
logfire.configure(
    service_name="deepagents",
    scrubbing=logfire.ScrubbingOptions(
        callback=scrubbing_callback
    )
)