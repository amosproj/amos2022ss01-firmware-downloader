import base64
import inspect
import json
import os
import re
import requests
import sys
import time
import urllib3
import urllib.parse
import wget
import zipfile
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from utils.chromium_downloader import ChromiumDownloader
from utils.database import Database
from utils.metadata_extractor import get_hash_value
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
# os.system('cmd /k "taskkill /F /IM chromedriver.exe /T"')
# os.system('cmd /k "taskkill /F /IM chrome.exe /T"')


class Honeywell:
    """ Honeywell class is used to run each module like in the page:
     'https://sps.honeywell.com/us/en/support/software-downloads'
     1. Advanced Sensing Technologies:
     'https://sps.honeywell.com/us/en/support/advanced-sensing-technologies/software-downloads'
     2. Productivity: 'https://authn.honeywell.com/idp/startSSO.ping?PartnerSpId=S_AND_PS_FTP' and
     3. Safety: 'https://sps.honeywell.com/us/en/software/safety/gas-detection-software-and-firmware'
     Each function is created to run the download module separately and update the data into database
     """

    def __init__(self):
        with open(os.path.join(parent_dir, 'config', 'config.json'), 'rb') as json_file:
            json_data = json.loads(json_file.read())
            honeywell_data = json_data['honeywell']
            self.email = honeywell_data['user']
            self.password = honeywell_data['password']
            self.url = honeywell_data['url']
            self.down_file_path = json_data['file_paths']['download_files_path']
        self.path = os.getcwd()
        opt = Options()
        opt.add_experimental_option("prefs", {
            "download.default_directory": r"{}\{}\Honeywell".format(self.path, self.down_file_path),
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

    @staticmethod
    def down_ele_click(loc_loc,  element):
        # A fn for duplication Check for not to download the files if files exist in local machine
        if not os.path.isfile(loc_loc.replace("\\", "/")):
            time.sleep(10)
            element.click()

    @staticmethod
    def regex_sep(in_file_name):
        version_regex = "ve?r?s?i?o?n?\.?.?[a-zA-Z0-9]+\.[a-zA-Z0-9]+\.?\d?\d?\d?\.?\d?\d?\d?"
        ind = re.search(version_regex, in_file_name, re.IGNORECASE)
        if ind:
            version = in_file_name[ind.start():ind.end()] if in_file_name[ind.start():ind.end()][-1] != '.' \
                else in_file_name[ind.start():ind.end()][:-1]
            in_file_name = str(in_file_name).replace(version, '')
            return version, in_file_name
        else:
            version = None
            return version, in_file_name

    def advanced_sensing_tech(self):
        # 1. the function responsible to drive Advanced Sensing Technologies
        driver = self.driver
        click_here_options = driver.find_element(By.XPATH, "(//a[contains(text(),'CLICK HERE')])[1]")
        click_here_options.click()
        rows = driver.find_elements(By.XPATH, '//*[@class="table__row fe-search-item"]')
        for row in rows:
            web_file_name, last_updated, file_size, file_type, download_text = "", "", "", "", ""
            data = rows[rows.index(row)].text
            web_file_name, last_updated, file_size, file_type, download_text = data.split("\n")
            version, model_name = self.regex_sep(web_file_name)
            download_link = rows[rows.index(row)].find_element(
                By.XPATH, "//div[@class='table__cell table__cell--icons ml-md-auto']//"
                          "*[contains(@data-analytics-asset-name, '{}')]"
                .format(str(web_file_name))).get_attribute('href')
            download_element = row.find_element(
                By.XPATH, "//div[@class='table__cell table__cell--icons ml-md-auto']//"
                          "*[contains(@data-analytics-asset-name, '{}')]".format(str(web_file_name)))
            file_name = row.find_element(
                By.XPATH, "//div[@class='table__cell table__cell--icons ml-md-auto']//"
                          "*[contains(@data-analytics-asset-name, '{}')]"
                .format(str(web_file_name))).get_attribute('download')
            print(data, download_link, file_name)
            actions = ActionChains(driver)
            actions.move_to_element(download_element).perform()
            local_file_location = r"{}\{}\Honeywell\{}".format(self.path, self.down_file_path, file_name)
            # Duplication Check for not to download the files if files exist in local machine
            self.down_ele_click(local_file_location, download_element)
            dbdict_carrier = {}
            db_used = Database()
            for key in self.dbdict:
                if key == "Manufacturer":
                    dbdict_carrier[key] = "Honeywell"
                elif key == "Modelname":
                    dbdict_carrier[key] = r'{}'.format(model_name)
                elif key == "Version":
                    dbdict_carrier[key] = r'{}'.format(version)
                elif key == "Fwfilename":
                    dbdict_carrier[key] = r'{}'.format(web_file_name)
                elif key == "Releasedate":
                    dbdict_carrier[key] = last_updated
                elif key == "Fwdownlink":
                    dbdict_carrier[key] = download_link
                elif key == "Fwfilelinktolocal":
                    dbdict_carrier[key] = str(local_file_location.replace("\\", "/"))
                elif key == "Checksum":
                    dbdict_carrier[key] = get_hash_value(str(local_file_location.replace("\\", "/")))
                elif key not in dbdict_carrier:
                    dbdict_carrier[key] = ''
            db_used.insert_data(dbdict_carrier)
        driver.back()

    @staticmethod
    def action_download(in_driver, in_click_here_options):
        actions = ActionChains(in_driver)
        actions.move_to_element(in_click_here_options).perform()
        in_click_here_options.click()

    @staticmethod
    def base64_decoding(input_url):
        # This fn is to decode the input url and form the correct url using utf-8
        converted_url = base64.b64decode(input_url).decode("utf-8", errors="ignore")
        print(converted_url)
        return converted_url

    def url_call(self, in_data_soft_id_url, in_brow_cookies):
        # This fn is responsible for creating a Post API session and return the base64 decode response from API
        session = requests.session()
        session.auth = (self.email, self.password)
        session.verify = False
        session.headers = {"Accept": "application/json",
                           'Content-Type': 'application/json',
                           'Cookie': in_brow_cookies}
        content = session.post(in_data_soft_id_url, data={}).json()
        print(content)
        return self.base64_decoding(content)

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

    def prod_crawler(self):
        # This fn is responsible to crawl for firmware files and write the respective data into db
        driver = self.driver
        crows = driver.find_elements(By.XPATH, ".//tbody//tr")
        print([ele.text for ele in crows])
        for crow in crows:
            crow_add_desc = driver.find_element(By.XPATH, ".//tbody//tr[{}]//td[1]".format(crows.index(crow)+1)).text
            cfile_name = driver.find_element(By.XPATH, ".//tbody//tr[{}]//strong[@class='title']".format(crows.index(crow)+1))\
                .text
            crow_add_desc = crow_add_desc.replace(cfile_name, '')
            data_soft_id = driver.find_element(
                By.XPATH, f".//tbody//tr[{crows.index(crow)}+1]"
                          f"//button[@class='btn btn-link']").get_attribute('data-software-id')
            en_data_soft_id = urllib.parse.quote(data_soft_id)
            # the urllib parse quote fn is used to decode the data-software-id rendered from webpage
            en_data_soft_id_url = f'https://hsmftp.honeywell.com/sitecore/api/software/Download?fileLink=' \
                                  f'{en_data_soft_id}'
            brow_cookies = self.clean_cookies(driver.get_cookies())
            crow_down_link = self.url_call(en_data_soft_id_url, brow_cookies)
            local_file_location = r"{}\{}\Honeywell\{}".format(self.path, self.down_file_path, cfile_name)
            if not os.path.isfile(local_file_location.replace("\\", "/")):
                response = requests.get(crow_down_link)
                with open(local_file_location, 'wb') as zip_file:
                    zip_file.write(response.content)
            print(cfile_name, crow_down_link, crow_add_desc, sep='\n')
            dbdict_carrier = {}
            db_used = Database()
            for key in self.dbdict:
                if key == "Fwfilename":
                    dbdict_carrier[key] = r'{}'.format(cfile_name)
                elif key == "Manufacturer":
                    dbdict_carrier[key] = "Honeywell"
                elif key == "Fwdownlink":
                    dbdict_carrier[key] = r'{}'.format(crow_down_link)
                elif key == "Fwfilelinktolocal":
                    dbdict_carrier[key] = str(local_file_location.replace("\\", "/"))
                elif key == "Fwadddata":
                    dbdict_carrier[key] = r'{}'.format(crow_add_desc)
                elif key == "Checksum":
                    dbdict_carrier[key] = get_hash_value(str(local_file_location.replace("\\", "/")))
                elif key not in dbdict_carrier:
                    dbdict_carrier[key] = ''
            db_used.insert_data(dbdict_carrier)

    def productivity(self):
        # 2. the function responsible to run the productivity and is only responsible for login & tree expansion
        driver = self.driver
        driver.refresh()
        time.sleep(10)
        click_here_options = driver.find_element(By.XPATH, "(//a[contains(text(),'CLICK HERE')])[2]")
        self.action_download(driver, click_here_options)
        windows = driver.window_handles
        driver.switch_to.window(windows[-1])
        driver.find_element(By.XPATH, ".//input[@id='identifierInput']").send_keys(self.email)
        driver.find_element(By.XPATH, ".//button[@id='postButton']").click()
        time.sleep(10)
        driver.find_element(By.XPATH, ".//input[@id='password']").send_keys(self.password)
        driver.find_element(By.XPATH, ".//button[@type='submit']").click()
        driver.refresh()
        time.sleep(10)
        hny_down_tool = driver.find_element(By.XPATH, ".//a[contains(text(),'here')]").get_attribute('href')
        print(hny_down_tool)
        honeywell_zip = wget.download(hny_down_tool, 'honeywell_downloader.zip')
        with zipfile.ZipFile(honeywell_zip, 'r') as zip_ref:
            zip_ref.extractall()
        os.remove(honeywell_zip)
        hny_down_tool_file = str([name for name in os.listdir(os.getcwd())
                                  if '.msi' in name]).replace('[', '').replace(']', '').replace("'", '')
        hny_down_tool_file_path = r"{}\{}".format(self.path, hny_down_tool_file)
        print(hny_down_tool_file_path)
        driver.find_element(By.XPATH, ".//li[@aria-level='1']//i[@class='jstree-icon jstree-ocl']").click()
        rows0 = driver.find_elements(By.XPATH,
                                     ".//li[@aria-level='1']//li[@aria-level='2']//i[@class='jstree-icon jstree-ocl']")
        for row0 in rows0:
            print(rows0.index(row0) + 1)
            driver.find_element(
                By.XPATH, ".//li[@aria-level='1']//li[@aria-level='2'][{}]//i[@class='jstree-icon jstree-ocl']"
                .format(rows0.index(row0)+1)).click()
            print(driver.find_element(
                By.XPATH, ".//li[@aria-level='1']//li[@aria-level='2'][{}]//"
                          "i[@class='jstree-icon jstree-themeicon']".format(rows0.index(row0)+1)).text)
            rows1 = driver.find_elements(By.XPATH, ".//li[@aria-level='1']//li[@aria-level='2'][{}]//"
                                                   "li[@aria-level='3']//i[@class='jstree-icon jstree-ocl']"
                                         .format(rows0.index(row0)+1))
            time.sleep(10)
            for row1 in rows1:
                print(rows0.index(row0) + 1, rows1.index(row1) + 1)
                time.sleep(10)
                if driver.find_element(By.XPATH, ".//li[@aria-level='1']//li[@aria-level='2'][{}]//"
                                                 "li[@aria-level='3'][{}]//i[@class='jstree-icon jstree-ocl']"
                                                 "".format(rows0.index(row0) + 1, rows1.index(row1) + 1)):
                    driver.find_element(By.XPATH, ".//li[@aria-level='1']//li[@aria-level='2'][{}]//"
                                                  "li[@aria-level='3'][{}]//i[@class='jstree-icon jstree-ocl']".
                                        format(rows0.index(row0) + 1, rows1.index(row1) + 1)).click()
                    rows2 = driver.find_elements(
                        By.XPATH, ".//li[@aria-level='1']//li[@aria-level='2'][{}]//"
                                  "li[@aria-level='3'][{}]//li[@aria-level='4']//"
                                  "i[@class='jstree-icon jstree-ocl']"
                        .format(rows0.index(row0) + 1, rows1.index(row1) + 1))
                    time.sleep(10)
                    for row2 in rows2:
                        print(rows0.index(row0) + 1, rows1.index(row1) + 1, rows2.index(row2) + 1)
                        time.sleep(10)
                        element0 = driver.find_element(By.XPATH,
                                                       ".//li[@aria-level='1']//li[@aria-level='2'][{}]"
                                                       "//li[@aria-level='3'][{}]//li[@aria-level='4'][{}]"
                                                       .format(rows0.index(row0) + 1, rows1.index(row1) + 1,
                                                               rows2.index(row2) + 1))
                        element01 = driver.find_elements(By.XPATH,
                                                         ".//li[@aria-level='1']//li[@aria-level='2'][{}]"
                                                         "//li[@aria-level='3'][{}]//li[@aria-level='4'][{}]"
                                                         .format(rows0.index(row0) + 1, rows1.index(row1) + 1,
                                                                 rows2.index(row2) + 1))
                        print([element.text for element in element01])
                        print(element0.get_attribute('id'))
                        print(element0.get_attribute('aria-expanded'))
                        print(element0.get_attribute('class'))
                        print(element0.get_attribute(".//ul[@class='jstree-children']"))
                        if element0.get_attribute('aria-expanded') == 'false':
                            time.sleep(10)
                            driver.find_element(By.XPATH,
                                                ".//li[@aria-level='1']//li[@aria-level='2'][{}]"
                                                "//li[@aria-level='3'][{}]//li[@aria-level='4'][{}]"
                                                "//i[@class='jstree-icon jstree-ocl']".
                                                format(rows0.index(row0) + 1, rows1.index(row1) + 1,
                                                       rows2.index(row2) + 1)).click()
                            if element0.get_attribute('aria-expanded') == 'true' \
                                    and (element0.get_attribute('class') == 'jstree-node jstree-open' or
                                         element0.get_attribute('class') == 'jstree-node jstree-last jstree-open'):
                                time.sleep(10)
                                rows3 = driver.find_elements(
                                    By.XPATH, ".//li[@aria-level='1']//li[@aria-level='2'][{}]//"
                                              "li[@aria-level='3'][{}]//li[@aria-level='4'][{}]//"
                                              "li[@aria-level='5']//i[@class='jstree-icon jstree-ocl']"
                                    .format(rows0.index(row0) + 1, rows1.index(row1) + 1,
                                            rows2.index(row2) + 1))
                                for row3 in rows3:
                                    print(rows0.index(row0) + 1, rows1.index(row1) + 1, rows2.index(row2) + 1,
                                          rows3.index(row3) + 1)
                                    element1 = driver.find_element(
                                        By.XPATH, ".//li[@aria-level='1']//li[@aria-level='2'][{}]//"
                                                  "li[@aria-level='3'][{}]//li[@aria-level='4'][{}]//"
                                                  "li[@aria-level='5'][{}]".
                                        format(rows0.index(row0) + 1, rows1.index(row1) + 1,
                                               rows2.index(row2) + 1, rows3.index(row3) + 1))
                                    if element1.get_attribute('aria-expanded') == 'false':
                                        time.sleep(10)
                                        driver.find_element(
                                            By.XPATH, ".//li[@aria-level='1']//li[@aria-level='2'][{}]//"
                                                      "li[@aria-level='3'][{}]//li[@aria-level='4'][{}]//"
                                                      "li[@aria-level='5'][{}]//i[@class='jstree-icon jstree-ocl']".
                                            format(rows0.index(row0) + 1, rows1.index(row1) + 1,
                                                   rows2.index(row2) + 1, rows3.index(row3) + 1)).click()
                                        if element1.get_attribute('aria-expanded') == 'true' \
                                                and (element1.get_attribute('class') == 'jstree-node jstree-open' or
                                                     element1.get_attribute('class') ==
                                                     'jstree-node jstree-last jstree-open'):
                                            time.sleep(10)
                                            rows4 = driver.find_elements(
                                                By.XPATH, ".//li[@aria-level='1']//li[@aria-level='2'][{}]//"
                                                          "li[@aria-level='3'][{}]//li[@aria-level='4'][{}]//"
                                                          "li[@aria-level='5'][{}]//li[@aria-level='6']".
                                                format(rows0.index(row0) + 1, rows1.index(row1) + 1,
                                                       rows2.index(row2) + 1, rows3.index(row3) + 1))
                                            for row4 in rows4:
                                                print(rows0.index(row0) + 1, rows1.index(row1) + 1,
                                                      rows2.index(row2) + 1, rows3.index(row3) + 1,
                                                      rows4.index(row4) + 1)
                                                element2 = driver.find_element(
                                                    By.XPATH, ".//li[@aria-level='1']//li[@aria-level='2'][{}]//"
                                                              "li[@aria-level='3'][{}]//li[@aria-level='4'][{}]//"
                                                              "li[@aria-level='5'][{}]//li[@aria-level='6'][{}]".
                                                    format(rows0.index(row0) + 1, rows1.index(row1) + 1,
                                                           rows2.index(row2) + 1, rows3.index(row3) + 1,
                                                           rows4.index(row4) + 1))
                                                if element2.get_attribute('class') == 'jstree-node  jstree-leaf ' \
                                                                                      'jstree-last' or \
                                                        element2.get_attribute('class') == 'jstree-node  jstree-leaf' \
                                                        or element2.get_attribute('class') == \
                                                        'jstree-node  jstree-closed' or \
                                                        element2.get_attribute('class') == 'jstree-node  ' \
                                                                                           'jstree-closed jstree-last':
                                                    time.sleep(10)
                                                    driver.find_element(
                                                        By.XPATH, ".//li[@aria-level='1']//li[@aria-level='2'][{}]//"
                                                                  "li[@aria-level='3'][{}]//li[@aria-level='4'][{}]//"
                                                                  "li[@aria-level='5'][{}]//li[@aria-level='6'][{}]"
                                                                  "//a[@class='jstree-anchor']".
                                                        format(rows0.index(row0) + 1, rows1.index(row1) + 1,
                                                               rows2.index(row2) + 1, rows3.index(row3) + 1,
                                                               rows4.index(row4) + 1)).click()
                                                    time.sleep(10)
                                                    self.prod_crawler()
                                    elif element1.get_attribute('class') == 'jstree-node  jstree-leaf jstree-last' or \
                                            element1.get_attribute('class') == 'jstree-node  jstree-leaf':
                                        time.sleep(10)
                                        driver.find_element(
                                            By.XPATH, ".//li[@aria-level='1']//li[@aria-level='2'][{}]//"
                                                      "li[@aria-level='3'][{}]//li[@aria-level='4'][{}]//"
                                                      "li[@aria-level='5'][{}]//a[@class='jstree-anchor']".
                                            format(rows0.index(row0) + 1, rows1.index(row1) + 1,
                                                   rows2.index(row2) + 1, rows3.index(row3) + 1)).click()
                                        time.sleep(10)
                                        self.prod_crawler()
                                    elif element1.get_attribute('class') == 'jstree-node jstree-closed':
                                        time.sleep(10)
                                        driver.find_element(
                                            By.XPATH, ".//li[@aria-level='1']//li[@aria-level='2'][{}]//"
                                                      "li[@aria-level='3'][{}]//li[@aria-level='4'][{}]//"
                                                      "li[@aria-level='5'][{}]//i[@class='jstree-node  jstree-closed']".
                                            format(rows0.index(row0) + 1, rows1.index(row1) + 1,
                                                   rows2.index(row2) + 1, rows3.index(row3) + 1)).click()
                                        time.sleep(10)
                                        self.prod_crawler()
                                        # if element1.get_attribute('class') == 'jstree-node jstree-open':

                        elif element0.get_attribute('class') == 'jstree-node  jstree-leaf' or \
                                element0.get_attribute('class') == 'jstree-node  jstree-leaf jstree-last':
                            time.sleep(10)
                            driver.find_element(By.XPATH,
                                                ".//li[@aria-level='1']//li[@aria-level='2'][{}]"
                                                "//li[@aria-level='3'][{}]//li[@aria-level='4'][{}]"
                                                "//a[@class='jstree-anchor']".
                                                format(rows0.index(row0) + 1, rows1.index(row1) + 1,
                                                       rows2.index(row2) + 1)).click()
                            time.sleep(10)
                            self.prod_crawler()
        driver.switch_to.window(windows[0])

    def gas(self):
        # 3. The function responsible to run the Safety
        driver = self.driver
        driver.refresh()
        time.sleep(10)
        click_here_options = driver.find_element(By.XPATH, "(//a[contains(text(),'CLICK HERE')])[3]")
        self.action_download(driver, click_here_options)
        select = Select(driver.find_element(By.XPATH, '//select[@data-filter-label="Type"]'))
        select.select_by_visible_text("Firmware")
        time.sleep(5)
        while driver.find_element(By.XPATH, "//div[@class='table__row']"):
            rows = driver.find_elements(By.XPATH, "//div[@class='table__row']")
            for row in rows:
                web_file_name, temp_add_web_data = "", ""
                data = rows[rows.index(row)].text
                web_file_name, temp_add_web_data = data.split("\n")
                version, model_name = self.regex_sep(web_file_name)
                download_link = rows[rows.index(row)].find_element(
                    By.XPATH, "//div[@class='table__row'][{}]//"
                              "div[@class='table__cell table__cell--icons ml-md-auto']//"
                              "a[@class='table__link table__link--download js-download-trigger  document-download']"
                    .format(rows.index(row)+1)).get_attribute('href')
                download_element = rows[rows.index(row)].find_element(
                    By.XPATH, "//div[@class='table__row'][{}]//"
                              "div[@class='table__cell table__cell--icons ml-md-auto']//"
                              "a[@class='table__link table__link--download js-download-trigger  document-download']"
                    .format(rows.index(row)+1))
                actions = ActionChains(driver)
                actions.move_to_element(download_element).perform()
                local_file_location = r"{}\{}\Honeywell\{}".format(self.path, self.down_file_path,
                                                                   download_link.split('/')[-1])
                self.down_ele_click(local_file_location, download_element)
                dbdict_carrier = {}
                db_used = Database()
                for key in self.dbdict:
                    if key == "Fwfilename":
                        dbdict_carrier[key] = r'{}'.format(web_file_name)
                    elif key == "Manufacturer":
                        dbdict_carrier[key] = "Honeywell"
                    elif key == "Modelname":
                        dbdict_carrier[key] = r'{}'.format(model_name)
                    elif key == "Version":
                        dbdict_carrier[key] = r'{}'.format(version)
                    elif key == "Fwdownlink":
                        dbdict_carrier[key] = download_link
                    elif key == "Fwfilelinktolocal":
                        dbdict_carrier[key] = str(local_file_location.replace("\\", "/"))
                    elif key == "Checksum":
                        dbdict_carrier[key] = get_hash_value(str(local_file_location.replace("\\", "/")))
                    elif key not in dbdict_carrier:
                        dbdict_carrier[key] = ''
                db_used.insert_data(dbdict_carrier)
            time.sleep(10)
            if driver.find_element(By.XPATH, "//*[text()='Next']").tag_name == "span":
                break
            driver.find_element(By.XPATH, "//a[text()='Next']").click()
        driver.back()

    def close_browser(self):
        # At the end of the program, the function will close the Chrome browser
        driver = self.driver
        time.sleep(10)
        driver.quit()


if __name__ == '__main__':
    ChromiumDownloader().executor()
    hw = Honeywell()
    hw.homepage()
    hw.advanced_sensing_tech()
    hw.gas()
    hw.productivity()
    hw.close_browser()
