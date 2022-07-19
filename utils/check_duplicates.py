import sqlite3
from utils.database import Database

#check duplicate data for firmware web scrapping
def check_duplicates(firmware_data, db_name):
    db_ = Database()
    db_.db_check()
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    try:
        cursor.execute("select * from FWDB WHERE Manufacturer='" + firmware_data["Manufacturer"] + "' AND Modelname='" + firmware_data["Modelname"] + "' AND Version = '" + firmware_data["Version"] + "'")
    except sqlite3.Error as er_:
        print('SQLite error: %s' % (' '.join(er_.args)))
        return False

    data_list = cursor.fetchall()
    conn.close()

    return len(data_list) > 0
