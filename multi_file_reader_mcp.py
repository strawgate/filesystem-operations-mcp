import os
from typing import List, Dict, Union
from fastmcp import FastMCP, Context

# Create an MCP server instance
mcp = FastMCP(
    "MultiFileReader",
    description="An MCP server that can read multiple files at once.",
    dependencies=["fastmcp"]
)

@mcp.tool()
async def read_files(file_paths: List[str], ctx: Context) -> Dict[str, Union[str, Dict]]:
    """
    Reads the content of multiple files specified by their paths.

    Args:
        file_paths: A list of relative or absolute file paths to read.
        ctx: The FastMCP context object.

    Returns:
        A dictionary where keys are the file paths and values are either
        the file content (as a string) or an error dictionary if reading failed.
    """
    results = {}
    total_files = len(file_paths)
    ctx.info(f"Attempting to read {total_files} files.")

    for i, file_path in enumerate(file_paths):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            results[file_path] = content
            ctx.info(f"Successfully read {file_path}")
        except FileNotFoundError:
            ctx.warning(f"File not found: {file_path}")
            results[file_path] = {"error": "FileNotFound", "message": f"The file '{file_path}' was not found."}
        except PermissionError:
            ctx.warning(f"Permission denied for file: {file_path}")
            results[file_path] = {"error": "PermissionError", "message": f"Permission denied when trying to read '{file_path}'."}
        except Exception as e:
            ctx.error(f"Error reading file {file_path}: {str(e)}")
            results[file_path] = {"error": "ReadError", "message": f"An unexpected error occurred while reading '{file_path}': {str(e)}"}

        # Report progress after processing each file
        await ctx.report_progress(i + 1, total_files)

    ctx.info(f"Finished processing {total_files} files.")
    return results

# Allow running the server directly for testing or advanced use cases
if __name__ == "__main__":
    mcp.run()