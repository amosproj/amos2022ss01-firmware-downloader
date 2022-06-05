import os
import threading
from check_duplicates import check_duplicates

#creating list of threads
threads = []
temp_data = {
    'Fwfileid': 'FILE',
    'Manufacturer': 'GE',
    'Modelname': 'orbit-bkrc-9_2_2.mpk',
    'Version': '',
    'Type': '',
    'Releasedate': '2022-05-31',
    'Checksum': 'None',
    'Embatested': 'Yes',
    'Embalinktoreport': 'None',
    'Embarklinktoreport': 'https://xyz.com',
    'Fwdownlink': 'https://google.com',
    'Fwfilelinktolocal': './xyz/abc.tar',
    'Fwadddata': 'some long sentence'
}

def main():
    print(check_duplicates(temp_data))
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