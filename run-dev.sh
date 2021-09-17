#!/bin/bash

mkdir -p recording
poetry install
yarn install

yarn serve &
uvicorn main:app --reload