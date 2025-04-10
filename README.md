# Multi-File Reader MCP Server

This project provides a FastMCP server that exposes a tool to read the content of multiple files.

## Features

*   **`read_files` Tool:** Reads a list of specified file paths and returns their content or error information if a file cannot be read.
*   **Progress Reporting:** Reports progress as it reads through the list of files.
*   **Error Handling:** Handles common errors like `FileNotFoundError` and `PermissionError`.

## McpServer Usage
Simply add the following to your McpServer configuration
```
    "Read Many Files (GitHub)": {
      "command": "uvx",
      "args": [
        "https://github.com/strawgate/mcp-many-files.git"
      ],
      "alwaysAllow": [
        "read_files"
      ]
    },
```

## Development

1.  Clone the repository:
    ```bash
    # Replace with the actual repository URL
    git clone https://github.com/your-username/mcp-many-files.git
    cd mcp-many-files
    ```
2.  Create a virtual environment and install dependencies:
    ```bash
    uv venv
    source .venv/bin/activate # or .venv\Scripts\activate on Windows
    uv pip install -e .[dev] # Install in editable mode with dev dependencies
    ```
3.  Run the server locally for testing:
    ```bash
    python multi_file_reader_mcp.py
    # or using the installed script
    multi-file-reader-mcp
    ```
