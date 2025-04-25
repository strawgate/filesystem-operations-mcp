"""
Custom exceptions for bulk filesystem operations.
"""


class MCPFileSystemOperationError(Exception):
    """Base exception for bulk filesystem operations."""

    pass


class MCPFileOperationError(MCPFileSystemOperationError):
    """Exception raised for errors during file operations."""

    def __init__(self, message, file_path):
        self.file_path = file_path
        super().__init__(f"Error performing operation on file {file_path}: {message}")


class MCPFolderOperationError(MCPFileSystemOperationError):
    """Exception raised for errors during folder operations."""

    def __init__(self, message, folder_path):
        self.folder_path = folder_path
        super().__init__(
            f"Error performing operation on folder {folder_path}: {message}"
        )


class MCPFileNotFoundError(MCPFileOperationError):
    """Exception raised when a file is not found."""

    def __init__(self, file_path):
        super().__init__("File not found", file_path)


class MCPFolderNotFoundError(MCPFolderOperationError):
    """Exception raised when a folder is not found."""

    def __init__(self, folder_path):
        super().__init__("Folder not found", folder_path)
