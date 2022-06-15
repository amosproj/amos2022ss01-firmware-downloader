import requests, wget, zipfile, os


class ChromiumDownloader:
    # The ChromiumDownloader is responsible to check and download if no Chromium Downloader is present at local repo

    def __init__(self):
        self.url = 'https://chromedriver.storage.googleapis.com'
        self.latest_release_url = 'https://chromedriver.storage.googleapis.com/LATEST_RELEASE'

    def load_and_extract(self):
        """ The fn is used to trigger the api to get latest version and then it allows to trigger download, unzip and
         delete the zip file"""
        response = requests.get(self.latest_release_url, allow_redirects=True).text
        download_url = "https://chromedriver.storage.googleapis.com/{}/chromedriver_win32.zip".format(response)
        print(response, download_url)
        chromium_zip = wget.download(download_url, 'chromedriver.zip')
        with zipfile.ZipFile(chromium_zip, 'r') as zip_ref:
            zip_ref.extractall()
        os.remove(chromium_zip)

    def executor(self):
        # Checksum for chromedriver
        if "chromedriver.exe" not in os.listdir(os.getcwd()):
            print("chromedriver.exe is not present in local path, so installing chromedriver")
            self.load_and_extract()
