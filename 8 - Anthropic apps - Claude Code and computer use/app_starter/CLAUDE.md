# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Run the MCP server
uv run main.py

# Run all tests
uv run pytest

# Run a single test
uv run pytest tests/test_document.py::TestBinaryDocumentToMarkdown::test_binary_document_to_markdown_with_docx
```

## Architecture

This is an MCP (Model Context Protocol) server that exposes document-processing tools to AI assistants.

**Entry point** — `main.py` creates a `FastMCP` instance and registers tools with `mcp.tool()(fn)`. Add new tools here after implementing them.

**Tools** — each file in `tools/` implements standalone Python functions. Tool parameters use `pydantic.Field` for descriptions (this is how MCP surfaces parameter docs to clients). Tool docstrings follow a specific format: one-line summary, detailed explanation, "When to use" section, and examples.

**`tools/document.py`** — wraps `markitdown` to convert binary document data (DOCX, PDF) to markdown. Takes raw `bytes` + a file extension string.

**`tools/math.py`** — example tool (`add`) showing the expected function signature pattern.

**Tests** — `tests/fixtures/` holds binary test files (`.docx`, `.pdf`). Tests read those files as bytes and pass them directly to tool functions — no MCP layer involved in testing.

## MCP Tool Definition

Tool functions must follow this signature pattern for MCP to correctly expose them:

```python
from pydantic import Field

def my_tool(
    param1: str = Field(description="Detailed description of this parameter"),
    param2: int = Field(description="Explain what this parameter does"),
) -> ReturnType:
    """One-line summary.

    Detailed explanation of what the tool does.

    When to use:
    - Scenario where this tool is appropriate
    - Another valid use case

    When NOT to use:
    - Scenario where another tool is better

    Examples:
    >>> my_tool("foo", 42)
    "expected output"
    """
```

Key rules:
- Every parameter needs a `Field(description=...)` — this is what the AI client sees when deciding which arguments to pass.
- The docstring drives how the AI decides *whether* to call the tool. Be explicit about when to use and when not to use it.
- Return type annotation is required; MCP uses it to validate and serialize the output.
- Functions must be pure and stateless — the MCP server may call them concurrently.

## Adding a new tool

1. Implement the function in `tools/<name>.py` using `Field` for parameter descriptions
2. Register it in `main.py`: `mcp.tool()(my_function)`
3. Add fixture files to `tests/fixtures/` if needed, write tests in `tests/`
