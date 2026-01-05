# Prompt Engineering Standards

## Prompt Design Principles

1. Single Responsibility: Each prompt handles one specific task
2. Composability: Build complex prompts from smaller, tested components
3. Testability: Prompts must be unit testable with expected outputs
4. Version Control: Track prompt changes like code changes

## System Prompt Structure

```python
SYSTEM_PROMPT = """
Role: {role_definition}

Context: {context_description}

Instructions:
- {instruction_1}
- {instruction_2}

Constraints:
- {constraint_1}
- {constraint_2}

Output Format: {expected_format}
"""
```

## Prompt Template Example

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class CustomerSupportPrompt:
    """Customer support chatbot prompt."""

    system: str = """
Role: You are a helpful customer support assistant for {company_name}.

Context: You help customers with product inquiries, order status, and general questions.

Instructions:
- Be polite and professional
- Provide accurate information based on available data
- Escalate to human agent when unable to resolve

Constraints:
- Never share sensitive customer data
- Do not make promises about refunds without verification
- Stay within scope of customer support

Output Format: Respond in clear, concise paragraphs.
"""

    user_template: str = "Customer query: {query}\nOrder context: {order_context}"
```

## Testing Prompts

```python
import pytest
from domain.prompts.customer_support import CustomerSupportPrompt


def test_prompt_renders_correctly():
    """Test prompt template rendering."""
    prompt = CustomerSupportPrompt()
    rendered = prompt.user_template.format(
        query="Where is my order?",
        order_context="Order #123, shipped 2 days ago"
    )
    assert "Where is my order?" in rendered
    assert "Order #123" in rendered
```
