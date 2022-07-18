import argparse
import json
import logging
import os
import inspect
import sys
from utils.Logs import get_logger
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

config_path = os.path.join(parent_dir, "config", "config.json")
with open(config_path, "rb") as fp:
    config = json.load(fp)
logger = get_logger("main")
parser = argparse.ArgumentParser()
parser.add_argument("--num-threads", type=int, default=2, help="Number of parallel executing modules")
args = parser.parse_args()
VENDORS_FILE = 'vendors'



def config_check(mod, var1):
    if mod in config: # ge
        if config[mod][var1]:
            # present
            # print('-> %s present %s', var1, config[mod][var1])
            return 1
        else:
            # none
            # print('none')
            # print('-> %s present %s', var1, config[mod][var1])
            return 0
    else: #gee
        if config['default'][var1]:
            # through fallback error
            # print('fallback')
            return 2


def config_check_all():
    for mod in os.listdir(VENDORS_FILE):
        print('url %s ', config_check(mod.split('.')[0], 'url'))
        print('abc %s :', mod.split('.')[0])
        if (config_check(mod.split('.')[0], 'url')):
            print('logging')
            logging.info('module : %s -> url  present', mod.split('.')[0])
        else:
            print('error')
            logging.error('module : %s -> url not present', mod.split('.')[0])

        print('user %S ', config_check(mod.split('.')[0], 'user'))
        if config_check(mod.split('.')[0], 'user'):
            logging.info('module : %s -> user  present', mod.split('.')[0])
        else:
            logging.error('module : %s -> user not present', mod.split('.')[0])

        print('password %S ', config_check(mod.split('.')[0], 'password'))
        if config_check(mod.split('.')[0], 'password'):
            logging.info('module : %S -> password  present', mod.split('.')[0])
        else:
            logging.error('module : %s -> password not present', mod.split('.')[0])


def vendor_field(mod,field):
    if config_check(mod,field):
        return config[mod][field]
    else:
        if config_check('default' ,field):
            return config['default'][field]
        else:
            return False
