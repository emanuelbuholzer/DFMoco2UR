import logging

logger = logging.getLogger(__name__)

defaults = {
    "heartbeat": {
        "interval": 2
    },
    "ur": {
        "host": "192.168.5.42",
        "dashboard_port": 29999,
        "max_unlock_attempts": 3,
        "tool_center_point": [0, 0, 0.1, 0, 0, 0],
        "weight": 2,
        "center_of_gravity": [0, 0.1, 0],
        "acc": 0.01,
        "vel": 0.01,
        "movement_aggregator": {
            "initial_timeout": 3,
            "max_throughput": 1,
            "interval": 4
        },
        "axis": "xyzrxryrz",
        "axes": {
            "xyzrxryrz": {
                "scale": [4*10000, 4*10000, 4*10000, 25*572.9577951308232, 25*572.9577951308232, 25*572.9577951308232],
                "inch_acc": [0.005, 0.005, 0.005, 0.01, 0.01, 0.01],
                "jog_acc": [0.01, 0.01, 0.01, 0.05, 0.05, 0.05]
            }
        }
    },
    "df": {
        "host": "127.0.0.1",
        "port": 10001,
    },
    "api": {
        "host": "127.0.0.1",
        "port": 10002
    },
    "logging": {
        "dfmoco2ur": 30,
        "ursecmon": 40,
        "urx": 50
    },
}

class Configuration:
    
    def __init__(self, config):
        self.config = config
    
    def _get(self, key, config):
        val = config
        for k in key.split("."):
            if k.isnumeric():
                val = val[int(k)]
            else:
                val = val.get(k)
        if val == None:
            raise AttributeError(f"Key {key} not found in configuration")
        return val

    def get(self, key):
        try:
            return self._get(key, self.config)
        except AttributeError as err:
            try:
                val = self._get(key, defaults)
                logger.debug(f"Using default config value {val} of key {key}.")
                return val
            except AttributeError:
                raise err
                
            


    