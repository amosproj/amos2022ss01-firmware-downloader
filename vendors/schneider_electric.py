import os
import math
import re
import uuid
import sys
import traceback
sys.path.append(os.path.abspath(os.path.join('.', '')))
from utils.Logs import get_logger

import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import parse_qs, urlparse
from utils.check_duplicates import *
from utils.database import Database
#from vendors import download_list_files

#Logger
name = "schneider_electric"
logger = get_logger("vendors.schneider_electric")
CONFIG_PATH = os.path.join("config", "config.json")
DATA={}
with open(CONFIG_PATH, "rb") as fp:
    DATA = json.load(fp)

def download_single_file(url, file_path_to_save):
    logger.info(f"Downloading {url} and saving as {file_path_to_save}")
    resp = requests.get(url, allow_redirects=True)
    if resp.status_code != 200:
        raise ValueError("Invalid Url or file not found")
    with open(file_path_to_save, "wb") as f:
        f.write(resp.content)

def download_list_files(metadata, max_files=-1): #max_files -1 means download all files
    if max_files == -1:
        max_files = len(metadata)
    if max_files > len(metadata):
        max_files = len(metadata)
    for file_ in range(max_files):
        download_single_file(metadata[file_]["Fwdownlink"], metadata[file_]["Fwfilelinktolocal"])

def write_metadata_to_db(metadata):
    logger.info("Going to write metadata in db")
    db = Database()
    for fw in metadata:
        db.insert_data(dbdictcarrier=fw)

def se_get_total_firmware_count(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    items = soup.find_all("label", class_="dn-check dn-selected")
    for item in items:
        if item.get("for") == "docTypeFilters-1555893":
            innerHtml =item.decode_contents()
            numbers = re.findall(r'\b\d+\b', innerHtml)
            count = int(numbers[0])
            logger.info(f"Found total {count} firmwares")
            return count

def get_firmware_data_using_api(url, fw_count, fw_per_page):
    if fw_count < fw_per_page:
        fw_pr_page = fw_count
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    total_pages = math.ceil(fw_count/fw_per_page)
    fw_list = list()
    for page in range(1, total_pages+1):

        req_body= {
            "data": f"docType=1555893-Firmware_COMMA_language=en_GB-English_COMMA_sortByField=Document_Date_New_COMMA_itemsPerPage={fw_per_page}_COMMA_pageNumber={page}_COMMA_COMMA_keyword=",
            "buisnessId": ""
        }
        response = requests.post(url, data=req_body, headers=headers)
        if response.status_code != 200:
            logger.info(f"Invalid API response with status_code = {response.status_code}")
            raise ValueError(f"Invalid API response with status_code = {response.status_code}")
        if page != total_pages:
            logger.info(f"Received metadata for {page*fw_per_page}/{fw_count}")
        else:
            logger.info(f"Received metadata for all {fw_count}/{fw_count} firmwares")
        fw_list += response.json()["docList"]
    return fw_list

def transform_metadata_format_ours(raw_data, local_storage_dir="."):
    fw_mod_list = list()
    for fw in raw_data:
        fw_mod = {
            'Fwfileid': 'FILE',
            'Fwfilename': str(fw.get("title", "").replace("'", "").replace(" ", "_")),
            'Manufacturer': 'schneider_electric',
            'Modelname': str(fw.get("title", "").replace("'", "").replace(" ", "_")),
            'Version': str(fw.get("version", "").replace(" ", "_")),
            'Type': str(fw.get("documentTypeEnglishLabel", "").replace(" ", "_")),
            'Releasedate': fw.get("docDate", ""),
            'Checksum': '',
            'Embatested': '',
            'Embalinktoreport': '',
            'Embarklinktoreport': '',
            'Fwdownlink': "https:" + fw.get("downloadUrl", ""),
            'Fwfilelinktolocal': os.path.join(local_storage_dir, parse_qs(urlparse(fw.get("downloadUrl")).query, keep_blank_values=True).get("p_File_Name", list(str(uuid.uuid4())))[0].replace(" ", "_").replace("'", "") ),
            'Fwadddata': ''
	    }
        db_name = 'firmwaredatabase.db'
        if (check_duplicates(fw_mod, db_name) == False):
            fw_mod_list.append(fw_mod)
    return fw_mod_list

# This method is outdated as of now.
def se_firmaware_parser(url, folder):
    dest = os.path.join(os.getcwd(), folder)
    try:
        if not os.path.isdir(dest):
            os.mkdir(dest)
    except Exception as e:
        raise ValueError(f"{e}")
    links = set()
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    items = soup.find_all("div", class_="result-list-options")
    for item in items:
        a_tag = item.findChild("ul").findChild("li").findChild("a", class_="icons")
        links.add("https:" + a_tag.get("href"))
    for url in links:
        p_url = parse_qs(urlparse(url).query, keep_blank_values=True)
        file_name = p_url["p_File_Name"][0]
        file_path = os.path.join(dest, file_name)
        download_list_files(url, file_path)
#Try and Catch impelementation
def main():
    try:
        url = "https://www.se.com/ww/en/download/doc-group-type/3541958-Software%20&%20Firmware/?docType=1555893-Firmware&language=en_GB-English&sortByField=Popularity"
        folder = DATA['file_paths']['download_files_path']
        dest = os.path.join(os.getcwd(), folder)
        try:
            if not os.path.isdir(dest):
                os.mkdir(dest)
        except Exception as e:
            raise ValueError(f"{e}")
        total_fw = se_get_total_firmware_count(url)
        api_url = "https://www.se.com/ww/en/download/doc-group-type/3541958-Software%20&%20Firmware/resultViewCahnge/resultListAjax"
        raw_fw_list = get_firmware_data_using_api(api_url, total_fw, 50) #50 is max fw_per_page
        metadata = transform_metadata_format_ours(raw_fw_list, local_storage_dir=os.path.abspath(folder))
        write_metadata_to_db(metadata)
        download_list_files(metadata, 10) # download max 10 files
    except Exception as general_exception:
        logger.error(f"{general_exception}")
        traceback.print_exc(file=sys.stdout)

if __name__ == "__main__":
    main()
