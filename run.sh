#!/bin/bash

set -e

PROJECT_ROOT="$(
    cd "$(dirname "$0")"
    pwd
)"

cd "$PROJECT_ROOT"

export PYTHONPATH="$PROJECT_ROOT"

exec python src/main.py "$@"
