import os
import sqlite3
import sys
sys.path.append(os.path.abspath(os.path.join('.', ''))) 
from vendors.ge import *
from utils.database import Database
import unittest
from utils.check_duplicates import check_duplicates

db_name = "test_firmwaredatabase.db"

def fetch_data():
    db = Database(dbname=db_name)
    if db_name not in os.listdir('.'):
        db.create_table()
    #db connection
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    try:
        cursor.execute("select * from FWDB WHERE Manufacturer='GE'")
    except sqlite3.Error as er:
        print('SQLite error:%s' % (' '.join(er.args)))

    data_list = cursor.fetchall()
    print(data_list)
    conn.close()

class Unit_Case_Test(unittest.TestCase):
    def test_case_without_authentication(self):
        files = ["orbit-mib-9_2_2.zip", "2022-05-12"]
        folder = 'Test_File_system'
        file_name = 'orbit-mib-9_2_2'
        gt_url = "https://www.gegridsolutions.com/communications/mds/software.asp?directory=Orbit_MCR&file=orbit%2Dmib%2D9%5F2%5F2%2Ezip"
        dest = os.path.join(os.getcwd() ,folder)
        try:
            if not os.path.isdir(dest):
                os.mkdir(dest)
        except Exception as e:
            raise ValueError(f"{e}")
        gt_file_path = os.path.join(dest, files[0])

        data = {
            'Manufacturer': 'GE',
            'Modelname': file_name,
            'Version': '',
	    }

        if os.path.isfile(gt_file_path) == False and check_duplicates(data, db_name) == True:
            download_file(gt_url, gt_file_path, files[0], files[1], folder, file_name, '', '', '', db_name, True)
        else:
            download_file(gt_url, gt_file_path, files[0], files[1], folder, file_name, '', '', '', db_name, False)
       
        
        self.assertTrue(check_duplicates(data, db_name), msg="Image didn't downloaded")
        fetch_data()
        

    def test_case_with_authentication(self):
        files = ["SDx-6_4_8.mpk", "2022-03-29"]
        folder = 'Test_File_system'
        file_name = 'SDx-6_4_8'
        gt_url = "https://www.gegridsolutions.com/communications/mds/software.asp?directory=SD_Series"
        dest = os.path.join(os.getcwd() ,folder)
        try:
            if not os.path.isdir(dest):
                os.mkdir(dest)
        except Exception as e:
            raise ValueError(f"{e}")
        gt_file_path = os.path.join(dest, files[0])

        data = {
            'Manufacturer': 'GE',
            'Modelname': file_name,
            'Version': '',
	    }
        gt_ex_file_path = os.path.join(gt_file_path, files[0]) 
       
        if (os.path.isfile(gt_ex_file_path) == False and check_duplicates(data, db_name) == True):
            download_file(gt_url, gt_file_path, files[0], files[1], folder, file_name, 'javascript:;', gt_url, "Passport_DownloadFile('SDSeries',7,70);return false", db_name, True)
        else:
            download_file(gt_url, gt_file_path, files[0], files[1], folder, file_name, 'javascript:;', gt_url, "Passport_DownloadFile('SDSeries',7,70);return false", db_name, False)
        
        
        self.assertTrue(check_duplicates(data, db_name), msg="Image didn't downloaded")
        fetch_data()
        

if __name__=="__main__":
    unittest.main()