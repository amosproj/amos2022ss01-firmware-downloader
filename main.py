import argparse
import json
import os

from vendors import runner
from utils.Logs import get_logger

config_path = os.path.join("config", "config.json")
with open(config_path, "rb") as fp:
    config = json.load(fp)
logger = get_logger("main")
parser = argparse.ArgumentParser()
parser.add_argument("--num-threads", type=int, default=2, help="Number of parallel executing modules")
args = parser.parse_args()

def get_skipped_modules(config):
    mods = list()
    for mod in config:
        if config[mod].get("ignore", False):
            mods.append(mod)
    return mods

if __name__ == "__main__":
    logger.info("Starting runner...")
    num_threads = args.num_threads
    skip_modules = get_skipped_modules(config)
    print("Following modules are skipped")
    print(skip_modules)
    runner(num_threads=num_threads, skip_modules=skip_modules)
