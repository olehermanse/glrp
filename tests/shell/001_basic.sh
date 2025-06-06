#!/usr/bin/env bash
set -e
set -x

glrp --version
glrp --help

glrp .
glrp . --output-dir=./out/
glrp . --pretty
glrp . --debug

git log --format=raw | glrp
git log -p --format=raw --show-signature --stat | glrp

cat 001_input.txt | glrp > 001_output.txt
diff 001_expected_output.txt 001_output.txt
