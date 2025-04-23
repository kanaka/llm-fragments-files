# llm-fragments-git

[![PyPI](https://img.shields.io/pypi/v/llm-fragments-git.svg)](https://pypi.org/project/llm-fragments-git/)
[![Changelog](https://img.shields.io/github/v/release/simonw/llm-fragments-git?include_prereleases&label=changelog)](https://github.com/simonw/llm-fragments-git/releases)
[![Tests](https://github.com/simonw/llm-fragments-git/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/llm-fragments-git/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/llm-fragments-git/blob/main/LICENSE)

Load GitHub repository contents as fragments

## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/).
```bash
llm install llm-fragments-git
```
## Usage

Use `-f github:user/repo` to include every text file from the specified GitHub repo as a fragment. For example:
```bash
llm -f github:simonw/files-to-prompt 'suggest new features for this tool'
```
Ue `-f issue:user/repo/number` to include the combined Markdown text of a specific issue. For example:
```bash
llm -f https://raw.githubusercontent.com/simonw/llm-fragments-git/refs/tags/0.1/llm_fragments_github.py \
  -f issue:simonw/llm-fragments-github/3 \
  'Propose an implementation for this issue'
```
The `issue:` prefix can also accept a URL to a GitHub issue, for example:
```bash
llm -f issue:https://github.com/simonw/llm-fragments-github/issues/3 \
  'muse on this a bit'
```
Set an API token in the environment variable `GITHUB_TOKEN` to access private repositories or increase your rate limit.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd llm-fragments-git
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
llm install -e '.[test]'
```
To run the tests:
```bash
python -m pytest
```
