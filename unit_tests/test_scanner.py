import schedule
import os
import json
import time
import unittest

data = {}
with open('config/test_config.json', 'r') as f:
    data = json.load(f)

def test_job(self, is_true, file):
    os.system("python vendors/"+file)
    self.assertTrue(is_true, msg="Scheduling not working")

class Scanner_Test(unittest.TestCase):
    
    def testing_scanner(self):
        if('asus' in data):
            schedule.every(data['asus']['interval']).minutes.do(test_job, self, True, 'asus.py')
        else:
            schedule.every(data['default']['interval']).minutes.do(test_job, self, True, 'asus.py')
        
        if('avm' in data):
            schedule.every(data['avm']['interval']).minutes.do(test_job, self, True, 'avm.py')
        else:
            schedule.every(data['default']['interval']).minutes.do(test_job, self, True, 'avm.py')
       
        if('ge' in data):
            schedule.every(data['ge']['interval']).minutes.do(test_job, self, True, 'ge.py')
        else:
            schedule.every(data['default']['interval']).minutes.do(test_job, self, True, 'ge.py')
        
        i=0
        while i != 3:
            schedule.run_pending()
            time.sleep(1)
            i=i+1

if __name__ == "__main__":
    unittest.main()