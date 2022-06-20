import schedule
import os
import json
import time
import unittest

data = {}
with open('config/config.json', 'r') as f:
    data = json.load(f)

def test_job(self, is_true, file):
    os.system("python vendors/"+file)
    self.assertTrue(is_true, msg="Scheduling not working")

class Schedule_Test(unittest.TestCase):
    
    def testing_scanner(self):
        schedule.every(data['asus']['interval']).minutes.do(test_job, self, True, 'asus.py')
        schedule.every(data['avm']['interval']).minutes.do(test_job, self, True, 'avm.py')
        schedule.every(data['ge']['interval']).minutes.do(test_job, self, True, 'ge.py')
        
        i=0
        while i != 10:
            schedule.run_pending()
            time.sleep(1)
            i=i+1

if __name__ == "__main__":
    unittest.main()