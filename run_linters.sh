#!/usr/bin/env bash

set -e

source .env

TARGET="./$SERVICE_NAME"

black --check "$TARGET" \
  && ruff check "$TARGET" \
  && flake8 --statistics "$TARGET" \
  && pylint "$TARGET"