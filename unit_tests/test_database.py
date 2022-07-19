import sqlite3
import unittest
from utils.database import Database


class DatabaseUnitTest(unittest.TestCase):
    def test_case_db(self):
        db_name = "firmwaredatabase.db"
        db_ = Database()
        db_.db_check()
        # Pass the data dictionary in the next line to insert the data db connection
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        # Create a function for selenium output in dict format and return the dict
        firmware_data = {
            'Fwfileid': 'c1',
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
            'Fwadddata': 'some long sentence',
            'Uploadedonembark': False,
            'Embarkfileid': 'abc',
            'Startedanalysisonembark': False
        }
        db_.insert_data(dbdictcarrier=firmware_data)
        data = 'x'
        try:
            cursor.execute(
                "select * from FWDB WHERE Manufacturer='" + firmware_data["Manufacturer"] + "' AND Modelname='" +
                firmware_data["Modelname"] + "' AND Version = '" + firmware_data["Version"] + "'")
        except sqlite3.Error as er_:
            print('SQLite error: %s' % (' '.join(er_.args)))

        data_list = cursor.fetchall()
        conn.close()
        if len(data_list) > 0:
            print('good')
        else:
            print('Fail')
        print(' data -> %s : ' % data)
        self.assertTrue(len(data_list), msg="Data not found in database")


if __name__ == "__main__":
    unittest.main()
