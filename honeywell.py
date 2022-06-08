from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time,os
from database import Database


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
        self.path=os.getcwd()
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

    def Advanced_Sensing_Tech(self):
        # the function responsible to drive Advanced Sensing Technologies
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
            print(data,download_link,file_name)
            actions = ActionChains(driver)
            actions.move_to_element(download_element).perform()
            local_file_location = r"{}\downloads\honeywell\{}".format(self.path, file_name)
            if not os.path.isfile(local_file_location.replace("\\", "/")):
                time.sleep(10)
                download_element.click()
            print(local_file_location)
            dbdict_carrier = dict()
            db = Database(dbname=self.db_name)
            for key in self.dbdict.keys():
                if key == "Manufacturer": dbdict_carrier[key] = "Honeywell"
                if key == "Releasedate": dbdict_carrier[key] = last_updated
                if key == "Fwdownlink": dbdict_carrier[key] = download_link
                if key == "Fwfilelinktolocal": dbdict_carrier[key] = str(local_file_location.replace("\\", "/"))
                if key not in dbdict_carrier.keys(): dbdict_carrier[key] = ''
                if self.db_name not in os.listdir('.'):
                    db.create_table()
            db.insert_data(dbdict_carrier)

        driver.back()

    def Gas(self):
        # The function responsible to run the Safety
        driver = self.driver
        click_here_options = driver.find_element(By.XPATH, "(//a[contains(text(),'CLICK HERE')])[3]")
        actions = ActionChains(driver)
        actions.move_to_element(click_here_options).perform()
        click_here_options.click()
        select = Select(driver.find_element(By.XPATH, '//select[@data-filter-label="Type"]'))
        select.select_by_visible_text("Firmware")
        time.sleep(5)
        # Next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Next']")))

        while driver.find_element(By.XPATH, "//*[text()='Next']").tag_name == "a":
            download_buttons = driver.find_elements(By.XPATH, "//span[text()='Download File']/ancestor::a")
            for download_button in download_buttons:
                actions = ActionChains(driver)
                actions.move_to_element(download_button).perform()
                download_button.click()
            driver.find_element(By.XPATH, "//a[text()='Next']").click()
            time.sleep(5)
        driver.back()

    def Close_browser(self):
        # At the end of the program, the function will close the Chrome browser
        driver = self.driver
        time.sleep(5)
        driver.quit()

# if __name__ == '__main__':
#     hw = Honeywell()
#     hw.homepage()
#     hw.Advanced_Sensing_Tech()
#     hw.Gas()
#     hw.Close_browser()
