# Bulk Filesystem Operations MCP Server

This project provides a FastMCP server that exposes tools for performing bulk file and folder operations. It includes centralized exception handling for filesystem operations.

## Available Tools

The server provides the following tools, categorized by their functionality:

*   **`call_tool_bulk`**: Call a single tool registered on this MCP server multiple times with a single request. Useful for speeding up what would otherwise take several individual tool calls.

*   **`call_tools_bulk`**: Call multiple tools registered on this MCP server in a single request. Each call can be for a different tool and can include different arguments. Useful for speeding up what would otherwise take several individual tool calls.

To add bulk tools to your FastMCP server, see https://github.com/jlowin/fastmcp/pull/215

### File Operations Tools (`file` server)

These tools are available under the `file` server namespace.

*   **`read`**: Reads the content of a file at the specified path
*   **`create`**: Creates a file with the specified content
*   **`append`**: Appends content to an existing file
*   **`erase`**: Erases the content of a file
*   **`move`**: Moves a file from source to destination
*   **`delete`**: Deletes a file at the specified path

### Folder Operations Tools (`folder` server)

These tools are available under the `folder` server namespace.

*   **`create`**: Creates a folder at the specified path
*   **`contents`**: Lists the contents of a folder
*   **`move`**: Moves a folder from source to destination
*   **`delete`**: Deletes a folder at the specified path
*   **`empty`**: Empties a folder by deleting all its contents

### Disabling Tools
You can disable specific file tools by setting the `DISABLE_FILE_TOOLS` to an array of tool names you want to disable. For example, to disable the `file_read` tool, set `DISABLE_FILE_TOOLS=["file_read"]`.

You can disable specific folder tools by setting the `DISABLE_FOLDER_TOOLS` to an array of tool names you want to disable. For example, to disable the `folder_create` tool, set `DISABLE_FOLDER_TOOLS=["folder_create"]`.

Bulk tools cannot currently be disabled.

## VS Code McpServer Usage
1. Open the command palette (Ctrl+Shift+P or Cmd+Shift+P).
2. Type "Settings" and select "Preferences: Open User Settings (JSON)".
3. Add the following MCP Server configuration

```json
{
    "mcp": {
        "servers": {
            "Filesystem Operations": {
                "command": "uvx",
                "args": [
                    "https://github.com/strawgate/mcp-many-files.git"
                ]
            }
        }
    }
}
```

## Roo Code / Cline McpServer Usage
Simply add the following to your McpServer configuration. Edit the AlwaysAllow list to include the tools you want to use without confirmation.

```
    "Filesystem Operations": {
      "command": "uvx",
      "args": [
        "https://github.com/strawgate/mcp-many-files.git"
      ],
      "alwaysAllow": [
        "file_read",
        "file_create",
        "file_append",
        "file_erase",
        "file_move",
        "file_delete",
        "folder_create",
        "folder_contents",
        "folder_move",
        "folder_delete",
        "folder_empty",
        "call_tool_bulk",
        "call_tools_bulk"
      ]
    },
```

## Development

1.  Clone the repository:
    ```bash
    # Replace with the actual repository URL
    git clone https://github.com/strawgate/filesystem-operations-mcp.git
    cd filesystem-operations-mcp
    ```
2.  Create a virtual environment and install dependencies:
    ```bash
    uv venv
    source .venv/bin/activate
    uv sync --extra dev
    ```
3.  Run the server locally for testing:
    ```bash
    python -m filesystem-operations-mcp.server
    # or using the installed script
    filesystem-operations-mcp
    ```

You can also debug with vscode via the built in debug launch configuration. To point your MCP Client to this local server, use the following MCP server configuration:
```json
"filesystem_operations_mcp": {
  "url": "http://localhost:8000/sse",
  "disabled": true,
  "autoApprove": [],
  "timeout": 30,
  "alwaysAllow": []
}

You can also set your uvx command to point to a branch on the repository via `"git+https://github.com/strawgate/filesystem-operations-mcp@branch-name"`.