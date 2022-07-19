import argparse
import json
import os
import time
from concurrent.futures import ThreadPoolExecutor
import schedule
from utils.Logs import get_logger
from uploader.upload import FirmwareUploader

config_path = os.path.join("config", "config.json")
with open(config_path, "rb") as fp:
    config = json.load(fp)
logger = get_logger("main")
parser = argparse.ArgumentParser()
parser.add_argument("--num-threads", type=int, default=2, help="Number of parallel executing modules")
args = parser.parse_args()
VENDORS_FILE = 'vendors'


def runner(mod):
    os.system("python vendors/" + mod + ".py")
    fw_ = FirmwareUploader()
    fw_.anaylise_data_file("firmwaredatabase.db")


def executor_job(mod_, executor):
    _ = executor.submit(runner, mod_)


def thread_pool(num_threads_, whitelisted_modules_):
    with ThreadPoolExecutor(num_threads_) as executor:
        for module in whitelisted_modules_:
            if module in config:
                logger.info("Starting %s downloader ...", module)
                schedule.every(config[module]['interval']).minutes.do(executor_job, module, executor)
            else:
                schedule.every(config['default']['interval']).minutes.do(executor_job, module, executor)
        while True:
            schedule.run_pending()
            time.sleep(1)


def get_modules(skip):
    mods = []
    for mod in os.listdir(VENDORS_FILE):
        if mod.endswith(".py"):
            if mod.split('.')[0] in config:
                if config[mod.split('.')[0]]["ignore"] is True and skip is True:
                    mods.append(mod.split('.')[0])
                elif config[mod.split('.')[0]]["ignore"] is False and skip is False:
                    mods.append(mod.split('.')[0])
            else:
                if config['default']['ignore'] is True and skip is True:
                    mods.append(mod.split('.')[0])
                elif config['default']['ignore'] is False and skip is False:
                    mods.append(mod.split('.')[0])
    return mods


if __name__ == "__main__":
    logger.info("Starting runner...")
    num_threads = args.num_threads
    whitelisted_modules = []
    skip_modules = []
    skip_modules = get_modules(True)
    whitelisted_modules = get_modules(False)
    print("Following modules are skipped")
    print(skip_modules)
    print("Following modules are enabled")
    print(whitelisted_modules)
    thread_pool(num_threads, whitelisted_modules)
