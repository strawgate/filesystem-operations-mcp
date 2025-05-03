import pytest
from filesystem_operations_mcp.servers.multi_folder_operations import FolderOperations
from filesystem_operations_mcp.models.settings import DEFAULT_SKIP_READ


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
        ("subdir/.git/config", [], DEFAULT_SKIP_READ, False),
        ("subdir/.venv/file.py", [], DEFAULT_SKIP_READ, False),
        ("subdir/normal_folder/file.py", [], DEFAULT_SKIP_READ, True),
        (".venv/file.py", [], DEFAULT_SKIP_READ, False),
        ("src/.venv/file.py", [], DEFAULT_SKIP_READ, False),
        ("src/__pycache__/file.py", [], DEFAULT_SKIP_READ, False),
    ],
)
def test_matches_globs(path, include, exclude, expected):
    folder_operations = FolderOperations()
    result = folder_operations._matches_globs(path, include, exclude)
    assert result == expected