import sys
sys.path.append(os.path.abspath(os.path.join('.', '')))

from utils.database import Database
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
import time,os
from utils.chromium_downloader import ChromiumDownloader


class WebCode(unittest.TestCase):

    def setUp(self):
        opt = Options()
        ChromiumDownloader().executor()
        opt.headless = True
        self.driver = webdriver.Chrome(options=opt)
        self.path = os.getcwd()
        self.db_name = 'firmwaredatabase.db'
        opt.add_experimental_option("prefs", {
            "download.default_directory": r"{}\downloads\honeywell".format(self.path),
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        })
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

    def test_homepage(self):
        driver = self.driver
        driver.get("https://sps.honeywell.com/us/en/support/software-downloads")
        driver.implicitly_wait(10)  # seconds
        driver.maximize_window()
        self.assertEqual("Software and Downloads | Honeywell", driver.title, msg="Homepage testcase passed")

    def down_ele_click(self, loc_loc,  element, f_name):
        # A fn for duplication Check for not to download the files if files exist in local machine
        if not os.path.isfile(loc_loc.replace("\\", "/")):
            print(f"The file is not found in local repository, now {f_name} will be downloaded into local")
            time.sleep(10)
            element.click()
        else:
            print(f"The file is found in local repository, now {f_name} will not be downloaded into local")

    def test_Advanced_Sensing_Tech(self):
        # 1. the function responsible to drive Advanced Sensing Technologies
        driver = self.driver
        driver.get("https://sps.honeywell.com/us/en/support/software-downloads")
        driver.implicitly_wait(10)  # seconds
        driver.maximize_window()
        driver.refresh()
        time.sleep(5)
        click_here_options = driver.find_element(By.XPATH, "(//a[contains(text(),'CLICK HERE')])[1]")
        click_here_options.click()
        rows = driver.find_elements(By.XPATH, '//*[@class="table__row fe-search-item"]')
        for row in rows:
            web_file_name, last_updated, file_size, file_type, download_text = "", "", "", "", ""
            data = rows[rows.index(row)].text
            web_file_name, last_updated, file_size, file_type, download_text = data.split("\n")
            download_link = rows[rows.index(row)].find_element(By.XPATH, "//div[@class='table__cell table__cell--icons ml-md-auto']//*[contains(@data-analytics-asset-name, '{}')]".format(str(web_file_name))).get_attribute('href')
            download_element = row.find_element(By.XPATH,"//div[@class='table__cell table__cell--icons ml-md-auto']//*[contains(@data-analytics-asset-name, '{}')]".format(str(web_file_name)))
            file_name = row.find_element(By.XPATH,"//div[@class='table__cell table__cell--icons ml-md-auto']//*[contains(@data-analytics-asset-name, '{}')]".format(str(web_file_name))).get_attribute('download')
            # print(data, download_link, file_name)
            actions = ActionChains(driver)
            actions.move_to_element(download_element).perform()
            local_file_location = r"{}\downloads\honeywell\{}".format(self.path, file_name)
            # Duplication Check for not to download the files if files exist in local machine
            self.down_ele_click(local_file_location, download_element, file_name)
            self.assertTrue(local_file_location, msg="Location exists")
            self.assertTrue(download_element, msg="download element found")
            # print(local_file_location)
            dbdict_carrier = dict()
            db = Database(dbname=self.db_name)
            for key in self.dbdict.keys():
                if key == "Manufacturer": dbdict_carrier[key] = "Honeywell"
                if key == "Fwfilename": dbdict_carrier[key] = web_file_name
                if key == "Releasedate": dbdict_carrier[key] = last_updated
                if key == "Fwdownlink": dbdict_carrier[key] = download_link
                if key == "Fwfilelinktolocal": dbdict_carrier[key] = str(local_file_location.replace("\\", "/"))
                if key not in dbdict_carrier.keys(): dbdict_carrier[key] = ''
                if self.db_name not in os.listdir('.'):
                    db.create_table()
            db.insert_data(dbdict_carrier)
            self.assertTrue(dbdict_carrier, msg="data inserted")

        driver.back()

    def test_Gas(self):
        # 3. The function responsible to run the Safety
        driver = self.driver
        driver.get("https://sps.honeywell.com/us/en/support/software-downloads")
        driver.implicitly_wait(10)  # seconds
        driver.maximize_window()
        driver.refresh()
        time.sleep(10)
        click_here_options = driver.find_element(By.XPATH, "(//a[contains(text(),'CLICK HERE')])[3]")
        actions = ActionChains(driver)
        actions.move_to_element(click_here_options).perform()
        click_here_options.click()
        select = Select(driver.find_element(By.XPATH, '//select[@data-filter-label="Type"]'))
        select.select_by_visible_text("Firmware")
        time.sleep(5)
        # Next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Next']")))

        while driver.find_element(By.XPATH, "//div[@class='table__row']"):
            rows = driver.find_elements(By.XPATH, "//div[@class='table__row']")
            for row in rows:
                web_file_name, temp_add_web_data = "", ""
                data = rows[rows.index(row)].text
                web_file_name, temp_add_web_data = data.split("\n")
                download_link = rows[rows.index(row)].find_element(By.XPATH,"//div[@class='table__row'][{}]//div[@class='table__cell table__cell--icons ml-md-auto']//a[@class='table__link table__link--download js-download-trigger  document-download']".format(rows.index(row) + 1)).get_attribute('href')
                download_element = rows[rows.index(row)].find_element(By.XPATH, "//div[@class='table__row'][{}]//div[@class='table__cell table__cell--icons ml-md-auto']//a[@class='table__link table__link--download js-download-trigger  document-download']".format(rows.index(row) + 1))
                actions = ActionChains(driver)
                actions.move_to_element(download_element).perform()
                local_file_location = r"{}\downloads\honeywell\{}".format(self.path, download_link.split('/')[-1])
                self.down_ele_click(local_file_location, download_element, web_file_name)
                self.assertTrue(local_file_location, msg="Location exists")
                self.assertTrue(download_element, msg="download element found")
                dbdict_carrier = dict()
                db = Database(dbname=self.db_name)
                for key in self.dbdict.keys():
                    if key == "Fwfilename": dbdict_carrier[key] = web_file_name
                    if key == "Manufacturer": dbdict_carrier[key] = "Honeywell"
                    if key == "Fwdownlink": dbdict_carrier[key] = download_link
                    if key == "Fwfilelinktolocal": dbdict_carrier[key] = str(local_file_location.replace("\\", "/"))
                    if key not in dbdict_carrier.keys(): dbdict_carrier[key] = ''
                    if self.db_name not in os.listdir('.'):
                        db.create_table()
                db.insert_data(dbdict_carrier)
                self.assertTrue(dbdict_carrier, msg="data inserted")
            time.sleep(10)
            if driver.find_element(By.XPATH, "//*[text()='Next']").tag_name == "span": break
            driver.find_element(By.XPATH, "//a[text()='Next']").click()
        driver.back()

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":

    unittest.main()
