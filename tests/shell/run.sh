#!/usr/bin/env bash
set -e
set -x

# Expectation way to run shell tests is:
# pip3 install .
# cd tests/shell
# bash ./run.sh
#
# Or in a one liner:
# pip3 install . && (cd tests/shell && bash ./run.sh)

bash ./001_basic.sh
