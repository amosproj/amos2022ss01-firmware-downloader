import schedule
import os

def test_job():
    os.system("python vendors/ge.py")

if __name__ == "__main__":
    schedule.every(data['ge']['interval']).minutes.do(test_job)