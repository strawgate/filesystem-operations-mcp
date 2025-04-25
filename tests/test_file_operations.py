"""
Simplified tests for file operations, focusing on methods with logic beyond simple os.* calls.
Exception handling for simple operations is covered by tests for the context managers.
"""

import pytest
from filesystem_operations_mcp.servers.multi_file_operations import FileOperations


# Mock Context for testing
class MockContext:
    def info(self, message):
        pass  # Suppress print during tests

    def warning(self, message):
        pass  # Suppress print during tests

    def error(self, message):
        pass  # Suppress print during tests


@pytest.fixture
def file_operations():
    """Fixture to provide a FileOperations instance."""
    return FileOperations()


@pytest.fixture
def mock_ctx():
    """Fixture to provide a MockContext instance."""
    return MockContext()


# No tests for simple file operations methods as their exception handling is covered by context manager tests.
# Add tests here only for FileOperations methods with logic beyond simple os.* calls.
