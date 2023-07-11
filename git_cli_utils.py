"""
Git CLI Utils
"""

import subprocess


def git_stash(repository_path) -> subprocess.CompletedProcess[str]:
    """
    Stash uncommitted changes
    """
    return git_run(repository_path, ["stash"])


def git_stash_list(repository_path) -> subprocess.CompletedProcess[str]:
    """
    Get the stash list
    """
    return git_run(repository_path, ["stash", "list"])


def git_stash_pop(repository_path) -> subprocess.CompletedProcess[str]:
    """
    Pop the stash
    """
    return git_run(repository_path, ["stash", "pop"])


def git_current_branch(repository_path) -> subprocess.CompletedProcess[str]:
    """
    Get the current branch
    """
    return git_run(repository_path, ["rev-parse", "--abbrev-ref", "HEAD"])


def git_checkout(
    repository_path, branch_name: str = "master"
) -> subprocess.CompletedProcess[str]:
    """
    Checkout the specified branch
    """
    return git_run(repository_path, ["checkout", branch_name])


def git_pull(repository_path) -> subprocess.CompletedProcess[str]:
    """
    Pull with rebase
    """
    return git_run(repository_path, ["pull", "--rebase"])


def git_pull_safe(repository_path):
    """
    Pulls master with rebase, stashing and unstashing changes if necessary
    """
    try:
        stash_list_before = git_stash_list(
            repository_path,
        ).stdout
        git_stash(repository_path)
        stash_list_after = git_stash_list(repository_path).stdout
        stash_was_successful = stash_list_before != stash_list_after

        current_branch = git_current_branch(repository_path).stdout.strip()

        if current_branch != "master":
            git_checkout(repository_path)

        git_pull(repository_path)
        if current_branch != "master":
            git_checkout(repository_path, current_branch)

        # Pop stash to unstash the changes if stash was successful
        if stash_was_successful:
            git_stash_pop(repository_path)
    except subprocess.CalledProcessError as ex:
        print(f"Failed to update git repo in {repository_path}. Error: {ex}")


def git_run(repository_path, command: list[str]) -> subprocess.CompletedProcess[str]:
    """
    Run a git command in the specified repository
    """
    return subprocess.run(
        ["git"] + command,
        cwd=repository_path,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=True,
    )
