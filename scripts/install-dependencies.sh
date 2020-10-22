#!/usr/bin/env bash

# Setup dfmoco2ur-api


git submodule init
git submodule update

pushd dfmoco2ur-api
source venv/bin/activate
pip3 install -r requirements.txt
popd
deactivate