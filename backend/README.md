# manga-updater (Server)

## Installation

Requirements:
- ⚠️ Python 3.10+
- Bash

Install python:
> Use any way to get modern python, you used to. I use [mise](https://github.com/jdx/mise) to manage python versions.

Download repository with script:
```bash
git clone github.com/bulatenkom/manga-updater
cd dedup
```

Setup virtualenv (skip if you are going to use global python and pip).
```bash
python -m venv .venv
source .venv/bin/activate

# check that venv activated correctly
# both following commands should print paths directed to python/pip in .venv
which pip
which python
```

Install dependencies
```bash
pip install -r requirements
```
