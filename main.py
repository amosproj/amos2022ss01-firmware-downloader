import os
from scheduler import *
from vendors.ge import *
from vendors.honeywell import *
from vendors.schneider_electric import *
from vendors.abb import *
from vendors.asus import *
from vendors.avm import *

#creating list of threads
threads = []
vendors_path = './vendors'

def job():
    for file in os.listdir(vendors_path):
        if file.endswith(".py") and "test" not in file:
            scheduler(exec(open("./" + vendors_path + "/" + file).read()), 0.1)

if __name__ == "__main__":
    job()