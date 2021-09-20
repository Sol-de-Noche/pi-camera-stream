#!/bin/bash

mkdir -p recording
poetry install
yarn

yarn build
