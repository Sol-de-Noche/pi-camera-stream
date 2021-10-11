#!/bin/bash

BASE_DIR="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
POETRY=`which poetry`

$POETRY install
yarn

yarn build
