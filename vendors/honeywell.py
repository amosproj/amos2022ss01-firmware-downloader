import sys, os, time, inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from database import Database
from chromium_downloader import ChromiumDownloader


class Honeywell:
    """ Honeywell class is used to run each module like in the page:
     'https://sps.honeywell.com/us/en/support/software-downloads'
     1. Advanced Sensing Technologies:
     'https://sps.honeywell.com/us/en/support/advanced-sensing-technologies/software-downloads'
     2. Productivity: 'https://authn.honeywell.com/idp/startSSO.ping?PartnerSpId=S_AND_PS_FTP' and
     3. Safety: 'https://sps.honeywell.com/us/en/software/safety/gas-detection-software-and-firmware'
     Each function is created to run the download module separately and update the data into database
     """

    def __init__(self, email="firmwaredownloader1@gmail.com", password="Firmware@123"):
        self.email = email
        self.password = password
        self.path = os.getcwd()
        self.db_name = 'firmwaredatabase.db'
        opt = Options()
        opt.add_experimental_option("prefs", {
            "download.default_directory": r"{}\downloads\honeywell".format(self.path),
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
            'Fwadddata': ''
        }

    def homepage(self):
        # The homepage is used to navigate to the main page of downloads
        driver = self.driver
        driver.get("https://sps.honeywell.com/us/en/support/software-downloads")
        driver.implicitly_wait(10)  # seconds
        driver.maximize_window()

    def down_ele_click(self, loc_loc,  element):
        # A fn for duplication Check for not to download the files if files exist in local machine
        if not os.path.isfile(loc_loc.replace("\\", "/")):
            time.sleep(10)
            element.click()

    def Advanced_Sensing_Tech(self):
        # 1. the function responsible to drive Advanced Sensing Technologies
        driver = self.driver
        click_here_options = driver.find_element(By.XPATH, "(//a[contains(text(),'CLICK HERE')])[1]")
        click_here_options.click()
        rows = driver.find_elements(By.XPATH, '//*[@class="table__row fe-search-item"]')
        for row in rows:
            web_file_name, last_updated, file_size, file_type, download_text = "", "", "", "", ""
            data = rows[rows.index(row)].text
            web_file_name, last_updated, file_size, file_type, download_text = data.split("\n")
            download_link = rows[rows.index(row)].find_element(By.XPATH, "//div[@class='table__cell table__cell--icons ml-md-auto']//*[contains(@data-analytics-asset-name, '{}')]".format(str(web_file_name))).get_attribute('href')
            download_element = row.find_element(By.XPATH, "//div[@class='table__cell table__cell--icons ml-md-auto']//*[contains(@data-analytics-asset-name, '{}')]".format(str(web_file_name)))
            file_name = row.find_element(By.XPATH, "//div[@class='table__cell table__cell--icons ml-md-auto']//*[contains(@data-analytics-asset-name, '{}')]".format(str(web_file_name))).get_attribute('download')
            print(data, download_link, file_name)
            actions = ActionChains(driver)
            actions.move_to_element(download_element).perform()
            local_file_location = r"{}\downloads\honeywell\{}".format(self.path, file_name)
            # Duplication Check for not to download the files if files exist in local machine
            self.down_ele_click(local_file_location, download_element)
            print(local_file_location)
            dbdict_carrier = dict()
            db = Database(dbname=self.db_name)
            for key in self.dbdict.keys():
                if key == "Manufacturer": dbdict_carrier[key] = "Honeywell"
                if key == "Fwfilename": dbdict_carrier[key] = r'{}'.format(web_file_name)
                if key == "Releasedate": dbdict_carrier[key] = last_updated
                if key == "Fwdownlink": dbdict_carrier[key] = download_link
                if key == "Fwfilelinktolocal": dbdict_carrier[key] = str(local_file_location.replace("\\", "/"))
                if key not in dbdict_carrier.keys(): dbdict_carrier[key] = ''
                if self.db_name not in os.listdir('.'):
                    db.create_table()
            db.insert_data(dbdict_carrier)

        driver.back()

    def Gas(self):
        # 3. The function responsible to run the Safety
        driver = self.driver
        driver.refresh()
        time.sleep(10)
        click_here_options = driver.find_element(By.XPATH, "(//a[contains(text(),'CLICK HERE')])[3]")
        actions = ActionChains(driver)
        actions.move_to_element(click_here_options).perform()
        click_here_options.click()
        select = Select(driver.find_element(By.XPATH, '//select[@data-filter-label="Type"]'))
        select.select_by_visible_text("Firmware")
        time.sleep(5)
        while driver.find_element(By.XPATH, "//div[@class='table__row']"):
            rows = driver.find_elements(By.XPATH, "//div[@class='table__row']")
            for row in rows:
                web_file_name, temp_add_web_data = "", ""
                data = rows[rows.index(row)].text
                web_file_name, temp_add_web_data = data.split("\n")
                download_link = rows[rows.index(row)].find_element(By.XPATH, "//div[@class='table__row'][{}]//div[@class='table__cell table__cell--icons ml-md-auto']//a[@class='table__link table__link--download js-download-trigger  document-download']".format(rows.index(row)+1)).get_attribute('href')
                download_element = rows[rows.index(row)].find_element(By.XPATH, "//div[@class='table__row'][{}]//div[@class='table__cell table__cell--icons ml-md-auto']//a[@class='table__link table__link--download js-download-trigger  document-download']".format(rows.index(row)+1))
                actions = ActionChains(driver)
                actions.move_to_element(download_element).perform()
                local_file_location = r"{}\downloads\honeywell\{}".format(self.path, download_link.split('/')[-1])
                self.down_ele_click(local_file_location, download_element)
                dbdict_carrier = dict()
                db = Database(dbname=self.db_name)
                for key in self.dbdict.keys():
                    if key == "Fwfilename": dbdict_carrier[key] = r'{}'.format(web_file_name)
                    if key == "Manufacturer": dbdict_carrier[key] = "Honeywell"
                    if key == "Fwdownlink": dbdict_carrier[key] = download_link
                    if key == "Fwfilelinktolocal": dbdict_carrier[key] = str(local_file_location.replace("\\", "/"))
                    if key not in dbdict_carrier.keys(): dbdict_carrier[key] = ''
                    if self.db_name not in os.listdir('.'):
                        db.create_table()
                db.insert_data(dbdict_carrier)
            time.sleep(10)
            if driver.find_element(By.XPATH, "//*[text()='Next']").tag_name == "span": break
            driver.find_element(By.XPATH, "//a[text()='Next']").click()
        driver.back()

    def Close_browser(self):
        # At the end of the program, the function will close the Chrome browser
        driver = self.driver
        time.sleep(10)
        driver.quit()


if __name__ == '__main__':
    ChromiumDownloader().executor()
    hw = Honeywell()
    hw.homepage()
    hw.Advanced_Sensing_Tech()
    hw.Gas()
    hw.Close_browser()
