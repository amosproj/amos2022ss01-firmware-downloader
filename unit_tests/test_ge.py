import os
import sqlite3
import sys
sys.path.append(os.path.abspath(os.path.join('.', '')))
from vendors.ge import *
import unittest
from utils.check_duplicates import check_duplicates

DB_NAME = "firmwaredatabase.db"
CONFIG_PATH = os.path.join("config", "config.json")
DATA={}
with open(CONFIG_PATH, "rb") as fp:
    DATA = json.load(fp)

def fetch_data():
    #DB connection
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("select * from FWDB WHERE Manufacturer='GE'")
    except sqlite3.Error as er_:
        print('SQLite error:%s' % (' '.join(er_.args)))

    data_list = cursor.fetchall()
    print(data_list)
    conn.close()

class GEUnitTest(unittest.TestCase):
    def test_case_without_authentication(self):
        files = ["orbit-mib-9_2_2.zip", "2022-05-12"]
        folder = DATA['file_paths']['dowload_test_files_path']
        file_name = 'orbit-mib-9_2_2'
        gt_url = "https://www.gegridsolutions.com/communications/mds/software.asp?directory=Orbit_MCR&file=orbit%2Dmib%2D9%5F2%5F2%2Ezip"
        dest = os.path.join(os.getcwd() ,folder)
        try:
            if not os.path.isdir(dest):
                os.mkdir(dest)
        except Exception as er_:
            raise ValueError("%s" % er_) from er_
        gt_file_path = os.path.join(dest, files[0])

        data = {
            'Manufacturer': 'GE',
            'Modelname': file_name,
            'Version': '',
	    }

        if os.path.isfile(gt_file_path) is False and check_duplicates(data, DB_NAME) is True:
            arg_data = {
                'url': gt_url, 
                'file_path_to_save': gt_file_path, 
                'data0': files[0], 
                'data1': files[1], 
                'filename': file_name, 
                'link': '', 
                'main_url': '', 
                'click': '', 
                'db_name': DB_NAME, 
                'is_file_download': True,
                'folder': folder
            }
            download_file(arg_data)
        else:
            arg_data = {
                'url': gt_url, 
                'file_path_to_save': gt_file_path, 
                'data0': files[0], 
                'data1': files[1], 
                'filename': file_name, 
                'link': '', 
                'main_url': '', 
                'click': '', 
                'db_name': DB_NAME, 
                'is_file_download': False,
                'folder': folder
            }
            download_file(arg_data)

        self.assertTrue(check_duplicates(data, DB_NAME), msg="Image didn't downloaded")
        fetch_data()

    def test_case_with_authentication(self):
        files = ["SDx-6_4_8.mpk", "2022-03-29"]
        folder = DATA['file_paths']['dowload_test_files_path']
        file_name = 'SDx-6_4_8'
        gt_url = "https://www.gegridsolutions.com/communications/mds/software.asp?directory=SD_Series"
        dest = os.path.join(os.getcwd() ,folder)
        try:
            if not os.path.isdir(dest):
                os.mkdir(dest)
        except Exception as er_:
            raise ValueError("%s" % er_) from er_
        gt_file_path = os.path.join(dest, files[0])

        data = {
            'Manufacturer': 'GE',
            'Modelname': file_name,
            'Version': '',
	    }
        gt_ex_file_path = os.path.join(gt_file_path, files[0])
        

        if os.path.isfile(gt_ex_file_path) is False and check_duplicates(data, DB_NAME) is True:
            arg_data = {
                'url': gt_url, 
                'file_path_to_save': gt_file_path, 
                'data0': files[0], 
                'data1': files[1], 
                'filename': file_name, 
                'link': 'javascript:;', 
                'main_url': gt_url, 
                'click': "Passport_DownloadFile('SDSeries',7,70);return false", 
                'db_name': DB_NAME, 
                'is_file_download': True,
                'folder': folder
            }
            download_file(arg_data)
        else:
            arg_data = {
                'url': gt_url, 
                'file_path_to_save': gt_file_path, 
                'data0': files[0], 
                'data1': files[1], 
                'filename': file_name, 
                'link': 'javascript:;', 
                'main_url': gt_url, 
                'click': "Passport_DownloadFile('SDSeries',7,70);return false", 
                'db_name': DB_NAME, 
                'is_file_download': False,
                'folder': folder
            }
            download_file(arg_data)

        self.assertTrue(check_duplicates(data, DB_NAME), msg="Image didn't downloaded")
        fetch_data()

if __name__=="__main__":
    unittest.main()
