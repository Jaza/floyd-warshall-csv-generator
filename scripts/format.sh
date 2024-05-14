#!/bin/bash
$HOME/.local/bin/poetry run autoflake \
    --remove-all-unused-imports \
    --recursive \
    --remove-unused-variables \
    --in-place \
    floyd_warshall_csv_generator tests
$HOME/.local/bin/poetry run black floyd_warshall_csv_generator tests
$HOME/.local/bin/poetry run isort floyd_warshall_csv_generator tests
