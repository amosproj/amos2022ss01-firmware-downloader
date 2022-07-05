import os
import sys
sys.path.append(os.path.abspath(os.path.join('.', '')))
from utils.database import Database
import sqlite3
import unittest
from vendors.schneider_electric import download_single_file
#from utils.check_duplicates import check_duplicates

db_name = "../firmwaredatabase.db"


def fetch_data():
    db = Database(dbname=db_name)
    if db_name not in os.listdir('.'):
        db.create_table()
    # db connection
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    try:
        cursor.execute("select * from FWDB WHERE Manufacturer='schneider_electric'")
    except sqlite3.Error as er:
        print('SQLite error:%s' % (' '.join(er.args)))

    data_list = cursor.fetchall()
    print(data_list)
    conn.close()


class Unit_Case_Test(unittest.TestCase):
    def test_if_download_working_correctly(self):
            gt_url = "https://download.schneider-electric.com/files?p_enDocType=Firmware&p_File_Name=PM5560_PM5563_V2.7.4_Release.zip&p_Doc_Ref=PM5560_PM5563_V2.7.4_Release"
            dest = "test_files"
            if not os.path.isdir(dest):
                os.mkdir(dest)
            gt_file = "PM5560_PM5563_V2.7.4_Release.zip"
            gt_file_path = os.path.join(dest, gt_file)
            if os.path.exists(gt_file_path):
                os.remove(gt_file_path)
            download_single_file(gt_url, gt_file_path)
            self.assertTrue(os.path.exists(gt_file_path), msg="Path not exists")

    def test_if_data_entered_in_db_for_schneider_electric(self):
            conn = sqlite3.connect(db_name)
            curs = conn.cursor()
            select_command = "select * from FWDB WHERE Manufacturer='schneider_electric'"
            curs.execute(select_command)
            records = len(curs.fetchall())
            self.assertTrue(records, msg="Record not exists")
            print(f"Database contains {records} firmwares for schneider_electric")


if __name__ == "__main__":
    fetch_data()
    unittest.main()