"""
This tool allows agents to interact with the pygithub library
and operate on a GitHub repository.

To use this tool, you must first set as environment variables:
    GITHUB_API_TOKEN
    GITHUB_REPOSITORY -> format: {owner}/{repo}

"""
import json
from typing import Optional, Type

from langchain.callbacks.manager import CallbackManagerForToolRun
from langchain.pydantic_v1 import Field
from langchain.tools.base import BaseTool
from langchain.utilities.github import GitHubAPIWrapper
from pydantic import BaseModel

class GitHubAction(BaseTool):
    """Tool for interacting with the GitHub API."""

    api_wrapper: GitHubAPIWrapper = Field(default_factory=GitHubAPIWrapper)
    mode: str
    name: str = ""
    description: str = ""
    args_schema: Optional[Type[BaseModel]] = None

    def _run(
        self,
        instructions: Optional[str],
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the GitHub API to run an operation."""

        if not instructions or instructions == "{}":
            # Catch empty input that GPT-4 likes to send.
            instructions = ""

        # Catch common formatting problems. Most commonly: instructions = '{"issue_number": "5"}'
        try:
            instructions_dict = json.loads(instructions)
        except (TypeError, json.JSONDecodeError):
            instructions_dict = None

        if isinstance(instructions_dict, dict):
            instructions = list(instructions_dict.values())[0]

        return self.api_wrapper.run(self.mode, instructions)
