# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Create and activate virtual environment
uv venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # macOS/Linux

# Install package in development mode
uv pip install -e .

# Start the MCP server
uv run main.py

# Run all tests
uv run pytest

# Run a single test
uv run pytest tests/test_document.py::test_binary_document_to_markdown_with_docx
```

## Architecture

This is an MCP (Model Context Protocol) server built with `FastMCP`. Tools defined in the `tools/` package are registered with the server in `main.py` and exposed to AI assistants over the MCP protocol.

**Registration pattern** — tools are registered in `main.py` using the decorator-call form:
```python
mcp.tool()(my_function)
```

**`tools/` package** — each module exports plain Python functions. Two tools currently exist:
- `tools/math.py` — `add(a, b)`: simple example tool, currently registered
- `tools/document.py` — `binary_document_to_markdown(binary_data, file_type)`: converts DOCX/PDF bytes to markdown via `markitdown`; exists but is **not yet registered** in `main.py`

**Tests** live in `tests/` with binary fixture files in `tests/fixtures/` (`.docx`, `.pdf`) used for integration-style tests of document conversion.

## Defining MCP Tools

Tools are Python functions using Pydantic `Field` for parameter documentation. The docstring becomes the tool description presented to the AI assistant, so it should be thorough.

```python
from pydantic import Field

def my_tool(
    param1: str = Field(description="What this parameter is and valid values"),
    param2: int = Field(description="What this parameter controls")
) -> ReturnType:
    """One-line summary.

    Detailed explanation of what the tool does.

    When to use: describe the ideal use case.
    When NOT to use: describe cases this tool cannot handle.

    Example:
        Input: param1="foo", param2=42
        Output: <expected result>
    """
    # implementation
```

After defining the function, register it in `main.py`:
```python
from tools.my_module import my_tool
mcp.tool()(my_tool)
```
