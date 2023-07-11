"""
Reporting module for nuget scanner
"""

import text_utils as text

# Solutuin name column width
S_NAME_COL_WIDTH = 35
# Project name column width
P_NAME_COL_WIDTH = 50
# Version column width
VERSION_COL_WIDTH = 10


def format_markdown(package_name: str, search_results: dict[str, dict]):
    """
    Format the search results as markdown
    :param package_name: The name of the package
    :param search_results: The search results
    :return: The markdown-formatted table of search results
    """
    header = f"### Package: {package_name}\n"

    table_header = "| Solution | Project | Version |\n"
    table_header += "| -------- | ------- | ------- |\n"

    table_rows = ""
    for s_name, p_versions in search_results.items():
        # Getting unique list of versions
        versions = set(p_versions.values())
        s_name = text.truncate_string(s_name, S_NAME_COL_WIDTH)
        # Adding asterisk if different versions in projects
        if len(versions) > 1:
            s_name += "*" if len(s_name) < S_NAME_COL_WIDTH else s_name[:-1] + "*"

        for project, version in p_versions.items():
            p_name = text.truncate_string(project, P_NAME_COL_WIDTH)
            table_rows += f"| {s_name} | {p_name} | {version} |\n"

    return header + table_header + table_rows


def format_text(package_name: str, search_results: dict[str, dict]):
    """
    Format the search results as text
    :param package_name: The name of the package
    :param search_results: The search results
    :return: The text-formatted table of search results
    """
    header = f"Package: {package_name}\n"

    table_header = f"{'Solution':<{S_NAME_COL_WIDTH}} {'Project':<{P_NAME_COL_WIDTH}} {'Version':<{VERSION_COL_WIDTH}}\n"
    table_header += (
        "-" * (S_NAME_COL_WIDTH + P_NAME_COL_WIDTH + VERSION_COL_WIDTH) + "\n"
    )

    table_rows = ""
    for s_name, p_versions in search_results.items():
        # Getting unique list of versions
        versions = set(p_versions.values())
        s_name = text.truncate_string(s_name, S_NAME_COL_WIDTH)
        # Adding asterisk if different versions in projects
        if len(versions) > 1:
            s_name += "*" if len(s_name) < S_NAME_COL_WIDTH else s_name[:-1] + "*"

        for project, version in p_versions.items():
            p_name = text.truncate_string(project, P_NAME_COL_WIDTH)
            table_rows += f"{s_name:<{S_NAME_COL_WIDTH}} {p_name:<{P_NAME_COL_WIDTH}} {version:<{VERSION_COL_WIDTH}}\n"

    return header + table_header + table_rows
