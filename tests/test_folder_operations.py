import pytest
import os
import shutil
from unittest.mock import MagicMock
from filesystem_operations_mcp.servers.multi_folder_operations import FolderOperations, FileReadSuccess, FileReadError, FileReadSummary
from filesystem_operations_mcp.models.settings import DEFAULT_SKIP_READ, DEFAULT_SKIP_LIST


class MockContext:
    def info(self, message):
        pass

    def debug(self, message):
        pass

    def error(self, message):
        pass

@pytest.mark.parametrize(
    "path, include, exclude, expected",
    [
        ("file.txt", ["*.txt"], [], True),
        ("file.txt", ["*.csv"], [], False),
        ("file.txt", ["*.txt"], ["file.txt"], False),
        ("file.txt", [], ["file.txt"], False),
        ("file.txt", [], [], True),
        ("subdir/file.txt", ["**/*.txt"], [], True),
        ("subdir/file.txt", ["**/*.csv"], ["**/*.txt"], False),
        ("subdir/.git/config", [], DEFAULT_SKIP_LIST, False),
        ("subdir/.venv/file.py", [], DEFAULT_SKIP_LIST, False),
        ("subdir/normal_folder/file.py", [], DEFAULT_SKIP_LIST, True),
        (".venv/file.py", [], DEFAULT_SKIP_LIST, False),
        ("src/.venv/file.py", [], DEFAULT_SKIP_LIST, False),
        ("src/__pycache__/file.py", [], DEFAULT_SKIP_LIST, False),
    ],
)
def test_matches_globs(path, include, exclude, expected):
    folder_operations = FolderOperations()
    result = folder_operations._matches_globs(path, include, exclude)
    assert result == expected

@pytest.fixture
def setup_test_folder(tmp_path):
    """Fixture to set up a temporary folder structure for testing."""
    base_dir = "." / tmp_path / "test_folder"
    base_dir.mkdir()

    # Create files and folders, some matching default exclusions
    (base_dir / "file1.txt").write_text("content1")
    (base_dir / "file2.log").write_text("content2")
    (base_dir / ".git").mkdir()
    (base_dir / ".git" / "config").write_text("git config")
    (base_dir / ".otherhidden").mkdir()
    (base_dir / ".otherhidden" / "config").write_text("git config")
    (base_dir / "__pycache__").mkdir()
    (base_dir / "__pycache__" / "cache.pyc").write_text("cache")
    (base_dir / "subdir").mkdir()
    (base_dir / "subdir" / "file3.txt").write_text("content3")
    (base_dir / "subdir" / ".venv").mkdir()
    (base_dir / "subdir" / ".venv" / "script.py").write_text("script")
    (base_dir / "subdir" / "data.csv").write_text("csv data")

    return base_dir

@pytest.mark.asyncio
async def test_contents_with_default_exclusions(setup_test_folder):
    """Tests listing folder contents with default exclusions."""
    folder_path = setup_test_folder
    ctx = MockContext()
    folder_operations = FolderOperations(
        list_folder_exclusions=DEFAULT_SKIP_LIST,
        read_file_exclusions=DEFAULT_SKIP_READ
    )

    # List contents with default exclusions (recurse=True)
    contents = await folder_operations.contents(ctx, str(folder_path), include=["**/*"], exclude=[], recurse=True)

    # Expected files (excluding default list exclusions like .git, __pycache__, .venv)
    expected_contents = [
        "./file1.txt",
        "./file2.log",
        "subdir/file3.txt",
        "subdir/data.csv",
    ]

    # Sort for consistent comparison
    contents.sort()
    expected_contents.sort()

    assert contents == expected_contents

@pytest.mark.asyncio
async def test_contents_without_default_exclusions(setup_test_folder):
    """Tests listing folder contents without default exclusions."""
    folder_path = setup_test_folder
    ctx = MockContext()
    folder_operations = FolderOperations(
        list_folder_exclusions=DEFAULT_SKIP_LIST,
        read_file_exclusions=DEFAULT_SKIP_READ
    )

    # List contents without default exclusions (recurse=True, bypass_default_exclusions=True)
    contents = await folder_operations.contents(ctx, str(folder_path), include=["**/*"], exclude=[], recurse=True, bypass_default_exclusions=True)

    # Expected files (including default list exclusions)
    expected_contents = [
        ".git/config",
        "__pycache__/cache.pyc",
        ".otherhidden/config",
        "./file1.txt",
        "./file2.log",
        "subdir/.venv/script.py",
        "subdir/data.csv",
        "subdir/file3.txt",
    ]

    # Sort for consistent comparison
    contents.sort()
    expected_contents.sort()

    assert contents == expected_contents

@pytest.mark.asyncio
async def test_read_all_with_default_exclusions(setup_test_folder):
    """Tests reading all files in a folder with default read exclusions."""
    folder_path = setup_test_folder
    ctx = MockContext()
    folder_operations = FolderOperations(
        read_file_exclusions=DEFAULT_SKIP_READ,
        list_folder_exclusions=DEFAULT_SKIP_LIST
    )

    # Read all files with default exclusions (recurse=True)
    summary: FileReadSummary = await folder_operations.read_all(ctx, str(folder_path), include=["**/*"], exclude=[], recurse=True)

    # Expected successful reads (excluding default read exclusions like .pyc)
    expected_successful_files = [
        "./file1.txt",
        "./file2.log",
        "subdir/file3.txt",
        "subdir/data.csv",
    ]

    successful_files = [result.file_path for result in summary.results]
    successful_files.sort()
    expected_successful_files.sort()

    assert successful_files == expected_successful_files
    assert len(summary.errors) == 0 # Assuming no read errors for these files

@pytest.mark.asyncio
async def test_read_all_without_default_exclusions(setup_test_folder):
    """Tests reading all files in a folder without default read exclusions."""
    folder_path = setup_test_folder
    ctx = MockContext()
    folder_operations = FolderOperations(
        read_file_exclusions=DEFAULT_SKIP_READ,
        list_folder_exclusions=DEFAULT_SKIP_LIST
    )

    # Read all files without default exclusions (recurse=True, bypass_default_exclusions=True)
    summary: FileReadSummary = await folder_operations.read_all(ctx, str(folder_path), include=["**/*"], exclude=[], recurse=True, bypass_default_exclusions=True)

    # Expected successful reads (including default read exclusions like .pyc)
    expected_successful_files = [
        ".git/config",
        "__pycache__/cache.pyc",
        "./file1.txt",
        "./file2.log",
        "subdir/.venv/script.py",
        ".otherhidden/config",
        "subdir/data.csv",
        "subdir/file3.txt",
    ]

    successful_files = [result.file_path for result in summary.results]
    successful_files.sort()
    expected_successful_files.sort()

    assert successful_files == expected_successful_files
    assert len(summary.errors) == 0 # Assuming no read errors for these files

@pytest.mark.asyncio
async def test_contents_with_include_only(setup_test_folder):
    """Tests listing folder contents with only include patterns."""
    folder_path = setup_test_folder
    ctx = MockContext()
    folder_operations = FolderOperations(
        list_folder_exclusions=DEFAULT_SKIP_LIST,
        read_file_exclusions=DEFAULT_SKIP_READ
    )

    # List contents with only include pattern for .txt files
    contents = await folder_operations.contents(ctx, str(folder_path), include=["**/*.txt"], exclude=[], recurse=True)

    # Expected files (only .txt files)
    expected_contents = [
        "./file1.txt",
        "subdir/file3.txt",
    ]

    # Sort for consistent comparison
    contents.sort()
    expected_contents.sort()

    assert contents == expected_contents