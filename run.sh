#!/bin/bash

mkdir -p recording
mkdir -p videos

poetry run uvicorn main:app --host 0.0.0.0 --port 8023