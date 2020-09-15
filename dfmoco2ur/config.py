import logging

logger = logging.getLogger(__name__)

defaults = {
    "ur": {
        "host": "192.168.5.42",
        "tool_center_point": [0, 0, 0.1, 0, 0, 0],
        "weight": 2,
        "center_of_gravity": [0, 0.1, 0],
        "acc": 0.1,
        "vel": 0.05,
        "movement_aggregator": {
            "initial_timeout": 2,
            "max_throughput": 1,
            "interval": 3
        },
        "axis": "xyzrxryrz",
        "axes": {
            "xyzrxryrz": {
                "scale": [10000, 10000, 10000, 572.9577951308232, 572.9577951308232, 572.9577951308232],
                "inch_size": [10, 10, 10, 10, 10, 10],
                "jog_size": [250, 250, 250, 50, 50, 50]
            }
        }
    },
    "df": {
        "host": "127.0.0.1",
        "port":  "10001"
    },
    "logging": {
        "dfmoco2ur": 20,
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
                
            


    