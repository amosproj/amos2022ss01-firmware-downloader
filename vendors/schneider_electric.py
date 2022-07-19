import os
import math
import re
import uuid
import sys
import traceback
import json
import inspect
from urllib.parse import parse_qs, urlparse
import requests
from bs4 import BeautifulSoup
from utils.check_duplicates import check_duplicates, Database
from utils.Logs import get_logger
from utils.modules_check import vendor_field
from utils.metadata_extractor import get_hash_value
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
sys.path.append(os.path.abspath(os.path.join('.', '')))

#Logger
MOD_NAME = "schneider_electric"
logger = get_logger("vendors.schneider_electric")
CONFIG_PATH = os.path.join(parent_dir, "config", "config.json")
DATA={}
URL = ''
API_URL = ''
with open(CONFIG_PATH, "rb") as fp:
    DATA = json.load(fp)
    if vendor_field('schneider_electric', 'url') is False:
        print('error url')
        logger.error('<module : schneider_electric > -> url not present')
        URL = "https://www.se.com/ww/en/download/doc-group-type/3541958-Software%20&%20Firmware/?docType=1555893-Firmware&language=en_GB-English&sortByField=Popularityy"
    else:
        # print(' url')
        URL = vendor_field('schneider_electric', 'url')

    if vendor_field('schneider_electric', 'apiurl') is False:
        # print('error url')
        logger.error('<module : schneider_electric > -> apiurl not present')
        API_URL = "https://www.se.com/ww/en/download/doc-group-type/3541958-Software%20&%20Firmware/resultViewCahnge/resultListAjax"
    else:
        # print('api url')
        API_URL = vendor_field('schneider_electric', 'apiurl')

def download_single_file(url, file_path_to_save, fw_metadata):
    logger.info("Downloading %s and saving as %s", url, file_path_to_save)
    resp = requests.get(url, allow_redirects=True)
    if resp.status_code != 200:
        raise ValueError("Invalid Url or file not found")
    with open(file_path_to_save, "wb") as fp_:
        fp_.write(resp.content)
    if fw_metadata:
        write_metadata_to_db([fw_metadata])

def download_list_files(metadata, max_files=-1): #max_files -1 means download all files
    if max_files == -1:
        max_files = len(metadata)
    if max_files > len(metadata):
        max_files = len(metadata)
    for file_ in range(max_files):
        download_single_file(metadata[file_]["Fwdownlink"], metadata[file_]["Fwfilelinktolocal"], metadata[file_])

def write_metadata_to_db(metadata, db_path=None):
    logger.info("Going to write metadata in db")
    if db_path:
        db_ = Database(db_path)
    else:
        db_ = Database()
    for fw_ in metadata:
        fw_["Checksum"] = get_hash_value(fw_["Fwfilelinktolocal"])
        db_.insert_data(dbdictcarrier=fw_)

def se_get_total_firmware_count(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    items = soup.find_all("label", class_="dn-check dn-selected")
    for item in items:
        if item.get("for") == "docTypeFilters-1555893":
            inner_html =item.decode_contents()
            numbers = re.findall(r'\b\d+\b', inner_html)
            count = int(numbers[0])
            logger.info("Found total %d firmwares", count)
            return count
    return int(numbers[0])

def get_firmware_data_using_api(url, fw_count, fw_per_page):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    total_pages = math.ceil(fw_count/fw_per_page)
    fw_list = []
    for page in range(1, total_pages+1):
        req_body= {
            "data": f"docType=1555893-Firmware_COMMA_language=en_GB-English_COMMA_sortByField=Document_Date_New_COMMA_itemsPerPage={fw_per_page}_COMMA_pageNumber={page}_COMMA_COMMA_keyword=",
            "buisnessId": ""
        }
        response = requests.post(url, data=req_body, headers=headers)
        if response.status_code != 200:
            logger.info("Invalid API response with status_code = %d", response.status_code)
            raise ValueError("Invalid API response with status_code = %d" % response.status_code)
        if page != total_pages:
            logger.info("Received metadata for %d/%d", page*fw_per_page, fw_count)
        else:
            logger.info("Received metadata for all %d/%d firmwares", fw_count, fw_count)
        fw_list += response.json()["docList"]
    return fw_list

def transform_metadata_format_ours(raw_data, local_storage_dir="."):
    fw_mod_list = []
    for fw_ in raw_data:
        fw_mod = {
            'Fwfileid': 'FILE',
            'Fwfilename': str(fw_.get("title", "").replace("'", "").replace(" ", "_")),
            'Manufacturer': 'schneider_electric',
            'Modelname': str(fw_.get("title", "").replace("'", "").replace(" ", "_")),
            'Version': str(fw_.get("version", "").replace(" ", "_")),
            'Type': str(fw_.get("documentTypeEnglishLabel", "").replace(" ", "_")),
            'Releasedate': fw_.get("docDate", ""),
            'Checksum': '',
            'Embatested': '',
            'Embalinktoreport': '',
            'Embarklinktoreport': '',
            'Fwdownlink': "https:" + fw_.get("downloadUrl", ""),
            'Fwfilelinktolocal': os.path.join(local_storage_dir, parse_qs(urlparse(fw_.get("downloadUrl")).query, keep_blank_values=True).get("p_File_Name", list(str(uuid.uuid4())))[0].replace(" ", "_").replace("'", "") ),
            'Fwadddata': '',
            'Uploadedonembark': '',
            'Embarkfileid': '',
            'Startedanalysisonembark': ''
	    }
        db_name = 'firmwaredatabase.db'
        if check_duplicates(fw_mod, db_name) is False:
            fw_mod_list.append(fw_mod)
    return fw_mod_list

# This method is outdated as of now.
def se_firmaware_parser(url, folder):
    dest = os.path.join(os.getcwd(), folder)
    try:
        if not os.path.isdir(dest):
            os.mkdir(dest)
    except Exception as er_:
        raise ValueError('%s' % er_) from er_
    links = set()
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    items = soup.find_all("div", class_="result-list-options")
    for item in items:
        a_tag = item.findChild("ul").findChild("li").findChild("a", class_="icons")
        links.add("https:" + a_tag.get("href"))
    for url_ in links:
        p_url = parse_qs(urlparse(url_).query, keep_blank_values=True)
        file_name = p_url["p_File_Name"][0]
        file_path = os.path.join(dest, file_name)
        download_list_files(url_, file_path)
#Try and Catch impelementation
def main():
    try:
        url = URL
        folder = DATA['file_paths']['download_files_path']
        dest = os.path.join(os.getcwd(), folder)
        try:
            if not os.path.isdir(dest):
                os.mkdir(dest)
        except Exception as er_:
            raise ValueError('%s' % er_) from er_
        total_fw = se_get_total_firmware_count(url)
        api_url = API_URL
        raw_fw_list = get_firmware_data_using_api(api_url, total_fw, 50) #50 is max fw_per_page
        metadata = transform_metadata_format_ours(raw_fw_list, local_storage_dir=os.path.abspath(folder))
        download_list_files(metadata, 10) # download max 10 files
    except Exception as general_exception:
        logger.error("%s", general_exception)
        traceback.print_exc(file=sys.stdout)
        raise ValueError('%s' % general_exception) from general_exception

if __name__ == "__main__":
    main()
