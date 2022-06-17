import schedule
import os
import json
import time
import unittest

data = {}
with open('config.json', 'r') as f:
    data = json.load(f)

def test_job(self, is_true):
    os.system("python vendors/asus.py")
    self.assertTrue(is_true, msg="Scheduling not working")

class Schedule_Test(unittest.TestCase):
    
    def testing_scanner(self):
        schedule.every(data['asus']['interval']).minutes.do(test_job, self, True)
        
        while True:
            schedule.run_pending()
            time.sleep(1)

if __name__ == "__main__":
    unittest.main()