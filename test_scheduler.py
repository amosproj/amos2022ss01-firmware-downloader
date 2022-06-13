from scheduler import scheduler

def job():
    print("Every 10 seconds it will run")

if __name__ == "__main__":
    scheduler(job, 0.1)