import logging
from logging.handlers import TimedRotatingFileHandler
import argparse
import yaml
from pathlib import Path
from xdg import XDG_CONFIG_HOME, XDG_CACHE_HOME
from dfmoco2ur import bridge
from dfmoco2ur.config import Configuration
import asyncio


if __name__ == '__main__':

    # Resolve the default config path using XDG and alternatively $HOME/.config followed by dfmoco-ur/config.yaml
    base_path = Path(XDG_CONFIG_HOME)
    if not base_path:
        base_path = Path.home().joinpath('.config')
    default_config_path = base_path.joinpath('dfmoco-ur', 'config.yaml')

    # Parse CLI arguments to obtain the config and log level
    parser = argparse.ArgumentParser(
        description='Dragonframe Motion Control to Universal Robot bridge', prefix_chars='-')
    parser.add_argument('--config', default=default_config_path,
                        help='Path to a configuration')
    args = parser.parse_args()

    # Parse the configuration and run the schedule
    config = Configuration({})
    try:
        with open(args.config, 'r') as raw_config:
            _config = Configuration(yaml.load(raw_config, Loader=yaml.FullLoader))
            config = _config
    except FileNotFoundError as err:
        logging.debug(err)
        
    # Setup logging
    logger = logging.getLogger("dfmoco2ur")
    logger.setLevel(config.get("logging.dfmoco2ur"))

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
    
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    
    def file_handler(filename):
        handler = TimedRotatingFileHandler(
            Path(XDG_CACHE_HOME).joinpath(filename),
            when="d", interval=1, backupCount=7
        )
        handler.setFormatter(formatter)
        return handler

    logger.addHandler(stream_handler)
    logger.addHandler(file_handler("dfmoco2ur.log"))

    for l in config.get('logging'):
        level = config.get(f'logging.{l}')
        logger = logging.getLogger(l)
        logger.setLevel(level)
        logger.addHandler(file_handler(f"{l}.log"))

    asyncio.run(bridge.run(config))