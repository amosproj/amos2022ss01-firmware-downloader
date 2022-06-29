import sys, os, time, inspect, wget, zipfile, re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from utils.database import Database
from utils.chromium_downloader import ChromiumDownloader
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

    def __init__(self, email="firmwaredownloader1@gmail.com", password="Firmware@123"):
        # with open('config/config.json', 'r') as f:
        #     self.email = json.load(f)['honeywell']['user']
        #     self.password = json.load(f)['honeywell']['password']
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

    @staticmethod
    def regex_sep(in_file_name):
        version_regex = 've?r?s?i?o?n?\.?.?[a-zA-Z0-9]+\.[a-zA-Z0-9]+\.?\d?\d?\d?\.?\d?\d?\d?'
        model_name, version = '', ''
        ind = re.search(version_regex, in_file_name, re.IGNORECASE)
        if ind:
            version = in_file_name[ind.start():ind.end()] if in_file_name[ind.start():ind.end()][-1] != '.' \
                else in_file_name[ind.start():ind.end()][:-1]
            in_file_name = str(in_file_name).replace(version, '')
            return version, in_file_name
        else:
            print(None, '----------', in_file_name)

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
            local_file_location = r"{}\downloads\honeywell\{}".format(self.path, file_name)
            # Duplication Check for not to download the files if files exist in local machine
            self.down_ele_click(local_file_location, download_element)
            dbdict_carrier = dict()
            db = Database(dbname=self.db_name)
            for key in self.dbdict.keys():
                if key == "Manufacturer":
                    dbdict_carrier[key] = "Honeywell"
                if key == "Modelname":
                    dbdict_carrier[key] = r'{}'.format(model_name)
                if key == "Version":
                    dbdict_carrier[key] = r'{}'.format(version)
                if key == "Fwfilename":
                    dbdict_carrier[key] = r'{}'.format(web_file_name)
                if key == "Releasedate":
                    dbdict_carrier[key] = last_updated
                if key == "Fwdownlink":
                    dbdict_carrier[key] = download_link
                if key == "Fwfilelinktolocal":
                    dbdict_carrier[key] = str(local_file_location.replace("\\", "/"))
                if key not in dbdict_carrier.keys():
                    dbdict_carrier[key] = ''
                if self.db_name not in os.listdir('.'):
                    db.create_table()
            db.insert_data(dbdict_carrier)
        driver.back()

    @staticmethod
    def action_download(in_driver, in_click_here_options):
        actions = ActionChains(in_driver)
        actions.move_to_element(in_click_here_options).perform()
        in_click_here_options.click()

    def Productivity(self):
        # 2. the function responsible to run the productivity
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
        driver.find_element(By.XPATH, ".//li[@aria-level='1']//i[@class='jstree-icon jstree-ocl']").click()
        rows0 = driver.find_elements(
            By.XPATH, ".//li[@aria-level='1']//li[@aria-level='2']//i[@class='jstree-icon jstree-ocl']")
        for row0 in rows0:
            print(rows0.index(row0) + 1)
            driver.find_element(
                By.XPATH, ".//li[@aria-level='1']//li[@aria-level='2'][{}]//i[@class='jstree-icon jstree-ocl']"
                .format(rows0.index(row0)+1)).click()
            print(driver.find_element(
                By.XPATH, ".//li[@aria-level='1']//li[@aria-level='2'][{}]//"
                          "i[@class='jstree-icon jstree-themeicon']".format(rows0.index(row0)+1)).text)
            rows1 = driver.find_elements(
                By.XPATH, ".//li[@aria-level='1']//li[@aria-level='2'][{}]//"
                          "li[@aria-level='3']//i[@class='jstree-icon jstree-ocl']".format(rows0.index(row0)+1))
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
                    print(driver.find_element(
                        By.XPATH,".//li[@aria-level='1']//li[@aria-level='2'][{}]//"
                                 "li[@aria-level='3'][{}]//i[@class='jstree-icon jstree-themeicon']"
                        .format(rows0.index(row0) + 1, rows1.index(row1) + 1)).text)
                    rows2 = driver.find_elements(
                        By.XPATH, ".//li[@aria-level='1']//li[@aria-level='2'][{}]//"
                                  "li[@aria-level='3'][{}]//li[@aria-level='4']//"
                                  "i[@class='jstree-icon jstree-ocl']"
                        .format(rows0.index(row0) + 1, rows1.index(row1) + 1))
                    time.sleep(10)
                    for row2 in rows2:
                        print(rows0.index(row0) + 1, rows1.index(row1) + 1, rows2.index(row2) + 1)
                        print(driver.find_element(By.XPATH,
                                                ".//li[@aria-level='1']//li[@aria-level='2'][{}]"
                                                "//li[@aria-level='3'][{}]//li[@aria-level='4'][{}]"
                                                "//i[@class='jstree-icon jstree-themeicon']".
                                                format(rows0.index(row0) + 1, rows1.index(row1) + 1,
                                                       rows2.index(row2) + 1)).text)
                        time.sleep(10)
                        element0 = driver.find_element(By.XPATH,
                                            ".//li[@aria-level='1']//li[@aria-level='2'][{}]"
                                            "//li[@aria-level='3'][{}]//li[@aria-level='4'][{}]".
                                            format(rows0.index(row0) + 1, rows1.index(row1) + 1,
                                                   rows2.index(row2) + 1))
                        element01 = driver.find_elements(By.XPATH,
                                                       ".//li[@aria-level='1']//li[@aria-level='2'][{}]"
                                                       "//li[@aria-level='3'][{}]//li[@aria-level='4'][{}]".
                                                       format(rows0.index(row0) + 1, rows1.index(row1) + 1,
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
                            if element0.get_attribute('aria-expanded') == 'true':
                                driver.find_element(By.XPATH,
                                                    ".//li[@aria-level='1']//li[@aria-level='2'][{}]//"
                                                    "li[@aria-level='3'][{}]//li[@aria-level='4'][{}]//"
                                                    "li[@aria-level='5']"
                                                    "".format(rows0.index(row0) + 1, rows1.index(row1) + 1,
                                                              rows2.index(row2) + 1)).click()
                        elif element0.get_attribute('class') == 'jstree-node  jstree-leaf':
                            driver.find_element(By.XPATH,
                                                ".//li[@aria-level='1']//li[@aria-level='2'][{}]"
                                                "//li[@aria-level='3'][{}]//li[@aria-level='4'][{}]"
                                                "//a[@class='jstree-anchor']".
                                                format(rows0.index(row0) + 1, rows1.index(row1) + 1,
                                                       rows2.index(row2) + 1)).click()
                        elif element0.get_attribute('class') == 'jstree-node  jstree-leaf jstree-last':
                            driver.find_element(By.XPATH,
                                                ".//li[@aria-level='1']//li[@aria-level='2'][{}]"
                                                "//li[@aria-level='3'][{}]//li[@aria-level='4'][{}]"
                                                "//a[@class='jstree-anchor']".
                                                format(rows0.index(row0) + 1, rows1.index(row1) + 1,
                                                       rows2.index(row2) + 1)).click()
        driver.switch_to.window(windows[0])

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
                local_file_location = r"{}\downloads\honeywell\{}".format(self.path, download_link.split('/')[-1])
                self.down_ele_click(local_file_location, download_element)
                dbdict_carrier = dict()
                db = Database(dbname=self.db_name)
                for key in self.dbdict.keys():
                    if key == "Fwfilename":
                        dbdict_carrier[key] = r'{}'.format(web_file_name)
                    if key == "Manufacturer":
                        dbdict_carrier[key] = "Honeywell"
                    if key == "Modelname":
                        dbdict_carrier[key] = r'{}'.format(model_name)
                    if key == "Version":
                        dbdict_carrier[key] = r'{}'.format(version)
                    if key == "Fwdownlink":
                        dbdict_carrier[key] = download_link
                    if key == "Fwfilelinktolocal":
                        dbdict_carrier[key] = str(local_file_location.replace("\\", "/"))
                    if key not in dbdict_carrier.keys():
                        dbdict_carrier[key] = ''
                    if self.db_name not in os.listdir('.'):
                        db.create_table()
                db.insert_data(dbdict_carrier)
            time.sleep(10)
            if driver.find_element(By.XPATH, "//*[text()='Next']").tag_name == "span":
                break
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
    hw.Productivity()
    hw.Gas()
    hw.Close_browser()
