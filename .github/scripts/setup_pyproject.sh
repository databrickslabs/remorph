#!/usr/bin/env bash

set -xve

PYTHON_VERSION="$1"
JINJA_TEMPLATE_PATH=.github/scripts/pyproject_toml.j2
OUTPUT_PATH=pyproject.toml

py_version_str="py${PYTHON_VERSION/./}"


jinja2 -D py_decimal="$PYTHON_VERSION" -D py_str="$py_version_str" "$JINJA_TEMPLATE_PATH" > "$OUTPUT_PATH"


if [ $? -eq 0 ]; then
    echo "pyproject.toml successfully configured with the REMORPH_PYTHON version: "$PYTHON_VERSION
else
    echo "pyproject.toml configuration failed."
    exit 1
fi
