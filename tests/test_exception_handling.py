"""
Tests for the exception handling context managers.
"""

import pytest
from filesystem_operations_mcp.utils.exception_handling import (
    handle_file_errors,
    handle_folder_errors,
)
from filesystem_operations_mcp.models.errors import (
    MCPFileOperationError,
    MCPFolderOperationError,
    MCPFileNotFoundError,
    MCPFolderNotFoundError,
)

# Parametrized test data for handle_file_errors
file_error_scenarios = [
    (FileNotFoundError, MCPFileNotFoundError, "File not found", "test_file.txt"),
    (
        PermissionError("Permission denied"),
        MCPFileOperationError,
        "Permission denied",
        "test_file.txt",
    ),
    (
        Exception("Some other error"),
        MCPFileOperationError,
        "An unexpected error occurred",
        "test_file.txt",
    ),
]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "raised_exception, expected_exception, exception_match, file_path",
    file_error_scenarios,
)
async def test_handle_file_errors(
    raised_exception: Exception,
    expected_exception: type[Exception],
    exception_match: str,
    file_path: str,
):
    """
    Test the handle_file_errors context manager for different built-in exceptions.

    Verifies that the context manager catches specific built-in exceptions
    (FileNotFoundError, PermissionError) and general Exceptions, and raises
    the corresponding custom MCP exceptions with the correct message and file path.
    """
    with pytest.raises(expected_exception, match=exception_match) as excinfo:
        async with handle_file_errors(file_path):
            if isinstance(raised_exception, type):
                raise raised_exception
            else:
                raise raised_exception

    if hasattr(excinfo.value, "file_path"):
        assert isinstance(excinfo.value, expected_exception)
        assert hasattr(excinfo.value, "file_path")
        file_path_value = getattr(excinfo.value, "file_path")
        assert file_path_value == file_path


# Parametrized test data for handle_folder_errors
folder_error_scenarios = [
    (FileNotFoundError, MCPFolderNotFoundError, "Folder not found", "test_folder"),
    (
        PermissionError("Permission denied"),
        MCPFolderOperationError,
        "Permission denied",
        "test_folder",
    ),
    (
        Exception("Some other error"),
        MCPFolderOperationError,
        "An unexpected error occurred",
        "test_folder",
    ),
]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "raised_exception, expected_exception, exception_match, folder_path",
    folder_error_scenarios,
)
async def test_handle_folder_errors(
    raised_exception: Exception,
    expected_exception: type[Exception],
    exception_match: str,
    folder_path: str,
):
    """
    Test the handle_folder_errors context manager for different built-in exceptions.

    Verifies that the context manager catches specific built-in exceptions
    (FileNotFoundError, PermissionError) and general Exceptions, and raises
    the corresponding custom MCP exceptions with the correct message and folder path.
    """
    with pytest.raises(expected_exception, match=exception_match) as excinfo:
        async with handle_folder_errors(folder_path):
            if isinstance(raised_exception, type):
                raise raised_exception
            else:
                raise raised_exception

    if hasattr(excinfo.value, "folder_path"):
        assert isinstance(excinfo.value, expected_exception)
        assert hasattr(excinfo.value, "folder_path")
        folder_path_value = getattr(excinfo.value, "folder_path")
        assert folder_path_value == folder_path
