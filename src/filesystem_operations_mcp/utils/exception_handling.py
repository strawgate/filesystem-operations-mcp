"""
Utility functions for centralized exception handling.
"""

from contextlib import asynccontextmanager
from filesystem_operations_mcp.models.errors import (
    MCPFileOperationError,
    MCPFolderOperationError,
    MCPFileNotFoundError,
    MCPFolderNotFoundError,
)


@asynccontextmanager
async def handle_file_errors(path: str):
    """
    Async context manager to handle file operation exceptions.
    """
    try:
        yield
    except FileNotFoundError:
        raise MCPFileNotFoundError(path)
    except PermissionError as e:
        raise MCPFileOperationError(f"Permission denied: {e}", path)
    except Exception as e:
        raise MCPFileOperationError(f"An unexpected error occurred: {e}", path)


@asynccontextmanager
async def handle_folder_errors(path: str):
    """
    Async context manager to handle folder operation exceptions.
    """
    try:
        yield
    except FileNotFoundError:
        raise MCPFolderNotFoundError(path)
    except PermissionError as e:
        raise MCPFolderOperationError(f"Permission denied: {e}", path)
    except Exception as e:
        raise MCPFolderOperationError(f"An unexpected error occurred: {e}", path)
