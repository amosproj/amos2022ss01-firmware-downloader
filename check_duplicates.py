import sqlite3

def filter_list(data, firmware_data):
    print(data)
    if(data[2] == firmware_data[2] and data[3] != firmware_data[3]):
        return True
    else:
        return False

#check duplicate data for firmware web scrapping
def check_duplicates(firmware_data):
    db_name = 'firmwaredatabase.db'
    #db connection
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    #data selection query from db
    cursor.execute("select * from FWDB")
    data_list = cursor.fetchall()
    filtered_list = []
    for x in data_list:
        if(filter_list(x, firmware_data)):
            filtered_list.append(x)

    print(filtered_list)
    cursor.close()