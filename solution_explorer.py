"""
Solution explorer module
"""
import os
from pathlib import Path


class SolutionExplorer:
    """
    Solution explorer class
    """

    @staticmethod
    def get_solutions(root_folder) -> dict[str, list[Path]]:
        """
        Get the solutions in the specified root folder
        together with their projects
        :param root_folder: The root folder
        :return: A dictionary of solution names and their
        projects provided as a list of paths to .csproj files
        """
        if not os.path.isdir(root_folder):
            raise ValueError(f"Invalid root folder: {root_folder}")

        solution_paths = [
            entry.path for entry in os.scandir(root_folder) if entry.is_dir()
        ]

        result = {}
        for solution_path in solution_paths:
            solution_name = os.path.basename(solution_path)
            result[solution_name] = Path(solution_path).rglob("*.csproj")

        return result
