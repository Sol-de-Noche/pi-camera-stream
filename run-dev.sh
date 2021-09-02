#!/bin/bash

poetry install
yarn install

yarn serve &
uvicorn main:app --reload