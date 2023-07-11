"""
This file contains functions for parsing xml files.
"""

import xml.etree.ElementTree as ET


def find_package_references(
    csproj_file_path: str, package_name: str
) -> list[ET.Element]:
    """
    Find all package references with the given name in the csproj file
    """
    tree = ET.parse(csproj_file_path)
    root = tree.getroot()
    return root.findall(f".//PackageReference[@Include='{package_name}']")


def find_package_version(csproj_file_path: str, package_name: str):
    """
    Find the version of the package with the given name in the csproj file
    """
    package_references = find_package_references(csproj_file_path, package_name)
    for package_reference in package_references:
        version = package_reference.get("Version")
        yield version
