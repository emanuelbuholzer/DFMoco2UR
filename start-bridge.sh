#!/usr/bin/env bash
. venv/bin/activate

echo "Starting the python bridge"
pushd dfmoco2ur-bridge
python3 -m dfmoco2ur --config /Users/hslu/Desktop/DFMoco2UR/hack/test.yaml
popd

deactivate