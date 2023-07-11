"""
Text utilities
"""

from typing import Optional


def truncate_string(source, max_length):
    """
    Truncate a string to a maximum length, adding three ellipsis if necessary
    :param s: The string to truncate
    :param max_length: The maximum length of the string
    :return: The truncated string
    :raises ValueError: If max_length is less than the length of the ellipsis
    """
    ending = "..."
    if max_length < len(ending):
        raise ValueError("max_length must be at least as long as the ending")

    return source if len(source) <= max_length else source[: max_length - 3] + "..."


def get_transitive_report_section(report: str) -> Optional[str]:
    """
    Extract the transitive section from a dotnet list package report
    :param report: The report
    :return: The transitive section
    """
    # Find the start of the transitive section
    start_markers = ["Transitive", "Транзитив"]
    start_index = -1
    for marker in start_markers:
        start_index = report.find(marker)
        if start_index >= 0:
            break

    if start_index >= 0:
        start_index += len(marker)
        return report[start_index:]

    return None


def get_transitive_dep_info(report_line: str) -> Optional[tuple[str, str]]:
    """
    Extract the transitive dependency information from a line
    in the transitive section of a dotnet list package report
    :param report_line: The line
    :return: A tuple containing the package name and version
    """
    # Split the line into words
    split_line = report_line.strip().split()
    if len(split_line) == 3:
        return split_line[1], split_line[2]

    return None


def find_transitive_dep_version(report: str, package_name: str) -> Optional[str]:
    """
    Find the version of a transitive dependency in a dotnet list package report
    :param report: The report
    :param package_name: The package name
    :return: The version of the package
    """
    if not report:
        return None

    if not package_name:
        return None

    for line in report.splitlines():
        dep_info = get_transitive_dep_info(line)
        if dep_info and dep_info[0] == package_name:
            return dep_info[1]

    return None
