import logging
import argparse
import yaml
from pathlib import Path
from xdg import XDG_CONFIG_HOME
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

    # Parse the configuration and run the scheduler
    try:
        with open(args.config, 'r') as raw_config:
            config = Configuration(yaml.load(raw_config, Loader=yaml.FullLoader))
            
            # Setup logging
            # TODO: We might want to send our logs out via a Websocket.
            logger = logging.getLogger("dfmoco2ur")
            logger.setLevel(config.get("logging.dfmoco2ur"))
            logger.addHandler(logging.StreamHandler())
            for l in config.get('logging'):
                level = config.get(f'logging.{l}')
                logging.getLogger(l).setLevel(level)
            
            asyncio.run(bridge.run(config))
    except FileNotFoundError as err:
        logging.critical(err)
        exit(1)