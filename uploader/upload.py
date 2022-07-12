import requests

from bs4 import BeautifulSoup, NavigableString

class FirmwareUploader:
    def __init__(self):
        self.auth_url = "http://embark.local"
        self.upload_fw_url = "http://embark.local/uploader/save/"
        self.start_analysis_url = "http://embark.local/uploader/start/"
        self.cookies = {}

    def authenticate(self, username, password):
        resp = requests.get(self.auth_url)
        csrf_token = None
        for cookie in resp.cookies:
            self.cookies[cookie.name] = cookie.value
        data =  {
            "csrfmiddlewaretoken": self.cookies.get("csrftoken", ""),
            "username": username,
            "password": password
        }
        resp = requests.post(self.auth_url,  data=data, cookies=self.cookies, allow_redirects=False)
        for cookie in resp.cookies:
            self.cookies[cookie.name] = cookie.value #saving csrftoken and seesionid cookies
        if set(["csrftoken", "sessionid"]).issubset(self.cookies.keys()):
            print("authentication is successful")
        else:
            print("authentication failed")
        print(self.cookies)

    def start_fw_analysis(self, fw_):
        data = {
            "csrfmiddlewaretoken": self.cookies.get("csrftoken", None),
            "firmware": fw_["id"],
            "version": "",
            "vendor": "",
            "device": "",
            "notes": "",
            "firmware_Architecture": "",
            "grep_able_log": "on",
            "relative_paths": "on",
            "ANSI_color": "on",
            "web_reporter": "on",
            "emulation_test": "on",
            "dependency_check": "on",
            "multi_threaded": "on",
            "firmware_remove": "on"
        }
        resp = requests.post(self.start_analysis_url, data=data, cookies=self.cookies)
        if resp.status_code == 200:
            print("Started firmware analysis successfully")
        else:
            print("Failed to start firmware analysis")

    def upload_fw(self, fw_):
        with open(fw_, 'rb') as firmware_file:
            files = [('file', firmware_file)]
            headers = {
                "X-CSRFToken": self.cookies.get('csrftoken', "")
            }
            resp = requests.post(self.upload_fw_url, files=files, headers=headers, cookies=self.cookies, allow_redirects=False)
            if resp.content == b'successful upload':
                print("File is uploaded successfully")

    def get_id_of_uploaded_file(self, filename):
        req = requests.get(self.start_analysis_url, cookies=self.cookies)
        soup = BeautifulSoup(req.text, 'html.parser')
        items = soup.find_all("select", id="id_firmware")
        options = items[0].find_all("option")
        selected_option = None
        for item in options:
            scrapped_filename = item.decode_contents().split("-")[-1].strip()
            scrapped_id = item.get("value")
            if "selected" in item.attrs.keys():
                if scrapped_filename == filename:
                    print("Found id of uploaded file %s", scrapped_id)

                    return scrapped_id
           

if __name__=="__main__":
    fwu = FirmwareUploader()
    fwu.authenticate("apiuser", "GpY8V3d25G3gaZg")
    fw_metadata = {}
    fw_metadata["file_path"] = "MPS4010_sys.zip"
    fwu.upload_fw(fw_metadata["file_path"])
    fw_metadata["id"] = fwu.get_id_of_uploaded_file(fw_metadata["file_path"])
    fwu.start_fw_analysis(fw_metadata)

