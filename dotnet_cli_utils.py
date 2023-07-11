"""
Dotnet CLI utilities
"""

import subprocess
import os


def dotnet_list_package(
    csproj_file_path: str, include_transitive: bool = False
) -> subprocess.CompletedProcess[str]:
    """
    List the packages used by the specified project
    """
    params = ["dotnet", "list", csproj_file_path, "package"]
    if include_transitive:
        params += ["--include-transitive"]

    return subprocess.run(
        params,
        cwd=os.path.dirname(csproj_file_path),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=True,
    )
