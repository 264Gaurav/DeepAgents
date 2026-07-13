import logfire
import observability

logfire.configure(service_name="deepagents")

logfire.info("Hello from Logfire!")

print("Done")