#!/bin/bash
set -e

$HOME/.local/bin/poetry run pytest \
  --cov=. \
  --cov-fail-under=100 \
  --cov-report=term-missing \
  tests

set +e
