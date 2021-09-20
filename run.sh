#!/bin/bash

BASE_DIR="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
RECORDING_DIR=$BASE_DIR'/recording/'
VIDEOS_DIR=$BASE_DIR'/videos/'
POETRY=`which poetry`

mkdir -p $RECORDING_DIR
mkdir -p $VIDEOS_DIR

cd $BASE_DIR
$POETRY run uvicorn main:app --host 0.0.0.0 --port 8023