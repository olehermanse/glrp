#!/usr/bin/env bash

# Convenience script to run both unit and shell tests:

# Warning: This script installs glrp and its dependencies:
#          pip3 install .
#          This is needed to run the shell tests.

set -e
set -x

py.test

pip3 install . && (cd tests/shell && bash run.sh)
