import schedule
import time
import os
import json
from scheduler import *
from vendors.ge import *
from vendors.honeywell import *
from vendors.schneider_electric import *
from vendors.abb import *
from vendors.asus import *
from vendors.avm import *

data = {}
with open('config.json', 'r') as f:
  data = json.load(f)

vendors_path = './vendors'

def asus():
  exec(open("./" + vendors_path + "/asus.py").read())

def avm():
  exec(open("./" + vendors_path + "/avm.py").read())


schedule.every(data['asus']['interval']).minutes.do(asus)
schedule.every(data['avm']['interval']).minutes.do(avm)

while True:
  schedule.run_pending()
  time.sleep(1)