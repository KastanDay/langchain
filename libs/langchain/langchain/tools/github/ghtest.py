import os

from langchain.agents import AgentType, initialize_agent
from langchain.agents.agent_toolkits.github.toolkit import GitHubToolkit
from langchain.chat_models import ChatOpenAI
from langchain.utilities.github import GitHubAPIWrapper


## ! ADD ENVIRONMENT VARIABLES HERE 

llm = ChatOpenAI(temperature=0, model="gpt-4-1106-preview")
github = GitHubAPIWrapper()
toolkit = GitHubToolkit.from_github_api_wrapper(github)
all_tools = toolkit.get_tools()

tools = []
for t in all_tools:
    if t.name == "Overview of existing files in Main branch":
        tools.append(t)

# STRUCTURED_CHAT includes args_schema for each tool, helps tool args parsing errors.
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)
print("Available tools:")
for tool in tools:
    print("\t" + tool.name)

agent.run(
    "You have the software engineering capabilities of a Google Principle engineer."
    "Please give me an overview of the files on my main branch."
    # " You are tasked with completing issues on a github repository. Please look at"
    # " the existing issues and complete them. For all github operations, the"
    # " action_input must be only the intended input string, do not include the"
    # " parameter name or other info, just the raw string input. For example,"
    # " if you want to create a file, the action_input should be the full file"
    # " path and contents, e.g. `some_dir/my_file.py\n\nmy file contents`."
)
