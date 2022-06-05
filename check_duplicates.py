import sqlite3

#check duplicate data for firmware web scrapping
def check_duplicates(firmware_data):
    db_name = 'firmwaredatabase.db'
    #db connection
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    print(firmware_data["Manufacturer"])
    if(len(firmware_data["Version"]) > 0):
        #data selection query from
        try:
            cursor.execute("select * from FWDB WHERE Manufacturer='" + firmware_data["Manufacturer"] + "' AND Modelname='" + firmware_data["Modelname"] + "' AND Version = '" + firmware_data["Version"] + "'")
        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
    else:
        try:
            cursor.execute("select * from FWDB WHERE Manufacturer='" + firmware_data["Manufacturer"] + "' AND Modelname='" + firmware_data["Modelname"] + "'")
        except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))


    data_list = cursor.fetchall()

    print(data_list)
    conn.close()
    if(len(data_list) > 0):
        return True
    else:
        return False
 