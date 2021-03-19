import json
import dfmoco2ur.api.actions as actions
from xdg import XDG_DATA_HOME
from pathlib import Path
import os


async def run(websocket):
    data_dir = Path(XDG_DATA_HOME).joinpath('.dfmoco2ur')
    data_dir.mkdir(parents=True, exist_ok=True)
    
    positions = [p.name.removesuffix('.npy') for p in data_dir.glob('*.npy')]

    response = {
       "type": actions.LOAD_POSITION_RESPONSE,
       "payload": {
           "positionNames": positions
       }
    }
    await websocket.send(json.dumps(response))