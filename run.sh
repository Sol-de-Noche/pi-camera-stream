#!/bin/bash

poetry install
yarn

yarn build
poetry run uvicorn main:app --host 0.0.0.0 --port 8023