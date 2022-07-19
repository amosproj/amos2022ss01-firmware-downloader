import json
import os
import inspect
import sys
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
config_path = os.path.join(parent_dir, "config", "config.json")
with open(config_path, "rb") as fp:
    config = json.load(fp)


def config_check(mod, var1):
    if mod in config:
        if config[mod][var1]:
            return 1
        else:
            return 0
    else:
        if config['default'][var1]:
            return 2
    return None


def vendor_field(mod,field):
    if config_check(mod,field):
        return config[mod][field]
    else:
        if config_check('default', field):
            return config['default'][field]
        else:
            return False
