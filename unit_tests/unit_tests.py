import os
import sys

sys.path.append(os.path.abspath(os.path.join('.', '')))
import sqlite3

from vendors.schneider_electric import download_single_file

def test_if_download_working_correctly():
    gt_url = "https://download.schneider-electric.com/files?p_enDocType=Firmware&p_File_Name=PM5560_PM5563_V2.7.4_Release.zip&p_Doc_Ref=PM5560_PM5563_V2.7.4_Release"
    dest = "test_files"
    if not os.path.isdir(dest):
        os.mkdir(dest)
    gt_file = "PM5560_PM5563_V2.7.4_Release.zip"
    gt_file_path = os.path.join(dest, gt_file)
    if os.path.exists(gt_file_path):
        os.remove(gt_file_path)
    download_single_file(gt_url, gt_file_path)
    assert os.path.exists(gt_file_path)
    print("Image Download Test Passed")

def test_if_data_entered_in_db_for_schneider_electric():
    dbname = "../firmwaredatabase.db"
    conn = sqlite3.connect(dbname)
    curs = conn.cursor()
    select_command = "select * from FWDB WHERE Manufacturer='schneider_electric'"
    curs.execute(select_command)
    records = len(curs.fetchall())
    assert records
    print(f"Database contains {records} firmwares for schneider_electric")
 

if __name__=="__main__":
    test_if_download_working_correctly()
    test_if_data_entered_in_db_for_schneider_electric()
