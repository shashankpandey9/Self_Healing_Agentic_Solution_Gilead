"""Shared base class that all self-healing agents extend.

No MCP layer is used - agents call their own local `tools.py` functions directly.
"""

from abc import ABC, abstractmethod


class AgentBase(ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @property
    @abstractmethod
    def description(self) -> str:
        ...

    @abstractmethod
    def invoke(self, state: dict) -> dict:
        """Run the agent against the shared workflow state and return the updated state."""
        ...
