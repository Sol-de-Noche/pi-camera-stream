#!/bin/bash

BASE_DIR="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
RECORDING_DIR=$BASE_DIR'/recording/'
VIDEOS_DIR=$BASE_DIR'/videos/'

mkdir -p $RECORDING_DIR
mkdir -p $VIDEOS_DIR

poetry run uvicorn main:app --host 0.0.0.0 --port 8023