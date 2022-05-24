import os
import threading

#creating list of threads
threads = []

def main():
    vendors_path = './vendors'
    for file in os.listdir(vendors_path):
        if file.endswith(".py"):
            #creating thread
            process = threading.Thread(target = exec(open("./" + vendors_path + "/" + file).read()))
            #starting threa
            process.start()
            #appending thread to a list
            threads.append(process)
            continue
        else:
            continue
    
    #waiting until thread n completely executed
    for process in threads:
        process.join()


main()