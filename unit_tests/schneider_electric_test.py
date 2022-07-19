import os
import sys
import sqlite3
import unittest
import json
from vendors.schneider_electric import download_single_file, write_metadata_to_db
from utils.check_duplicates import Database

sys.path.append(os.path.abspath(os.path.join('.', '')))

DB_NAME = os.path.join(os.getcwd(), "schneiderelectrictempfirmware.db")
CONFIG_PATH = os.path.join("config", "config.json")
DATA={}
with open(CONFIG_PATH, "rb") as fp:
    DATA = json.load(fp)

def setup_db():
    db_ = Database(db_path=DB_NAME)
    db_.db_check()
    db_.create_table()

class SchneiderUnitTest(unittest.TestCase):
    def setUp(self):
        setup_db()
        dest = DATA['file_paths']['download_test_files_path']
        if not os.path.isdir(dest):
            os.mkdir(dest)
        gt_file = "PM5560_PM5563_V2.7.4_Release.zip"  #Firmware_1.10.0_5500AC2.zip
        self.gt_file_path = os.path.join(dest, gt_file)
        self.gt_url = "https://download.schneider-electric.com/files?p_enDocType=Firmware&p_File_Name=PM5560_PM5563_V2.7.4_Release.zip&p_Doc_Ref=PM5560_PM5563_V2.7.4_Release"
        # remove all schneider electric data in test database
        delete_command = "DELETE FROM FWDB where Manufacturer='schneider_electric'"
        conn = sqlite3.connect(DB_NAME)
        curs = conn.cursor()
        curs.execute(delete_command)

    def test_download(self):
        if os.path.exists(self.gt_file_path):
            os.remove(self.gt_file_path)
        download_single_file(self.gt_url, self.gt_file_path, {})
        self.assertTrue(os.path.exists(self.gt_file_path), msg="Path not exists")

    def test_if_data_entered_in_db(self):
        dummy_data = {
            'Fwfileid': 'FILE',
            'Fwfilename': "testfile",
            'Manufacturer': 'schneider_electric',
            'Modelname': "1.0.0",
            'Version': "1.0.0",
            'Type': "firmware",
            'Releasedate': "",
            'Checksum': '',
            'Embatested': '',
            'Embalinktoreport': '',
            'Embarklinktoreport': '',
            'Fwdownlink': "https://test.com/firmware.zip",
            'Fwfilelinktolocal': self.gt_file_path,
            'Fwadddata': '',
            'Uploadedonembark': False,
            'Embarkfileid': '',
            'Startedanalysisonembark': False
	}
        conn = sqlite3.connect(DB_NAME)
        curs = conn.cursor()
        select_command = "select * from FWDB WHERE Manufacturer='schneider_electric'"
        curs.execute(select_command)
        records = len(curs.fetchall())
        #Make sure no record exist for schneider_electric
        self.assertEqual(records, 0,msg="There should be no record in db")
        # Add data for schneider electric
        write_metadata_to_db([dummy_data], db_path=DB_NAME)
        # Now test if one record exist for schneider_electric
        curs.execute(select_command)
        records = len(curs.fetchall())
        self.assertEqual(records, 1 , msg="There should be only one record in db")
        print(f"Database contains {records} firmwares for schneider_electric")

    def tearDown(self):
        if os.path.exists(DB_NAME):
            os.remove(DB_NAME)

if __name__ == "__main__":
    unittest.main()
