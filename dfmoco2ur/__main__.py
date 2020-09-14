import logging
import argparse
import yaml
from pathlib import Path
from xdg import XDG_CONFIG_HOME
from dfmoco2ur import bridge
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
            config = yaml.load(raw_config, Loader=yaml.FullLoader)

            # Setup logging
            # TODO: We might want to send our logs out via a Websocket.
            for logger in config['logging']:
                if logger == "dfmoco2ur":
                    logging.basicConfig(level=config['logging'][logger])
                else:
                    logging.getLogger(logger).setLevel(config['logging'][logger])

            if args.config == default_config_path:
                logging.info(f"Using default configuration from {args.config}")
            else:
                logging.debug(f"Using custom configuration from {args.config}")

            asyncio.run(bridge.run(config))
    except FileNotFoundError as err:
        logging.critical(err)
        exit(1)
