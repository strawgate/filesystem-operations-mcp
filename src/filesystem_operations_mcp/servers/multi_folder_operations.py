"""
MCP Server for performing folder operations.

This server provides tools for creating, listing contents, moving, deleting,
and emptying folders, with centralized exception handling.
"""

from fastmcp import Context
from fastmcp.contrib.mcp_mixin import MCPMixin, mcp_tool
from filesystem_operations_mcp.utils.exception_handling import handle_folder_errors
import os
import shutil
from logging import getLogger

logger = getLogger(__name__)

class FolderOperations(MCPMixin):
    """
    This class provides MCP tools to manipulate folders.

    It includes methods for creating, listing contents, moving, deleting,
    and emptying folders, with integrated custom exception handling.
    """

    def __init__(self, denied_operations:list[str]=None):
        """
        Initializes the FolderOperations class.
        Args:
            denied_operations: A list of operations that should be denied.
        """
        if denied_operations is not None:
            for operation in denied_operations:
                if hasattr(self, operation):
                    delattr(FolderOperations, operation)
                    logger.info(f"Disabled folder tool: {operation}")

        super().__init__()

    @mcp_tool()
    async def create(self, ctx: Context, folder_path: str) -> bool:
        """
        Creates a folder at the specified path.

        Args:
            folder_path: The path where the folder should be created.

        Returns:
            bool: True if the folder was created successfully, False otherwise.
        """
        async with handle_folder_errors(folder_path):
            os.makedirs(folder_path, exist_ok=True)
            ctx.info(f"Folder created successfully at {folder_path}")
            return True

    @mcp_tool()
    async def contents(self, ctx: Context, folder_path: str) -> list:
        """
        Lists the contents of a folder.

        Args:
            folder_path: The path of the folder to list.

        Returns:
            list: A list of items in the folder.
        """
        async with handle_folder_errors(folder_path):
            contents = os.listdir(folder_path)
            ctx.info(f"Contents of {folder_path} listed successfully")
            return contents

    @mcp_tool()
    async def move(self, ctx: Context, source_path: str, destination_path: str) -> bool:
        """
        Moves a folder from source to destination.

        Args:
            source_path: The current path of the folder.
            destination_path: The new path where the folder should be moved.

        Returns:
            bool: True if the folder was moved successfully, False otherwise.
        """
        async with handle_folder_errors(source_path):
            os.rename(source_path, destination_path)
            ctx.info(f"Folder moved from {source_path} to {destination_path}")
            return True

    @mcp_tool()
    async def delete(
        self, ctx: Context, folder_path: str, recursive: bool = False
    ) -> bool:
        """
        Deletes a folder at the specified path.

        Args:
            folder_path: The path of the folder to delete.
            recursive: If True, deletes the folder and all its contents recursively.

        Returns:
            bool: True if the folder was deleted successfully, False otherwise.
        """
        async with handle_folder_errors(folder_path):
            if recursive:
                shutil.rmtree(folder_path)
            else:
                os.rmdir(folder_path)
            ctx.info(f"Folder deleted successfully at {folder_path}")
            return True
