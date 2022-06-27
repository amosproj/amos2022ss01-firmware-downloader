from multiprocessing import Pool
import os
import json
import schedule
import time
from utils.Logs import get_logger

logger = get_logger("vendors.__init__")

data = {}
with open('config/config.json', 'r') as f:
    data = json.load(f)

vendors_path = 'vendors'

def job(file):
    os.system("python vendors/" + file)

def scanner(file):
    if file.split('.')[0] in data:
        logger.info(f"Starting {file} downloader ...")
        schedule.every(data[file.split('.')[0]]['interval']).minutes.do(job, file)
    else:
        schedule.every(data['default']['interval']).minutes.do(job, file)

def mod_runner(mod_name):
    for file in os.listdir(vendors_path):
        if file.endswith(".py") and file != "__init__.py":
            if file.split('.')[0] in mod_name:
                scanner(file)    
    while True:
        schedule.run_pending()
        time.sleep(1)      

def runner(num_threads=2, skip_modules=[]):
    logger.info(f"Enabled modules:")
    for file in os.listdir(vendors_path):
        if file.endswith(".py") and file.split('.')[0] in data and file != "__init__.py":
            if file.split('.')[0] in skip_modules:
                logger.info(f"{file.split('.')[0]}")
    mods_need_run = []
    for file in os.listdir(vendors_path):
        if file.endswith(".py") and file.split('.')[0] in data and file != "__init__.py":
            if file.split('.')[0] in skip_modules:
                logger.info(f"Skipping {file.split('.')[0]}")
                continue
            mods_need_run.append(file.split('.')[0])
    
    # mod_runner(mods_need_run)
    with Pool(processes=num_threads) as pool:
        pool.map(mod_runner, mods_need_run)
    
   
