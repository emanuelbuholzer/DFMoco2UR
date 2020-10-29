#!/usr/bin/env bash

pushd dfmoco2ur-bridge
source venv/bin/activate
python3 -m pytest
popd
deactivate