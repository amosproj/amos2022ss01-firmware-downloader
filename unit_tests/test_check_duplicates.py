import os
import sys
import unittest
sys.path.append(os.path.abspath(os.path.join('.', '')))
import sqlite3
from utils.check_duplicates import check_duplicates
from utils.database import Database


def fetch_data():
    db_name = "firmwaredatabase.db"
    
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    try:
        cursor.execute("select * from FWDB")
    except sqlite3.Error as er:
        print('SQLite error:%s' % (' '.join(er.args)))

    data_list = cursor.fetchall()
    print(data_list)
    conn.close()
#https://sqliteviewer.flowsoft7.com/
class Unit_Case_Test(unittest.TestCase):
    def test_if_check_duplicates_working_correctly(self):
        temp_data = {
            'Manufacturer': 'GE',
            'Fwfilename': 'orbit-bkrc-9_2_2.mpk',
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
        self.assertTrue(check_duplicates(temp_data, 'firmwaredatabase.db'), msg="Data not exist")

    def test_if_check_duplicates_working_correctly_with_data_inserted(self):
        temp_data = {
            'Manufacturer': 'GE',
            'Fwfilename': 'orbit-bkrc-9_2_2.mpk',
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
        db_name = 'firmwaredatabase.db'
        db = Database()
        # Create a function for selenium output in dict format and return the dict. Pass it in the next line to insert the data
        db.insert_data(dbdictcarrier=temp_data)
        
        self.assertTrue(check_duplicates(temp_data, db_name), msg="Data not exist")


if __name__ == "__main__":
    fetch_data()
    unittest.main()

