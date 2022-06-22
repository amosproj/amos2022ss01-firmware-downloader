from multiprocessing import Pool
from vendors import abb, ge, honeywell, schneider_electric

from utils.Logs import get_logger

logger = get_logger("vendors.__init__")
enabled_modules = [abb, ge, honeywell, schneider_electric]

def mod_runner(mod_name):
    for mod in enabled_modules:
        if mod.name == mod_name:
            logger.info(f"Starting {mod.name} downloader ...")
            mod.main()

def runner(num_threads=2, skip_modules=[]):
    logger.info(f"Enabled modules:")
    for mod in enabled_modules:
        logger.info(f"{mod.name}")
    mods_need_run = []
    for mod in enabled_modules:
        if mod.name in skip_modules:
            logger.info(f"Skipping {mod.name}")
            continue
        mods_need_run.append(mod.name)
    with Pool(processes=num_threads) as pool:
        pool.map(mod_runner, mods_need_run)
