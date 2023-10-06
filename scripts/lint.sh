#!/bin/bash 

set -ex

black --check .
ruff check .
mypy .
