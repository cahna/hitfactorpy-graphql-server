# Linux dev environment steps

## Prerequisites

### Install system dependencies

- [poetry](https://python-poetry.org/docs/#installation)
- [pyenv](https://github.com/pyenv/pyenv)
  - and [its dependencies](https://github.com/pyenv/pyenv/wiki#suggested-build-environment)
  - verify installation with `pyenv doctor` 

### Setup pyenv for project

1. `pyenv virtualenv 3.10 hitfactorpy_graphql_server`: create a virtualenv named "hitfactorpy_graphql_server" using python v3.10
2. `pyenv local hitfactorpy_graphql_server`: configure pyenv to use "hitfactorpy_graphql_server" for the current directory
3. `pyenv activate hitfactorpy_graphql_server`: activate the virtualenv

### Configure poetry to recognize pyenv

1. `poetry config virtualenvs.prefer-active-python true`
2. Verify output of `poetry env info`; the paths for `Virtualenv` and `System` should match the value of `$PYENV_ROOT` (default: `$HOME/.pyenv`)

## Development

1. Install dependencies: `poetry install`
2. Install pre-commit hooks: `pre-commit install`
3. Test: `poetry run tox` (or `tox`, or `pytest tests`)
4. Build: `poetry build`
