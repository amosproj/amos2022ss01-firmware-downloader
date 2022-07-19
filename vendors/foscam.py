import os
import sys
import inspect
import json
import time
import requests
import urllib3
import wget
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from utils.chromium_downloader import ChromiumDownloader
from utils.database import Database
from utils.metadata_extractor import get_hash_value
from utils.modules_check import vendor_field
from utils.Logs import get_logger
logger = get_logger("vendors.foscam")
sys.path.append(os.path.abspath(os.path.join('.', '')))

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)


class FoscamHomeSecurity:

    def __init__(self):
        with open(os.path.join(parent_dir, 'config', 'config.json'), 'rb') as json_file:
            json_data = json.loads(json_file.read())
            dummy_foscam_data = json_data['foscam']
            if vendor_field('foscam', 'user') is False:
                logger.error('<module : foscam > -> user not present')
            else:
                self.email = vendor_field('foscam', 'user')
            if vendor_field('foscam', 'password') is False:
                logger.error('<module : foscam > -> password not present')
            else:
                self.password = vendor_field('foscam', 'password')
            if vendor_field('foscam', 'url') is False:
                logger.error('<module : foscam > -> url not present')
                self.url = "https://www.foscam.com/downloads/index.html"
            else:
                self.url = vendor_field('foscam', 'url')
            self.down_file_path = json_data['file_paths']['download_files_path']
        self.path = os.getcwd()
        opt = Options()
        opt.add_experimental_option("prefs", {
            "download.default_directory": r"{}\{}\Foscam".format(self.path, self.down_file_path),
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        })
        self.driver = webdriver.Chrome(options=opt)
        self.dbdict = {
            'Fwfileid': '',
            'Fwfilename': '',
            'Manufacturer': '',
            'Modelname': '',
            'Version': '',
            'Type': '',
            'Releasedate': '',
            'Checksum': '',
            'Embatested': '',
            'Embalinktoreport': '',
            'Embarklinktoreport': '',
            'Fwdownlink': '',
            'Fwfilelinktolocal': '',
            'Fwadddata': '',
            'Uploadedonembark': '',
            'Embarkfileid': '',
            'Startedanalysisonembark': ''
        }

    def homepage(self):
        # The homepage is used to navigate to the main page of downloads
        driver = self.driver
        driver.get(self.url)
        driver.implicitly_wait(10)  # seconds
        driver.maximize_window()

    def firmware_collector(self):
        driver = self.driver
        return [ele.get_attribute('href') for ele in driver.find_elements(
            By.XPATH, ".//div[@class='one']//div[contains(@class,'down_product_list_img')]"
                      "//a[contains(@href,'downloads/firmware_details.html?id=')]")]

    @staticmethod
    def url_call_file_name(in_data_soft_id_url, in_brow_cookies):
        # This fn is responsible for creating a Post API session and return the base64 decode response from API
        session = requests.session()
        # session.auth = (self.email, self.password)
        session.verify = False
        session.headers = {"Accept": "application/json", 'Content-Type': 'application/json', 'Cookie': in_brow_cookies}
        content = session.get(in_data_soft_id_url)
        content_headers = content.headers
        if 'Content-Disposition' in content_headers.keys():
            content_headers = content_headers['Content-Disposition'].replace('attachment; filename=', '') \
                .replace('"', '')
        else:
            content_headers = None
        print(content_headers)
        return content_headers

    @staticmethod
    def clean_cookies(in_brow_cookies):
        # This fn is responsible to clean the cookies to use for API headers and consume the cookies from driver
        in_brow_cookies = [{item['name']: item['value']} for item in in_brow_cookies]
        temp_cookies = []
        for item in in_brow_cookies:
            temp_cookies.append(''.join([f"{key}={item[key]}" for key in item]))
        in_brow_cookies = '; '.join(temp_cookies)
        print(in_brow_cookies)
        return in_brow_cookies

    def firmware_downloader(self):
        driver = self.driver
        fw_coll_data = list(set(self.firmware_collector()))
        for iter_num in range(2, 8):
            driver.find_element(
                By.XPATH,
                ".//a[contains(@onclick,'gotopage({})')]//"
                "img[contains(@src, '/Public/Home/images/faq/02.png')]".format(iter_num)).click()
            fw_coll_data.extend(list(set(self.firmware_collector())))
        print(len(fw_coll_data), fw_coll_data)
        for href_url in fw_coll_data:
            driver.get(href_url)
            print(href_url)
            try:
                if driver.find_element(By.XPATH, ".//table").is_displayed():
                    rows = driver.find_elements(By.XPATH, ".//tbody//tr")
                    web_file_name = driver.find_element(By.XPATH, ".//div[@class='download_list_icon']//span").text
                    for row in range(2, len(rows) + 1):
                        version = driver.find_element(By.XPATH, ".//tbody//tr[{}]//td[1]".format(row)).text
                        build_date = driver.find_element(By.XPATH, ".//tbody//tr[{}]//td[2]".format(row)).text
                        size = driver.find_element(By.XPATH, ".//tbody//tr[{}]//td[3]".format(row)).text
                        release_notes = driver.find_element(By.XPATH, ".//tbody//tr[{}]//td[4]".format(row)).text
                        attention = driver.find_element(By.XPATH, ".//tbody//tr[{}]//td[5]".format(row)).text
                        down_link = driver.find_element(By.XPATH, ".//tbody//tr[{}]//td[6]//a".format(row)) \
                            .get_attribute('href')
                        add_desc = fr'Size: {size},  Release Notes: {release_notes}, Attention: {attention},' \
                                   fr'Crawled Website: {href_url}.'
                        down_id = down_link.split('=')[-1]
                        api_url = f'https://www.foscam.com/downloads/file.html?cate=firmware&id={down_id}'
                        brow_cookies = self.clean_cookies(driver.get_cookies())
                        file_name = self.url_call_file_name(api_url, brow_cookies)
                        local_file_location = fr"{self.path}\{self.down_file_path}\Foscam\{str(f'{file_name}')}"
                        if not os.path.isfile(local_file_location.replace("\\", "/")) and file_name is not None:
                            wget.download(down_link, local_file_location)
                        dbdict_carrier = {}
                        db_used = Database()
                        for key in self.dbdict:
                            if key == "Manufacturer":
                                dbdict_carrier[key] = "Foscam"
                            elif key == "Fwfilename":
                                dbdict_carrier[key] = web_file_name
                            elif key == "Modelname":
                                dbdict_carrier[key] = file_name
                            elif key == "Version":
                                dbdict_carrier[key] = version
                            elif key == "Releasedate":
                                dbdict_carrier[key] = build_date
                            elif key == "Fwadddata":
                                dbdict_carrier[key] = add_desc
                            elif key == "Fwdownlink":
                                dbdict_carrier[key] = down_link
                            elif key == "Fwfilelinktolocal":
                                dbdict_carrier[key] = local_file_location
                            elif key == "Checksum":
                                if local_file_location.split("\\")[-1] is not None and file_name is not None:
                                    dbdict_carrier[key] = get_hash_value(str(local_file_location.replace("\\", "/")))
                                else:
                                    dbdict_carrier[key] = ''
                            else:
                                dbdict_carrier[key] = ''
                        db_used.insert_data(dbdict_carrier)
            except NoSuchElementException:
                dbdict_carrier = {}
                db_used = Database()
                for key in self.dbdict:
                    if key == "Manufacturer":
                        dbdict_carrier[key] = "Foscam"
                    elif key == "Fwadddata":
                        dbdict_carrier[key] = fr"The Webpage doesn't contain any Firmware downloads,\
                        So this page is skipped, The Firmware crawled page is: {href_url}"
                    else:
                        dbdict_carrier[key] = ''
                db_used.insert_data(dbdict_carrier)

    def close_browser(self):
        # At the end of the program, the function will close the Chrome browser
        driver = self.driver
        time.sleep(10)
        driver.quit()


if __name__ == '__main__':
    ChromiumDownloader().executor()
    fos = FoscamHomeSecurity()
    fos.homepage()
    fos.firmware_downloader()
    fos.close_browser()
