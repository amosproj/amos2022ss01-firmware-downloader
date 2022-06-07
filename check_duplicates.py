import sqlite3

#check duplicate data for firmware web scrapping
def check_duplicates(firmware_data, db_name):
    #db connection
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    try:
        cursor.execute("select * from FWDB WHERE Manufacturer='" + firmware_data["Manufacturer"] + "' AND Modelname='" + firmware_data["Modelname"] + "' AND Version = '" + firmware_data["Version"] + "'")
    except sqlite3.Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))

    data_list = cursor.fetchall()
    conn.close()
    if(len(data_list) > 0):
        return True
    else:
        return False
 