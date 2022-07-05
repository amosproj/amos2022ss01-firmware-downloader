import argparse
import json
import os
import schedule
import time
from vendors import runner
from utils.Logs import get_logger
from concurrent.futures import ThreadPoolExecutor

config_path = os.path.join("config", "config.json")
with open(config_path, "rb") as fp:
    config = json.load(fp)
logger = get_logger("main")
parser = argparse.ArgumentParser()
parser.add_argument("--num-threads", type=int, default=2, help="Number of parallel executing modules")
args = parser.parse_args()
vendors_path = 'vendors'

def get_skipped_modules(config):
    mods = list()
    for mod in os.listdir(vendors_path):
        if mod.endswith(".py") and mod != "__init__.py":
            if mod.split('.')[0] in config:
                if config[mod.split('.')[0]]["ignore"] == True:
                    mods.append(mod.split('.')[0])
            else:
                if config['default']['ignore'] == True:
                    mods.append(mod.split('.')[0])
               
    return mods

def executor_job(mod):
    _ = executor.submit(runner, mod) 

if __name__ == "__main__":
    logger.info("Starting runner...")
    num_threads = args.num_threads
    skip_modules = get_skipped_modules(config)
    print("Following modules are skipped")
    print(skip_modules)

    whitelisted_modules = []
    for file in os.listdir(vendors_path):
        if file.endswith(".py") and file.split('.')[0] in config and file != "__init__.py":
            if file.split('.')[0] in skip_modules:
                logger.info(f"Skipping {file.split('.')[0]}")
                continue
            whitelisted_modules.append(file.split('.')[0])

    with ThreadPoolExecutor(num_threads) as executor:
        for mod in whitelisted_modules:
            if mod in config:
                logger.info(f"Starting {mod} downloader ...")
                schedule.every(config[mod]['interval']).minutes.do(executor_job, mod)
            else:
                schedule.every(config['default']['interval']).minutes.do(executor_job, mod)
        while True:
            schedule.run_pending()
            time.sleep(1)