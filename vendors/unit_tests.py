import os
from main import download_file

def test_if_download_working_correctly():
    gt_url = "https://download.schneider-electric.com/files?p_enDocType=Firmware&p_File_Name=PM5560_PM5563_V2.7.4_Release.zip&p_Doc_Ref=PM5560_PM5563_V2.7.4_Release"
    dest = os.path.join(os.getcwd() ,"test_files")
    os.mkdir(dest)
    gt_file = "PM5560_PM5563_V2.7.4_Release.zip"
    gt_file_path = os.path.join(dest, gt_file)
    download_file(gt_url, gt_file_path)
    assert os.path.exists(gt_file_path)
    print("Image Download Test Passed")

if __name__=="__main__":
    test_if_download_working_correctly()