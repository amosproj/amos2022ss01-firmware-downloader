import argparse
import json
import os
import schedule
import time
from utils.Logs import get_logger
from concurrent.futures import ThreadPoolExecutor

def job(file):
    os.system("python vendors/" + file)

def mod_runner(mod_name):
    job(mod_name+".py")

def runner(mod):
    mod_runner(mod)

config_path = os.path.join("config", "config.json")
with open(config_path, "rb") as fp:
    config = json.load(fp)
logger = get_logger("main")
parser = argparse.ArgumentParser()
parser.add_argument("--num-threads", type=int, default=2, help="Number of parallel executing modules")
args = parser.parse_args()
VENDORS_FILE = 'vendors'

def get_skipped_modules():
    mods = []
    for mod in os.listdir(VENDORS_FILE):
        if mod.endswith(".py"):
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
    skip_modules = get_skipped_modules()
    print("Following modules are skipped")
    print(skip_modules)

    whitelisted_modules = []
    for file in os.listdir(VENDORS_FILE):
        if file.endswith(".py") and file.split('.')[0] in config:
            if file.split('.')[0] in skip_modules:
                logger.info("Skipping %s", file.split('.')[0])
                continue
            whitelisted_modules.append(file.split('.')[0])

    with ThreadPoolExecutor(num_threads) as executor:
        for module in whitelisted_modules:
            if module in config:
                logger.info("Starting %s downloader ...", module)
                schedule.every(config[module]['interval']).minutes.do(executor_job, module)
            else:
                schedule.every(config['default']['interval']).minutes.do(executor_job, module)
        while True:
            schedule.run_pending()
            time.sleep(1)
