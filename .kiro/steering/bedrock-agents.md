# Bedrock Agents & Prompt Engineering

## Overview

Chatbots and AI agents use Amazon Bedrock. Prompts are treated as first-class citizens following hexagonal architecture.

## Directory Structure

```
src/
├── domain/
│   └── prompts/              # Prompt templates (domain layer)
│       ├── base.py           # Base prompt classes
│       ├── system_prompts/   # System prompt definitions
│       └── templates/        # Reusable prompt templates
├── application/
│   └── interfaces/
│       └── llm_port.py       # LLM abstraction (port)
└── infrastructure/
    └── external/
        └── bedrock/          # Bedrock adapter implementation
            ├── client.py     # Bedrock client wrapper
            └── adapter.py    # LLM port implementation
```

## Prompt as Domain Objects

```python
from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass(frozen=True)
class PromptTemplate:
    """Immutable prompt template following value object pattern."""

    system: str
    user_template: str
    max_tokens: int = 1024
    temperature: float = 0.7

    def render(self, **kwargs) -> str:
        """Render user template with provided variables."""
        return self.user_template.format(**kwargs)
```

## LLM Port (Application Layer)

```python
from abc import ABC, abstractmethod
from domain.prompts.base import PromptTemplate


class LLMPort(ABC):
    """Port for LLM interactions - keeps domain independent of Bedrock."""

    @abstractmethod
    async def invoke(self, prompt: PromptTemplate, user_input: str) -> str:
        """Invoke LLM with prompt template."""
        pass

    @abstractmethod
    async def invoke_with_history(
        self, prompt: PromptTemplate, messages: list[dict], user_input: str
    ) -> str:
        """Invoke LLM with conversation history."""
        pass
```
