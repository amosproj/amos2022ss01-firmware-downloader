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
    mods = []
    for mod in os.listdir(vendors_path):
        if mod.endswith(".py") and mod != "__init__.py":
            if mod.split('.')[0] in config:
                if config[mod.split('.')[0]]["ignore"] is True:
                    mods.append(mod.split('.')[0])
            else:
                if config['default']['ignore'] is True:
                    mods.append(mod.split('.')[0])       
    return mods

def executor_job(mod_):
    _ = executor.submit(runner, mod_) 

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
        for module in whitelisted_modules:
            if module in config:
                logger.info(f"Starting {module} downloader ...")
                schedule.every(config[module]['interval']).minutes.do(executor_job, module)
            else:
                schedule.every(config['default']['interval']).minutes.do(executor_job, module)
        while True:
            schedule.run_pending()
            time.sleep(1)