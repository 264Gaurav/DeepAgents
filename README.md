# DeepAgents
DeepAgents core understandings and developement of advanced ai agents. With memory, skill, tools, subagents, multiagents flow etc.


## Project setup and start:
1. ``` uv init deepagents``` //Initialize the Project
2. ``` cd deepagents```
3. ``` uv venv```  // Lock and Setup the Environment
4. ``` uv run main.py``` //run the project (optional - make sure correct setup is done)

- Now, from the correct path: 
5. Create a requirements.txt file with correct module and other requirements.
6. ```uv add -r requirements.txt``` //migrate the requirements.
7. ``` uv pip install -r requirements.txt``` //install the dependencies and required modules/lib.
 
----------
## Deep agent selection over langchain and langgraph or other frameworks/sdk

![Deep agent selection over langchain and langgraph or other frameworks/sdk](assets/image.png)

-----------
## Deep agent Filesystem Tools - Backend

![Deep agent Filesystem Tools - Backend](assets/backend.png)

---
## Deep agent backend configured with postgres DB - 
### For CompositeStore and StoreBackend : to maintain chat history and memory across different threads in persistence manner.

![PG_DB](assets/pg_deep_agent.png)


## Deepagent Subagents:

A deep agent can create subagents to delegate work. You can specify custom subagents in the subagents parameter. Subagents are useful for context quarantine (keeping the main agent’s context clean) and for providing specialized instructions.


![Subagent](assets/subagents.png)

