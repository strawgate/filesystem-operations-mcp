"""
MCP Server for performing folder operations.

This server provides tools for creating, listing contents, moving, deleting,
and emptying folders, with centralized exception handling.
"""

from fnmatch import fnmatch
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

    def __init__(self, denied_operations: list[str] = None):
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
    async def list(
        self, ctx: Context, folder_path: str, include: str, exclude: str, recurse: bool
    ) -> list:
        """
        Lists the contents of a folder.
         If you are listing items recursively, the include and exclude patterns will 
         apply to the relative path of the items. So to capture all files of a certain type
         in a folder and its subfolders, you would use a pattern like `**/*.txt` for `include`.

        Args:
            folder_path: The path of the folder to list.
            include: A glob pattern to include specific files, applies to the relative path.
            exclude: A glob pattern to exclude specific files, applies to the relative path.
            recurse: If True, lists contents recursively.

        Returns:
            list: A list of items in the folder.
        """
        async with handle_folder_errors(folder_path):
            contents = []

            if recurse:
                for dir_, _, files in os.walk(folder_path):
                    for file_name in files:

                        rel_dir = os.path.relpath(dir_, folder_path)
                        rel_file = os.path.join(rel_dir, file_name)

                        if include and not fnmatch(rel_file, include):
                            continue
                        if exclude and fnmatch(rel_file, exclude):
                            continue

                        contents.append(rel_file)
            else:
                contents = os.listdir(folder_path)

            ctx.info(f"Contents of {folder_path} listed successfully")
            return contents

    @mcp_tool()
    async def read_all(
        self, ctx: Context, folder_path: str, include: str, exclude: str, recurse: bool
    ) -> dict[str, str]:
        """
        Provides the full contents (every character) of every file in a folder.
         If you are listing items recursively, the include and exclude patterns will 
         apply to the relative path of the items. So to capture all files of a certain type
         in a folder and its subfolders, you would use a pattern like `**/*.txt` for `include`.

        Args:
            folder_path: The path of the folder to list.
            include: A glob pattern to include specific files, applies to the relative path.
            exclude: A glob pattern to exclude specific files, applies to the relative path.
            recurse: If True, reads files recursively.

        Returns:
            dict[str, str]: A dictionary with file paths as keys and their contents as values.
        """
        async with handle_folder_errors(folder_path):
            files = await self.list(ctx, folder_path, include, exclude, recurse)

            file_with_contents = {}

            for file in files:
                file_path = os.path.join(folder_path, file)
                if not os.path.isfile(file_path):
                    continue

                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    file_with_contents[file] = content

            ctx.info(f"Contents of all files in {folder_path} read successfully")
            return file_with_contents

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
