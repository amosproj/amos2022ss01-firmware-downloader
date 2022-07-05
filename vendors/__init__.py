import os
import sys
sys.path.append(os.path.abspath(os.path.join('.', '')))

from multiprocessing import Pool
import json
from utils.Logs import get_logger


logger = get_logger("vendors.__init__")

data = {}
config_path = os.path.join("config", "config.json")
with open(config_path, "rb") as fp:
    config = json.load(fp)

vendors_path = 'vendors'

def job(file):
    os.system("python vendors/" + file)

def mod_runner(mod_name):
    job(mod_name+".py")

def runner(mod):
    mod_runner(mod)  

    
   
