"""
Settings models for the Bulk Filesystem Operations MCP server.
"""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class FilesystemOperationsMCPSettings(BaseSettings):
    """
    Configuration settings for the Bulk Filesystem Operations MCP server.

    These settings can be loaded from environment variables or a .env file.
    """

    model_config = SettingsConfigDict()
    mcp_transport: str = Field(
        default="stdio",
        alias="mcp_transport",
        description="The transport protocol for the MCP server, e.g., 'stdio', 'sse",
    )
    disabled_file_tools: List[str] = Field(
        default_factory=list,
        alias="disabled_file_tools",
        description="List of disabled file tools provided by DISABLED_FILE_TOOLS environment variable.",
    )
    disabled_folder_tools: List[str] = Field(
        default_factory=list,
        alias="disabled_folder_tools",
        description="List of disabled folder tools provided by DISABLED_FOLDER_TOOLS environment variable.",
    )
