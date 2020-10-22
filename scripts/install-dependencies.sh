#!/usr/bin/env bash

source venv/bin/activate

git submodule init
git submodule update

pip3 install -r requirements.txt