import unittest
from utils.check_duplicates import check_duplicates
from utils.database import Database

#https://sqliteviewer.flowsoft7.com/
class CheckDuplicatesUnitTest(unittest.TestCase):
    def test_check_duplicates(self):
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

    def test_check_duplicates_with_data(self):
        db_ = Database()
        db_.db_check()
        # Create a function for selenium output in dict format and return the dict. Pass it in the next line to insert the data
        db_.insert_data(dbdictcarrier={
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
