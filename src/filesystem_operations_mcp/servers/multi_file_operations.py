"""
MCP Server for performing file operations.

This server provides tools for reading, creating, appending, erasing, moving,
and deleting files, with centralized exception handling.
"""

from logging import getLogger
import os
from fastmcp import Context
from fastmcp.contrib.mcp_mixin import MCPMixin, mcp_tool
from filesystem_operations_mcp.utils.exception_handling import handle_file_errors

logger = getLogger(__name__)


class FileOperations(MCPMixin):
    """
    This class provides MCP tools to manipulate files.

    It includes methods for reading, creating, appending, erasing, moving,
    and deleting files, with integrated custom exception handling.
    """

    def __init__(self, denied_operations: list[str] = None):
        """
        Initializes the FileOperations class.
        Args:
            denied_operations: A list of operations that should be denied.
        """
        if denied_operations is not None:
            for operation in denied_operations:
                if hasattr(self, operation):
                    delattr(FileOperations, operation)
                    logger.info(f"Disabled file tool: {operation}")

        super().__init__()

    @mcp_tool()
    async def read(self, ctx: Context, file_path: str) -> str:
        """
        Reads the content of a file at the specified path.

        Args:
            file_path: The path of the file to read.

        Returns:
            str: The content of the file.
        """
        async with handle_file_errors(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            ctx.info(f"File read successfully from {file_path}")
            return content

    @mcp_tool()
    async def create(self, ctx: Context, file_path: str, content: str) -> bool:
        """
        Creates a file with the specified content.

        Args:
            file_path: The path where the file should be created.
            content: The content to write into the file.

        Returns:
            bool: True if the file was created successfully, False otherwise.
        """
        async with handle_file_errors(file_path):
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            ctx.info(f"File created successfully at {file_path}")
            return True

    @mcp_tool()
    async def append(self, ctx: Context, file_path: str, content: str) -> bool:
        """
        Appends content to an existing file.

        Args:
            file_path: The path of the file to append content to.
            content: The content to append to the file.

        Returns:
            bool: True if the content was appended successfully, False otherwise.
        """
        async with handle_file_errors(file_path):
            with open(file_path, "a", encoding="utf-8") as f:
                f.write(content)
            ctx.info(f"Content appended successfully to {file_path}")
            return True

    @mcp_tool()
    async def erase(self, ctx: Context, file_path: str) -> bool:
        """
        Erases the content of a file.

        Args:
            file_path: The path of the file to erase.

        Returns:
            bool: True if the file was erased successfully, False otherwise.
        """
        async with handle_file_errors(file_path):
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("")
            ctx.info(f"File content erased successfully at {file_path}")
            return True

    @mcp_tool()
    async def move(self, ctx: Context, source_path: str, destination_path: str) -> bool:
        """
        Moves a file from source to destination.

        Args:
            source_path: The current path of the file.
            destination_path: The new path where the file should be moved.

        Returns:
            bool: True if the file was moved successfully, False otherwise.
        """
        async with handle_file_errors(source_path):
            os.rename(source_path, destination_path)
            ctx.info(f"File moved from {source_path} to {destination_path}")
            return True

    @mcp_tool()
    async def delete(self, ctx: Context, file_path: str) -> bool:
        """
        Deletes a file at the specified path.

        Args:
            file_path: The path of the file to delete.

        Returns:
            bool: True if the file was deleted successfully, False otherwise.
        """
        async with handle_file_errors(file_path):
            os.remove(file_path)
            ctx.info(f"File deleted successfully at {file_path}")
            return True
