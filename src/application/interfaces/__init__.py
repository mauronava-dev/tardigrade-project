"""Port definitions (abstract interfaces)."""

from src.application.interfaces.llm_port import LLMPort, PromptTemplate
from src.application.interfaces.repository_port import UserRepositoryPort

__all__ = ["UserRepositoryPort", "LLMPort", "PromptTemplate"]
