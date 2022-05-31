import os
import threading
import sqlite3

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

def filter_list(data):
    print(data)
    if(data[2] != temp_data[2] and data[3] != temp_data[3]):
        return True
    else:
        return False

def check_duplicates():
    db_name = 'firmwaredatabase.db'
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("select * from FWDB")
    data_list = cursor.fetchall()
    filtered_list = []
    for x in data_list:
        if(filter_list(x)):
            filtered_list.append(x)

    print(filtered_list)
    cursor.close()

def main():
    check_duplicates()
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