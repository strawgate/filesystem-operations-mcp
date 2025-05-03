"""
Settings models for the Bulk Filesystem Operations MCP server.
"""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

DEFAULT_SKIP_LIST = [
    "**/.?*/**",
    ".?*/**", # exclude hidden folders
    "**/.?*", # exclude hidden files
    "**/.git/**",
    ".git/*",
    "**/.svn/**",
    ".svn/*",
    "**/.mypy_cache/**",
    ".mypy_cache/*",
    "**/.pytest_cache/**",
    "*.pytest_cache/*",
    "**/__pycache__/**",
    "*__pycache__/*",
    "**/.venv/**",
    ".venv/*",
]

DEFAULT_SKIP_READ = [
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
    disabled_file_tools: list[str] = Field(
        default_factory=list,
        alias="disabled_file_tools",
        description="List of disabled file tools provided by DISABLED_FILE_TOOLS environment variable.",
    )
    disabled_folder_tools: list[str] = Field(
        default_factory=list,
        alias="disabled_folder_tools",
        description="List of disabled folder tools provided by DISABLED_FOLDER_TOOLS environment variable.",
    )
    read_file_exclusions: list[str] = Field(
        default_factory=lambda: DEFAULT_SKIP_READ,
        alias="read_file_exclusions",
        description="List of file patterns to exclude from all multi-read operations.",
    )
    list_folder_exclusions: list[str] = Field(
        default_factory=lambda: DEFAULT_SKIP_LIST,
        alias="list_folder_exclusions",
        description="List of folder patterns to exclude from listing operations.",
    )
    
