from llm_fragments_git import git_loader, dir_loader
import pytest

def _frags(fs):
    return [(str(f.source), str(f)) for f in fs]


def test_git_loader():
    fragments = git_loader("./")
    assert "README.md" in [a for a, _ in _frags(fragments)]
    assert ("example/file.txt", "This is an example file.\n") in _frags(fragments)

def test_dir_loader():
    fragments = dir_loader("./example")
    assert ("example/file.txt", "This is an example file.\n") in _frags(fragments)
