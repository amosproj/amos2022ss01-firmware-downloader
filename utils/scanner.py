import schedule
import time
import os
import json
from vendors.ge import *
from vendors.honeywell import *
from vendors.schneider_electric import *
from vendors.abb import *
from vendors.asus import *
from vendors.avm import *

def scanner():
  data = {}
  with open('config/config.json', 'r') as f:
    data = json.load(f)

  vendors_path = 'vendors'

  def job(file):  
    os.system("python vendors/" + file)

  for file in os.listdir(vendors_path):
    if file.endswith(".py") and "test":
      schedule.every(data[file.split('.')[0]]['interval']).minutes.do(job, file)

  while True:
      schedule.run_pending()
      time.sleep(1)