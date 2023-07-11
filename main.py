"""
This script searches for the specified NuGet package in the 
specified root folder
"""

import os
import argparse
from collections import defaultdict

from package_version_extractor import PackageVersionExtractor
from solution_explorer import SolutionExplorer
from report import format_markdown, format_text
from git_cli_utils import git_pull_safe


def find_nuget_version(root_folder, package_name, mode) -> dict[str, dict]:
    """
    Find the version of the specified package in the specified root folder
    :param root_folder: The root folder for solutions to be searched
    :param package_name: The name of the package to be searched for
    :param mode: The mode to be used for searching,
    either "direct" or "transitive"
    :return: A dictionary of solution names and their
    projects provided as a name of project with the version of the
    specified package
    """
    res = defaultdict(dict)
    extractor = PackageVersionExtractor(mode)
    solutions = SolutionExplorer.get_solutions(root_folder)
    for solution_name, projects in solutions.items():
        res[solution_name] = {
            project.stem: version
            for project in projects
            if (version := extractor.extract(str(project), package_name))
        }

    return res


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Find NuGet package versions in .NET projects."
    )
    parser.add_argument(
        "--root-folder",
        type=str,
        help="Root folder containing .NET project repositories",
    )
    parser.add_argument(
        "--package-name", type=str, help="NuGet package name to search for"
    )
    parser.add_argument(
        "--mode", type=str, help="Resolving dependencies: direct or transitive"
    )
    parser.add_argument(
        "--update-git",
        action="store_true",
        help="Update git repositories before searching",
    )
    parser.add_argument(
        "--format-md", action="store_true", help="Output results in markdown format"
    )

    args = parser.parse_args()

    if args.update_git:
        print("Updating git repositories...")
        solution_dirs = [
            d
            for d in os.listdir(args.root_folder)
            if os.path.isdir(os.path.join(args.root_folder, d))
        ]
        num_solutions = len(solution_dirs)
        for i, solution_dir in enumerate(solution_dirs):
            print(
                f"Updating and analyzing solution ({i + 1}/{num_solutions}): {solution_dir}"
            )
            git_pull_safe(os.path.join(args.root_folder, solution_dir))

    results = find_nuget_version(args.root_folder, args.package_name, args.mode)

    if results:
        if args.format_md:
            report_markdown = format_markdown(args.package_name, results)
            print(report_markdown)
        else:
            report_text = format_text(args.package_name, results)
            print(report_text)
    else:
        print(f"No references to package {args.package_name} found.")
