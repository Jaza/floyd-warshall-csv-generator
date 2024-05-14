#!/bin/bash
set -e

curl -sSL https://install.python-poetry.org | python3 -

if [[ -n "${POETRY_VIRTUALENVS_IN_PROJECT:-}" ]]; then
  $HOME/.local/bin/poetry config virtualenvs.in-project true
fi

$HOME/.local/bin/poetry install

set +e
