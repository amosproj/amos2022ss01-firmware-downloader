import os
import threading
from check_duplicates import check_duplicates

#creating list of threads
threads = []
temp_data = [
        'FILE',
        'Siemens',
        'SZ-100',
        '1.2.3',
        'Router',
        '2022-05-24',
        'None',
        'Yes',
        'None',
        'https://xyz.com',
        'https://google.com',
        './xyz/abc.tar',
        'some long sentence'
]

def main():
    check_duplicates(temp_data)
    vendors_path = './vendors'
    for file in os.listdir(vendors_path):
        if file.endswith(".py"):
            #creating thread
            process = threading.Thread(target = exec(open("./" + vendors_path + "/" + file).read()))
            #starting thread
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