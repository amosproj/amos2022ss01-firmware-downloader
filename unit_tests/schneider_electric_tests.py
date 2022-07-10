import os
import sys
import sqlite3
import unittest
import json
sys.path.append(os.path.abspath(os.path.join('.', '')))
from vendors.schneider_electric import download_single_file
from utils.check_duplicates import check_duplicates

DB_NAME = "firmwaredatabase.db"
CONFIG_PATH = os.path.join("config", "config.json")
DATA={}
with open(CONFIG_PATH, "rb") as fp:
    DATA = json.load(fp)

def fetch_data():
    # db connection
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("select * from FWDB WHERE Manufacturer='schneider_electric'")
    except sqlite3.Error as er_:
        print('SQLite error:%s' % (' '.join(er_.args)))

    data_list = cursor.fetchall()
    print(data_list)
    conn.close()


class SchneiderUnitTest(unittest.TestCase):
    def test_download(self):
            gt_url = "https://download.schneider-electric.com/files?p_enDocType=Firmware&p_File_Name=PM5560_PM5563_V2.7.4_Release.zip&p_Doc_Ref=PM5560_PM5563_V2.7.4_Release"
            dest = DATA['file_paths']['dowload_test_files_path']
            if not os.path.isdir(dest):
                os.mkdir(dest)
            gt_file = "PM5560_PM5563_V2.7.4_Release.zip"  #Firmware_1.10.0_5500AC2.zip
            gt_file_path = os.path.join(dest, gt_file)
            if os.path.exists(gt_file_path):
                os.remove(gt_file_path)
            download_single_file(gt_url, gt_file_path)
            self.assertTrue(os.path.exists(gt_file_path), msg="Path not exists")
            fetch_data()

    def test_if_data_entered_in_db(self):
            conn = sqlite3.connect(DB_NAME)
            curs = conn.cursor()
            select_command = "select * from FWDB WHERE Manufacturer='schneider_electric'"
            curs.execute(select_command)
            records = len(curs.fetchall())
            self.assertFalse(records, msg="Record not exists")
            print(f"Database contains {records} firmwares for schneider_electric")

    def test_for_check_dublicates(self):
        file_name = 'EPDU_SP1_HC_V2010'
        data = {
            'Manufacturer': 'schneider_electric',
            'Modelname': file_name,
            'Version': '',
        }
        self.assertFalse(check_duplicates(data, DB_NAME), msg="Image didn't downloaded")
        fetch_data()


if __name__ == "__main__":
    unittest.main()
