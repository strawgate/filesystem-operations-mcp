import pytest
from filesystem_operations_mcp.models.settings import FilesystemOperationsMCPSettings, DEFAULT_SKIP_READ

def test_default_skip_read():
    """
    Test that DEFAULT_SKIP_READ contains the expected file patterns.
    """
    assert isinstance(DEFAULT_SKIP_READ, list)
    assert "**/.git/**" in DEFAULT_SKIP_READ
    assert "*.pyc" in DEFAULT_SKIP_READ
    assert "*.DS_Store" in DEFAULT_SKIP_READ
    assert "*~" in DEFAULT_SKIP_READ
    assert len(DEFAULT_SKIP_READ) > 0


def test_filesystem_operations_mcp_settings_defaults():
    """
    Test the default values of FilesystemOperationsMCPSettings.
    """
    settings = FilesystemOperationsMCPSettings()

    assert settings.mcp_transport == "stdio"
    assert settings.disabled_file_tools == []
    assert settings.disabled_folder_tools == []
    assert settings.read_file_exclusions == DEFAULT_SKIP_READ


def test_filesystem_operations_mcp_settings_custom_values():
    """
    Test that FilesystemOperationsMCPSettings can be initialized with custom values.
    """
    custom_skip_read = ["*.log", "*.tmp"]
    settings = FilesystemOperationsMCPSettings(
        mcp_transport="sse",
        disabled_file_tools=["tool1", "tool2"],
        disabled_folder_tools=["folder_tool1"],
        read_file_exclusions=custom_skip_read,
    )

    assert settings.mcp_transport == "sse"
    assert settings.disabled_file_tools == ["tool1", "tool2"]
    assert settings.disabled_folder_tools == ["folder_tool1"]
    assert settings.read_file_exclusions == custom_skip_read