import logging
import argparse
import yaml
import sys
from pathlib import Path
from xdg import XDG_CONFIG_HOME
from dfmoco2ur import scheduler


if __name__ == '__main__':

    # Resolve the default config path using XDG and alternatively $HOME/.config followed by dfmoco-ur/config.yaml
    base_path = Path(XDG_CONFIG_HOME)
    if not base_path:
        base_path = Path.home().joinpath('.config')
    default_config_path = base_path.joinpath('dfmoco-ur', 'config.yaml')

    # Parse CLI arguments to obtain the config and log level
    parser = argparse.ArgumentParser(description='Dragonframe Motion Control to Universal Robot bridge', prefix_chars='-')
    parser.add_argument('--config', default=default_config_path, help='Path to a configuration')
    parser.add_argument('--logLevel', type=int, default=10, help='Log level according to the python logging module')
    args = parser.parse_args()

    # Setup logging
    # TODO: We might want to send our logs out via a Websocket.
    logging.basicConfig(level=args.logLevel)

    # Parse the configuration and run the scheduler
    if args.config == default_config_path:
        logging.info(f"Using default configuration from {args.config}")
    else:
        logging.debug(f"Using custom configuration from {args.config}")
    try:
        with open(args.config, 'r') as raw_config:
            config = yaml.load(raw_config, Loader=yaml.FullLoader)
            scheduler.run(config)
    except FileNotFoundError as err:
        logging.critical(err)
        sys.exit(1)
