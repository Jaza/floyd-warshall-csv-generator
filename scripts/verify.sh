#!/bin/bash
set -e

$HOME/.local/bin/poetry run black floyd_warshall_csv_generator tests --check
$HOME/.local/bin/poetry run isort --check-only floyd_warshall_csv_generator tests
$HOME/.local/bin/poetry run flake8 floyd_warshall_csv_generator tests
$HOME/.local/bin/poetry run mypy floyd_warshall_csv_generator tests
$HOME/.local/bin/poetry run bandit -c pyproject.toml -r floyd_warshall_csv_generator tests

set +e
