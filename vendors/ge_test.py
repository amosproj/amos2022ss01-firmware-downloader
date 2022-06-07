import os
from ge import *

def test_if_download_working_correctly():
    data = ["orbit-mib-9_2_2.zip", "2022-05-12"]
    folder = 'File_system'
    file_name = 'orbit-mib-9_2_2.zip'
    gt_url = "https://www.gegridsolutions.com/communications/mds/software.asp?directory=Orbit_MCR&file=orbit%2Dmib%2D9%5F2%5F2%2Ezip"
    dest = os.path.join(os.getcwd() ,"test_files")
    try:
        if not os.path.isdir(dest):
            os.mkdir(dest)
    except Exception as e:
        raise ValueError(f"{e}")
    gt_file_path = os.path.join(dest, file_name)
    download_file(gt_url, gt_file_path, data[0], data[1], folder, file_name, '', '', '')
    print("Firmware Image Download Test Passed")

def test_if_download_working_correctly_selenium():
    data = ["SDx-6_4_8.mpk", "2022-03-29"]
    folder = 'File_system'
    file_name = 'SDx-6_4_8.mpk'
    gt_url = "https://www.gegridsolutions.com/communications/mds/software.asp?directory=SD_Series"
    dest = os.path.join(os.getcwd() ,"test_files")
    try:
        if not os.path.isdir(dest):
            os.mkdir(dest)
    except Exception as e:
        raise ValueError(f"{e}")
    gt_file_path = os.path.join(dest, file_name)
    download_file(gt_url, gt_file_path, data[0], data[1], folder, file_name, 'javascript:;', gt_url, "Passport_DownloadFile('SDSeries',7,70);return false")
    print("Firmware Image Download Test Passed")

if __name__=="__main__":
    test_if_download_working_correctly()
    test_if_download_working_correctly_selenium()