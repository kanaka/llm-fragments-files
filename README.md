# llm-fragments-dir

[![PyPI](https://img.shields.io/pypi/v/llm-fragments-dir.svg)](https://pypi.org/project/llm-fragments-dir/)
[![Changelog](https://img.shields.io/github/v/release/simonw/llm-fragments-dir?include_prereleases&label=changelog)](https://github.com/simonw/llm-fragments-dir/releases)
[![Tests](https://github.com/simonw/llm-fragments-dir/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/llm-fragments-dir/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/llm-fragments-dir/blob/main/LICENSE)

Load directory/git/GitHub contents as file fragments (with file
names). The fragment format is like this:
````
File: path/to/file
```
file contents
```
````

## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/).
```bash
llm install llm-fragments-dir
```
## Usage

Use `-f dir:path/to/dir` to include every text file from the directory.
```bash
llm -f dir:path/to/dir 'Summarize each file as a brief bullet point.'
```
Use `-f git:path/to/repo` to include every text files from the local git repo directory.
```bash
llm -f git:path/to/repo 'Summarize this project'
```
Use `-f github:user/repo` to include every text file from the specified GitHub repo as a fragment. For example:
```bash
llm -f github:simonw/files-to-prompt 'suggest new features for this tool'
```
Set an API token in the environment variable `GITHUB_TOKEN` to access private repositories or increase your rate limit.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd llm-fragments-dir
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
python -m pytest
```
