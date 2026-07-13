from dotenv import load_dotenv
import logfire

load_dotenv()

logfire.configure(
    service_name="deepagents"
)