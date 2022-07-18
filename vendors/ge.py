import requests
from bs4 import BeautifulSoup
import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
sys.path.append(os.path.abspath(os.path.join('.', '')))
from utils.database import Database
from utils.check_duplicates import check_duplicates
from utils.Logs import get_logger
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
from utils.modules_check import config_check
logger = get_logger("vendors.ge")
links=[]

USERNAME = ''
PASSWORD = ''
URL = ''
CONFIG_PATH = os.path.join("config", "config.json")
DATA={}
with open(CONFIG_PATH, "rb") as fp:
    DATA = json.load(fp)
    # user check
    if config_check('ge', 'user'):
        USERNAME = DATA['ge']['user']
    else:
        if config_check('default', 'user'):
            USERNAME = DATA['default']['user']
        else:
            print('error')
            logger.error('<module : Ge> -> user not present')
            # using hardcode user for GE
    # password check
    if config_check('ge', 'password'):
        PASSWORD = DATA['ge']['password']
    else:
        if config_check('default', 'password'):
            PASSWORD = DATA['default']['password']
        else:
            print('error')
            logger.error('<module : Ge> -> password not present')
            # using hardcode user for GE

    # Url check
    if config_check('ge', 'url'):
        URL = DATA['ge']['url']
    else:
        if config_check('default', 'url'):
            URL = DATA['default']['url']
        else:
            print('error')
            logger.error('<module : Ge> -> url not present')
            # using hardcode user for GE
            logger.info('<module : Ge> -> using hardcode url')
            URL = 'https://www.gegridsolutions.com'

#inserting meta data into database
def insert_into_db(fwdata):
    db_ = Database()
    db_.insert_data(dbdictcarrier=fwdata)
    logger.info("data inserted")

#download firmware image
def download_file(data):
    local_uri = os.path.abspath(DATA['file_paths']['download_files_path'] + "/" + data['data0'])
    req_data = {
        'Fwfileid': 'FILE',
        'Fwfilename': data['data0'],
		'Manufacturer': 'GE',
		'Modelname': os.path.splitext(data['data0'])[0],
		'Version': '',
		'Type': '',
		'Releasedate': data['data1'],
		'Checksum': 'None',
		'Embatested': '',
		'Embalinktoreport': '',
		'Embarklinktoreport': '',
		'Fwdownlink': data['url'],
		'Fwfilelinktolocal': local_uri,
		'Fwadddata': ''
	}

    if check_duplicates(req_data, data['db_name']) is False or data['is_file_download'] is True:
        if data['link'] != "javascript:;":
            logger.info("Downloading %s and saving as %s", data['url'], data['file_path_to_save'])
            resp = requests.get(data['url'], allow_redirects=True)
            if resp.status_code != 200:
                raise ValueError("Invalid Url or file not found")
            with open(data['file_path_to_save'], "wb") as fp_:
                fp_.write(resp.content)
            if data['is_file_download'] is False:
                insert_into_db(req_data)
        else:
            options = webdriver.ChromeOptions()
            prefs = {"download.default_directory" : data['file_path_to_save']}
            options.add_argument("headless")
            options.add_experimental_option("prefs",prefs)
            driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
            # Go to your page url
            try:
                url_ = URL
                driver.get(url_)
                driver.find_element(By.ID, "ctl00_BodyContent_Login1_UserName").send_keys(USERNAME)
                driver.find_element(By.ID, "ctl00_BodyContent_Login1_Password").send_keys(PASSWORD)
                driver.find_element(By.ID, "ctl00_BodyContent_Login1_LoginButton").click()
                # Get button you are going to click by its id ( also you could us find_element_by_css_selector to get element by css selector)
                driver.get(data['main_url'])
                driver.execute_script(data['click'])
                time.sleep(10)
                driver.close()
                if data['is_file_download'] is False:
                    insert_into_db(req_data)
            except Exception as er_:
                logger.error("Error in downloading: %s", er_)

    else:
        logger.info("Data already exist!")

#parse html and start clean according to our need
def scraper_parse(url, base_url):
    dest = os.path.join(os.getcwd(), DATA['file_paths']['download_files_path'])
    try:
        if not os.path.isdir(dest):
            os.mkdir(dest)
    except Exception as er_:
        raise ValueError("%s" % er_) from er_
    cont = requests.get(url)
    soup = BeautifulSoup(cont.text, 'html.parser')
    items = soup.find_all("tr", valign="top")
    data = []
    click = ""
    for item in items:
        sub_data = []
        items_temp = item.find_all("td")
        if len(items_temp):
            if items_temp[0].get_text().find(".zip") != -1 or items_temp[0].get_text().find(".mpk") != -1 or items_temp[0].get_text().find(".S28") != -1:
                for item_temp in items_temp:
                    if items_temp.index(item_temp) == 0:
                        link = item_temp.findChild("a").get("href")
                        if link == "javascript:;":
                            click = item_temp.findChild("a").get("onclick")
                        file_path = os.path.join(dest, item_temp.get_text())
                        arg_data = {
                            'url': base_url + link,
                            'file_path_to_save': file_path,
                            'data0': items_temp[0].get_text(),
                            'data1': items_temp[1].get_text(),
                            'filename': item_temp.get_text(),
                            'link': link,
                            'main_url': url,
                            'click': click,
                            'db_name': 'firmwaredatabase.db',
                            'is_file_download': False,
                            'folder': DATA['file_paths']['download_files_path']
                        }
                        download_file(arg_data)
                    sub_data.append(item_temp.get_text())
                data.append(sub_data)

def directories_link(url, base_url):
    cont = requests.get(url)
    soup = BeautifulSoup(cont.text, 'html.parser')
    items = soup.find_all("p", style="MARGIN-TOP: 0px; PADDING-LEFT: 15px")
    for item in items:
        items_temp = item.find_all("a")
        for item_temp in items_temp:
            link = item_temp.get("href")
            if str(link).find("software.asp?directory=") != -1:
                links.append(base_url + "/communications/mds/" + link)
            elif str(link).find("/Communications/MDS/PulseNET_Download.aspx"):
                links.append(base_url + "/Communications/MDS/PulseNET_Download.aspx")
            elif str(link).find("/app/resources.aspx?prod=vistanet&type=7"):
                links.append(base_url + "/app/resources.aspx?prod=vistanet&type=7")

def main():
    base_url = DATA['ge']['url']
    directories_link(base_url + '/communications/mds/software.asp', base_url)
    paths = links
    for path in paths:
        url = path
        scraper_parse(url, base_url)

if __name__ == "__main__":
    main()
