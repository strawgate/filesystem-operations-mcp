"""
Main entry point for the Bulk Filesystem Operations MCP Server.

This server provides tools for performing file and folder operations
through the Model Context Protocol (MCP). It registers specialized
servers for file and folder operations and a bulk tool caller.
"""

from fastmcp import FastMCP
from fastmcp.contrib.bulk_tool_caller import BulkToolCaller

from logging import getLogger, Logger

from filesystem_operations_mcp.models.settings import (
    FilesystemOperationsMCPSettings,
)
from filesystem_operations_mcp.servers.multi_file_operations import FileOperations
from filesystem_operations_mcp.servers.multi_folder_operations import (
    FolderOperations,
)

logger: Logger = getLogger(__name__)


def main():
    """
    Entry point for running the Bulk Filesystem Operations MCP server.

    Initializes the root MCP server, registers the FileOperations and
    FolderOperations servers as tools, registers the BulkToolCaller,
    mounts the sub-servers, and starts the main server loop.
    Disabled tools are removed based on settings.
    """

    settings = FilesystemOperationsMCPSettings()  # Gather settings from the environment

    root_mcp = FastMCP(
        "FilesystemOperationsMCP",
        dependencies=["fastmcp"],
    )

    file_mcp = FastMCP(
        "FileOperations",
        dependencies=["fastmcp"],
    )

    folder_mcp = FastMCP(
        "FolderOperations",
        dependencies=["fastmcp"],
    )

    # Register the tools for file manipulation, disabling any specified in settings
    file_operations = FileOperations(denied_operations=settings.disabled_file_tools)
    file_operations.register_all(file_mcp)

    # Register the tools for folder manipulation, disabling any specified in settings
    folder_operations = FolderOperations(
        denied_operations=settings.disabled_folder_tools,
        read_file_exclusions=settings.read_file_exclusions,
        list_folder_exclusions=settings.list_folder_exclusions,
    )
    folder_operations.register_all(folder_mcp)

    # Register the bulk tool caller
    bulk_tool_caller = BulkToolCaller()
    bulk_tool_caller.register_all(root_mcp)

    # Mount the MCP servers
    root_mcp.mount("file", file_mcp)
    root_mcp.mount("folder", folder_mcp)

    # Start the MCP server
    root_mcp.run(transport=settings.mcp_transport)


# Allow running the server directly for testing or advanced use cases
if __name__ == "__main__":
    main()
