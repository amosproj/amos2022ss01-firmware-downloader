import os
import sys
sys.path.append(os.path.abspath(os.path.join('.', '')))

from multiprocessing import Pool
import json
from utils.Logs import get_logger


logger = get_logger("vendors.__init__")

data = {}
with open('config/config.json', 'r') as f:
    data = json.load(f)

vendors_path = 'vendors'

def job(file):
    os.system("python vendors/" + file)

def mod_runner(mod_name):
    job(mod_name+".py")

def runner(num_threads=2, skip_modules=[], whitelisted_modules=[]):
    logger.info(f"Enabled modules:")
    for mod in whitelisted_modules:
        logger.info(f"{mod}")

    
    with Pool(processes=num_threads) as pool:
        pool.map(mod_runner, whitelisted_modules)     

    
   
