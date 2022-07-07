import os
import sys
import unittest
sys.path.append(os.path.abspath(os.path.join('.', '')))
#import sqlite3
from utils.check_duplicates import check_duplicates
from utils.database import Database

#https://sqliteviewer.flowsoft7.com/
class Unit_Case_Test(unittest.TestCase):
    def test_if_check_duplicates_working_correctly(self):
        temp_data = {
            'Fwfileid': 'c',
            'Fwfilename': 'x',
            'Manufacturer': 'd',
            'Modelname': 'SZ-d',
            'Version': '1',
            'Type': 'Router',
            'Releasedate': '2022-05-31',
            'Checksum': 'None',
            'Embatested': 'Yes',
            'Embalinktoreport': 'None',
            'Embarklinktoreport': 'https://xyz.com',
            'Fwdownlink': 'https://google.com',
            'Fwfilelinktolocal': './xyz/abc.tar',
            'Fwadddata': 'some long sentence'
        }
        self.assertFalse(check_duplicates(temp_data, 'firmwaredatabase.db'), msg="Data not exist")

    def test_if_check_duplicates_working_correctly_with_data_inserted(self):
        db_name = 'firmwaredatabase.db'
        db = Database()
        if db_name not in os.listdir('.'):
            db.create_table()
        # Create a function for selenium output in dict format and return the dict. Pass it in the next line to insert the data
        db.insert_data(dbdictcarrier={
            'Fwfileid': 'FILE',
            'Fwfilename': 'Siemens ABC firmware',
            'Manufacturer': 'Siemens',
            'Modelname': 'SZ-100',
            'Version': '1.2.3',
            'Type': 'Router',
            'Releasedate': '2022-05-31',
            'Checksum': 'None',
            'Embatested': 'Yes',
            'Embalinktoreport': 'None',
            'Embarklinktoreport': 'https://xyz.com',
            'Fwdownlink': 'https://google.com',
            'Fwfilelinktolocal': './xyz/abc.tar',
            'Fwadddata': 'some long sentence'
        })
        temp_data = {
            'Fwfileid': 'FILE',
            'Fwfilename': 'Siemens ABC firmware',
            'Manufacturer': 'Siemens',
            'Modelname': 'SZ-100',
            'Version': '1.2.3',
            'Type': 'Router',
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

if __name__ == "__main__":
    unittest.main()