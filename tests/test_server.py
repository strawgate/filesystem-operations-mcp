"""
Tests for the MCP server setup and configuration.
"""

from filesystem_operations_mcp.models.settings import FilesystemOperationsMCPSettings
from filesystem_operations_mcp.servers.multi_file_operations import FileOperations
from filesystem_operations_mcp.servers.multi_folder_operations import FolderOperations


def test_file_tool_exclusion(monkeypatch):
    """
    Test that file tools are correctly excluded based on DISABLED_FILE_TOOLS environment variable.
    """

    monkeypatch.setenv("DISABLED_FILE_TOOLS", '["delete","copy"]')

    settings = FilesystemOperationsMCPSettings()

    filtered_file_operations = FileOperations(
        denied_operations=settings.disabled_file_tools
    )

    assert hasattr(filtered_file_operations, "move"), (
        "Expected 'move' tool to be available"
    )
    assert not hasattr(filtered_file_operations, "delete"), (
        "Expected 'delete' tool to be disabled"
    )
    assert not hasattr(filtered_file_operations, "copy"), (
        "Expected 'copy' tool to be disabled"
    )
    assert hasattr(filtered_file_operations, "create"), (
        "Expected 'create' tool to be available"
    )


def test_folder_tool_exclusion(monkeypatch):
    """
    Test that folder tools are correctly excluded based on DISABLED_FOLDER_TOOLS environment variable.
    """

    monkeypatch.setenv("DISABLED_FOLDER_TOOLS", '["delete","copy"]')

    settings = FilesystemOperationsMCPSettings()

    filter_folder_operations = FolderOperations(
        denied_operations=settings.disabled_folder_tools
    )

    assert hasattr(filter_folder_operations, "move"), (
        "Expected 'move' tool to be available"
    )
    assert not hasattr(filter_folder_operations, "delete"), (
        "Expected 'delete' tool to be disabled"
    )
    assert not hasattr(filter_folder_operations, "copy"), (
        "Expected 'copy' tool to be disabled"
    )
    assert hasattr(filter_folder_operations, "create"), (
        "Expected 'create' tool to be available"
    )
