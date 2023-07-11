"""
This module contains the PackageVersionExtractor class.
"""

import os
from typing import Optional

import xml_utils as xml
import dotnet_cli_utils as dotnet
import text_utils as text


class PackageVersionExtractor:
    """
    This class is used to extract the version of a nuget package
    from either a csproj file or a dotnet list package report.
    """

    allowed_modes = ["direct", "transitive"]

    def __init__(self, mode="direct"):
        if mode not in self.allowed_modes:
            raise ValueError(
                f"Invalid mode: {mode}. Only {self.allowed_modes} are allowed."
            )
        self.mode = mode

    def extract(self, csproj_file_path: str, package_name: str) -> Optional[str]:
        """
        Extract the version of the specified package from the
        specified csproj file
        """
        if not csproj_file_path:
            raise ValueError("csproj_file_path cannot be empty.")

        if not os.path.exists(csproj_file_path):
            raise ValueError(f"{csproj_file_path} does not exist.")

        if not package_name:
            raise ValueError("package_name cannot be empty.")

        if self.mode == "direct":
            versions = list(xml.find_package_version(csproj_file_path, package_name))
            if len(versions) > 1:
                raise ValueError(
                    f"Found multiple versions of {package_name} in {csproj_file_path}."
                )
            return versions[0] if versions else None

        if self.mode == "transitive":
            output = dotnet.dotnet_list_package(csproj_file_path, True).stdout.strip()
            version = text.find_transitive_dep_version(output, package_name)
            return version

        return None
