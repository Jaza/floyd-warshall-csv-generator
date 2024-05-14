#!/bin/bash
set -e

$HOME/.local/bin/poetry run pytest \
  -m pureunit \
  --cov=. \
  --cov-fail-under=100 \
  --cov-report=term-missing \
  tests

set +e
