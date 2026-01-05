"""LLM port interface for AI/ML operations.

This module defines the abstract interface (port) for LLM interactions.
Infrastructure adapters (e.g., Bedrock) implement this interface.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class PromptTemplate:
    """Immutable prompt template following value object pattern.

    Attributes:
        system: The system prompt defining the AI's role and behavior.
        user_template: Template string for user messages with placeholders.
        max_tokens: Maximum tokens in the response.
        temperature: Sampling temperature for response generation.
    """

    system: str
    user_template: str
    max_tokens: int = 1024
    temperature: float = 0.7

    def render(self, **kwargs) -> str:
        """Render user template with provided variables.

        Args:
            **kwargs: Variables to substitute in the template.

        Returns:
            Rendered user message string.
        """
        return self.user_template.format(**kwargs)


class LLMPort(ABC):
    """Abstract interface for LLM interactions.

    This port defines the contract for LLM operations, keeping the application
    layer independent of specific LLM providers (Bedrock, OpenAI, etc.).
    """

    @abstractmethod
    async def invoke(self, prompt: PromptTemplate, user_input: str) -> str:
        """Invoke LLM with a prompt template and user input.

        Args:
            prompt: The prompt template containing system and user templates.
            user_input: The user's input message.

        Returns:
            The LLM's response as a string.
        """
        pass

    @abstractmethod
    async def invoke_with_history(self, prompt: PromptTemplate, messages: list[dict], user_input: str) -> str:
        """Invoke LLM with conversation history.

        Args:
            prompt: The prompt template containing system and user templates.
            messages: List of previous messages in the conversation.
                Each message should have 'role' and 'content' keys.
            user_input: The current user input message.

        Returns:
            The LLM's response as a string.
        """
        pass
