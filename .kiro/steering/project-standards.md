# Tardigrade Project Standards

## Language and Naming Conventions

- All code, comments, and documentation must be written in English
- Use `snake_case` for variables, functions, and file names
- Use `PascalCase` for class names
- Use `UPPER_SNAKE_CASE` for constants

## Code Quality Requirements

- Maximum line length: 120 characters
- Indentation: 4 spaces
- String quotes: double quotes (`"`)
- All functions, classes, and modules must have docstrings
- Follow single responsibility principle for functions
- Apply hexagonal architecture patterns
- Prefer functional programming paradigm where appropriate

## Testing Requirements

- Create unit tests for every new module or significant functionality
- Maintain minimum 80% code coverage
- Use pytest as the testing framework
- Place tests in a `tests/` directory mirroring the source structure

## Documentation

- Use Google-style docstrings format
- Document all public functions, classes, and modules
- Include type hints in function signatures

## Example Function Template

```python
def calculate_total_price(items: list[dict], tax_rate: float) -> float:
    """
    Calculate the total price including tax for a list of items.

    Args:
        items: List of item dictionaries with 'price' and 'quantity' keys.
        tax_rate: Tax rate as a decimal (e.g., 0.16 for 16%).

    Returns:
        Total price including tax.

    Raises:
        ValueError: If tax_rate is negative.
    """
    if tax_rate < 0:
        raise ValueError("Tax rate cannot be negative")

    subtotal = sum(item["price"] * item["quantity"] for item in items)
    return subtotal * (1 + tax_rate)
```
