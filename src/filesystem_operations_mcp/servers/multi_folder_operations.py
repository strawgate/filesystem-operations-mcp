"""
MCP Server for performing folder operations.

This server provides tools for creating, listing contents, moving, deleting,
and emptying folders, with centralized exception handling.
"""

from fnmatch import fnmatch
from fastmcp import Context
from fastmcp.contrib.mcp_mixin import MCPMixin, mcp_tool
from pydantic import BaseModel, Field
from filesystem_operations_mcp.utils.exception_handling import handle_folder_errors
import os
import shutil
from logging import getLogger

logger = getLogger(__name__)

DEFAULT_SKIP_READ = [
    "**/.git/**",
    "**/.svn/**",
    "**/.mypy_cache/**",
    "**/.pytest_cache/**",
    "**/__pycache__/**",
    "*.pyc",
    "*.pyo",
    "*.pyd",
    "*.hg",
    "*.tox",
    "*.com",
    "*.class",
    "*.dll",
    "*.exe",
    "*.o",
    "*.so",
    "*.7z",
    "*.dmg",
    "*.gz",
    "*.iso",
    "*.jar",
    "*.rar",
    "*.tar",
    "*.zip",
    "*.msi",
    "*.sqlite",
    "*.DS_Store",
    "*.DS_Store?",
    "*._*",
    "*.Spotlight-V100",
    "*.Trashes",
    "*ehthumbs.db",
    "*Thumbs.db",
    "*desktop.ini",
    "*.bak",
    "*.swp",
    "*.swo",
    "*~",
    "*#",
]

class BaseMultiFileReadResult(BaseModel):
    file_path: str

class FileReadError(BaseMultiFileReadResult):
    """
    A model to represent an error that occurred while reading a file.
    
    Attributes:
        file_path (str): The path of the file that caused the error.
        error (str): The error message.
    """
    error: str

class FileReadSuccess(BaseModel):
    """
    A model to represent a successful file read operation.
    
    Attributes:
        file_path (str): The path of the file that was read.
        content (str): The content of the file.
    """
    file_path: str
    content: str

class FileReadSummary(BaseModel):
    """
    A model to summarize the results of reading files.
    
    Attributes:
        total_files (int): The total number of files read.
        successful_reads (int): The number of files read successfully.
        errors (list[FileReadError]): A list of errors encountered while reading files.
    """
    total_files: int = Field(default=0, description="Total number of files processed")
    skipped_files: int = Field(default=0, description="Number of files skipped due to exclusions")
    errors: list[FileReadError] = Field(default_factory=list, description="List of errors encountered while reading files")
    results: list[FileReadSuccess] = Field(default_factory=list, description="List of successfully read files with their content")


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
    async def contents(
        self, ctx: Context, folder_path: str, include: list[str], exclude: list[str], recurse: bool
    ) -> list:
        """
        Lists the contents of a folder.
         If you are listing items recursively, the include and exclude patterns will 
         apply to the relative path of the items. So to capture all files of a certain type
         in a folder and its subfolders, you would use a pattern like `**/*.txt` for `include`.

        Args:
            folder_path: The path of the folder to list.
            include: A list of glob patterns to include specific files, applies to the relative path.
            exclude: A list of glob pattern to exclude specific files, applies to the relative path.
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

                        included = any([fnmatch(rel_file, pat) for pat in include] if include else [True])

                        excluded = any([fnmatch(rel_file, pat) for pat in exclude])

                        if included and not excluded:
                            contents.append(rel_file)
            else:
                contents = os.listdir(folder_path)

            ctx.info(f"Contents of {folder_path} listed successfully")
            return contents

    @mcp_tool()
    async def read_all(
        self, ctx: Context, folder_path: str, include: list[str], exclude: list[str], recurse: bool, head: int = 0, tail: int = 0, bypass_default_exclusions: bool = False
    ) -> list[FileReadSuccess | FileReadError]:
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
            head: Number of lines to read from the start of each file (default is 0, meaning read all).
            tail: Number of lines to read from the end of each file (default is 0, meaning read all).
            bypass_default_exclusions: If True, skips the default exclusions for reading files.

        Returns:
            list[FileReadSuccess | FileReadError]: A list of results containing the file path and content or error.
        """
        async with handle_folder_errors(folder_path):
            files = await self.contents(ctx, folder_path, include, exclude, recurse)
            unfiltered_files = await self.contents(ctx, folder_path, [], [], recurse)

            results: list[FileReadSuccess] = []
            errors: list[FileReadError] = []

            for file in files:
                file_path = os.path.join(folder_path, file)

                if not bypass_default_exclusions:
                    # Check if the file matches any default exclusion patterns
                    if any(fnmatch(file, pat) for pat in DEFAULT_SKIP_READ):
                        ctx.debug(f"Skipping file due to default exclusion: {file_path}")
                        continue
                

                if not os.path.isfile(file_path):
                    continue
                try:
                    with open(file_path, "r", encoding="utf-8", errors="strict") as f:
                        if head > 0:
                            content = ''.join(f.readlines()[:head])
                        elif tail > 0:
                            f.seek(0, os.SEEK_END)
                            f.seek(max(0, f.tell() - tail), os.SEEK_SET)
                            content = f.read()
                        else:
                            content = f.read()
                    results.append(FileReadSuccess(file_path=file, content=content))
                    ctx.debug(f"File read successfully: {file_path}")
                except Exception as e:
                    errors.append(FileReadError(file_path=file, error=str(e)))
                    ctx.error(f"Error reading file {file_path}: {e}")

            return FileReadSummary(
                total_files=len(files),
                skipped_files=len(unfiltered_files) - len(files),
                errors=errors,
                results=results,
            )

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
