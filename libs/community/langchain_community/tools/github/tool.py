"""
This tool allows agents to interact with the pygithub library
and operate on a GitHub repository.

To use this tool, you must first set as environment variables:
    GITHUB_API_TOKEN
    GITHUB_REPOSITORY -> format: {owner}/{repo}

"""
import json
from typing import Optional, Type, Union

from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.tools import BaseTool

from langchain_community.utilities.github import GitHubAPIWrapper


class GitHubAction(BaseTool):
    """Tool for interacting with the GitHub API."""

    api_wrapper: GitHubAPIWrapper = Field(default_factory=GitHubAPIWrapper)
    mode: str
    name: str = ""
    description: str = ""
    args_schema: Optional[Union[Type[BaseModel], BaseModel]] = None

    def _run(
        self,
        instructions: Optional[str] = "",
        run_manager: Optional[CallbackManagerForToolRun] = None,
        **kwargs,
    ) -> str:
        """Use the GitHub API to run an operation."""
        # print(f"In GitHubAction._run --- Instructions: {instructions}")
        # print(f"In GitHubAction._run --- self.mode: {self.mode}")
        # print(f"In GitHubAction._run --- name: {self.name}")
        # print(f"In GitHubAction._run --- args_schema: {self.args_schema}")
        # print(f"In GitHubAction._run --- kwargs: {kwargs}")
        # print(f"In GitHubAction._run --- type kwargs: {type(kwargs)}")
        # print(f"In GitHubAction._run --- {list(kwargs.values()) = }")

        # Catch improper formatting of args, like this improper: instructions = "{'formatted_filepath': 'Report_WholeBrain/Report_Antonson_WholeBrain_2022Mar.Rmd'}"
        # proper would be: instructions = 'Report_WholeBrain/Report_Antonson_WholeBrain_2022Mar.Rmd'
        if kwargs and kwargs.values() and list(kwargs.values())[0] is not None:
            print(f"In GitHubAction._run --- {list(kwargs.values())[0] = }")
            instructions = list(kwargs.values())[0]


        return self.api_wrapper.run(self.mode, instructions)
