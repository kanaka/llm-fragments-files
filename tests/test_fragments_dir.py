from llm_fragments_dir import git_loader, dir_loader, github_loader
import pytest

def _frags(fs):
    return [(str(f.source), str(f)) for f in fs]


def test_git_loader():
    fragments = git_loader("./")
    assert "README.md" in [a for a, _ in _frags(fragments)]
    assert ("example/file1.txt", "File: example/file1.txt\n```\nThis is an example file.\n\n```\n") in _frags(fragments)

def test_dir_loader():
    fragments = dir_loader("./example")
    assert ("example/file1.txt", "File: example/file1.txt\n```\nThis is an example file.\n\n```\n") in _frags(fragments)

def test_github_loader():
    fragments = github_loader("simonw/test-repo-for-llm-fragments-github")
    assert [(str(fragment.source), str(fragment)) for fragment in fragments] == [
        (
            "simonw/test-repo-for-llm-fragments-github/README.md",
            "File: simonw/test-repo-for-llm-fragments-github/README.md\n```\n# test-repo-for-llm-fragments-github\nUsed by tests for https://github.com/simonw/llm-fragments-github\n\n```\n",
        ),
        (
            "simonw/test-repo-for-llm-fragments-github/example/file.txt",
            "File: simonw/test-repo-for-llm-fragments-github/example/file.txt\n```\nThis is an example file.\n\n```\n",
        ),
    ]

