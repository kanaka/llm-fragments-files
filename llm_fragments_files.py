#!/usr/bin/env python3

from typing import List, Tuple
import llm
import os
import pathlib
import re
import subprocess
import sys
import tempfile


@llm.hookimpl
def register_fragment_loaders(register):
    register("file", file_loader)
    register("dir", dir_loader)
    register("git", git_loader)
    register("github", github_loader)


def file_loader(argument: str) -> List[llm.Fragment]:
    """
    Load a file from a local directory as a fragment

    Argument is a path to a directory
    """
    try:
        relative_path = pathlib.Path(argument)

        return _files_to_fragments("", _load_files("", [relative_path]))

    except Exception as e:
        raise ValueError(f"Error processing directory {argument}: {str(e)}")


def dir_loader(argument: str) -> List[llm.Fragment]:
    """
    Load files from a local directory as fragments

    Argument is a path to a directory
    """
    try:
        return _files_to_fragments(argument, _dir_files(argument))

    except Exception as e:
        raise ValueError(f"Error processing directory {argument}: {str(e)}")


def git_loader(argument: str) -> List[llm.Fragment]:
    """
    Load files from a local git working copy as fragments

    Argument is a path to the top or subdirectory of a git working copy.
    """
    try:
        return _files_to_fragments(argument, _git_files(argument))

    except Exception as e:
        raise ValueError(f"Error processing git directory {argument}: {str(e)}")


def github_loader(argument: str) -> List[llm.Fragment]:
    """
    Load files from a GitHub repository as fragments

    Argument is a GitHub repository URL or username/repository
    """
    # Normalize the repository argument
    if not argument.startswith(("http://", "https://", "git@")):
        # Assume format is username/repo
        repo_url = f"https://github.com/{argument}.git"
    else:
        repo_url = argument
        if not repo_url.endswith(".git"):
            repo_url = f"{repo_url}.git"

    # Create a temporary directory to clone the repository
    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            # Clone the repository with --no-checkout first
            subprocess.run(
                ["git", "clone", "--depth=1", "--filter=blob:none", repo_url, temp_dir],
                check=True,
                capture_output=True,
                text=True,
            )

            # Checkout files without .git metadata
            subprocess.run(
                ["git", "checkout", "HEAD", "--", "."],
                check=True,
                capture_output=True,
                text=True,
                cwd=temp_dir,
            )

            # Process the cloned repository
            return _files_to_fragments(argument, _git_files(temp_dir))
        except subprocess.CalledProcessError as e:
            # Handle Git errors
            raise ValueError(f"Failed to clone or process repository {repo_url}: {e.stderr}")
        except Exception as e:
            # Handle other errors
            raise ValueError(f"Error processing repository {repo_url}: {str(e)}")


def _git_files(repo_path: str) -> List[Tuple[str, str]]:
    """
    Return [(path, content), ...] for files in a git repository.
    Excludes .git and gitignored files.
    """
    # List tracked and untracked files, excluding .git and gitignored files
    res = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
        check=True,
        capture_output=True,
        text=True,
        cwd=repo_path,
    )
    relative_paths = res.stdout.split("\n")

    return _load_files(repo_path, relative_paths)


def _dir_files(dir_path: str) -> List[Tuple[str, str]]:
    relative_paths = [(pathlib.Path(root) / file).relative_to(dir_path)
            for root, dirs, files in os.walk(dir_path)
            for file in files]
    return _load_files(dir_path, relative_paths)


def _load_files(top_path: str, relative_paths: List[str]) -> List[Tuple[str, str]]:
    """
    Return [(path, content), ...] for each file in relative_paths that
    is a regular text (UTF-8) file.
    """
    files = []
    for relative_path in relative_paths:
        file_path = pathlib.Path(top_path) / relative_path
        if file_path.is_file():
            try:
                # Try to read the file as UTF-8
                content = file_path.read_text(encoding="utf-8")

                # Add the file as (path, content)
                files.append((relative_path, content))
            except UnicodeDecodeError:
                # Skip files that can't be decoded as UTF-8
                continue

    return files


def _files_to_fragments(prefix: str, files: List[Tuple[str, str]]) -> List[llm.Fragment]:
    fragments = []
    for path, content in files:
        full_path = str(pathlib.Path(prefix, path))
        frag = f"File: {full_path}\n```\n{content}\n```\n"
        fragments.append(llm.Fragment(frag, full_path))

    return fragments


def _to_markdown(issue: dict, comments: List[dict]) -> str:
    md: List[str] = []
    md.append(f"# {issue['title']}\n")
    md.append(f"*Posted by @{issue['user']['login']}*\n")
    if issue.get("body"):
        md.append(issue["body"] + "\n")

    if comments:
        md.append("---\n")
        for c in comments:
            md.append(f"### Comment by @{c['user']['login']}\n")
            if c.get("body"):
                md.append(c["body"] + "\n")
            md.append("---\n")

    return "\n".join(md).rstrip() + "\n"

if __name__ == "__main__":
    [kind, location] = sys.argv[1].split(":")
    loaders = {
        "file": file_loader,
        "dir": dir_loader,
        "git": git_loader,
        "github": github_loader
    }
    fragments = loaders[kind](location)
    for fragment in fragments:
        print("FILE/SOURCE:", fragment.source)
        print("CONTENT:\n" + re.sub(r'^', '    ', str(fragment), flags=re.MULTILINE))

