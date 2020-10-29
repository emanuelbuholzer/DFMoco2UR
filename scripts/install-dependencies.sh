#!/usr/bin/env bash

# Setup dfmoco2ur-bridge

git submodule init
git submodule update

pushd dfmoco2ur-bridge
source venv/bin/activate
pip3 install -r requirements.txt
popd
deactivate