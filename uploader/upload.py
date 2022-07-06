import requests


class FirmwareUploader(object):
    def __init__(self):
        self.auth_url = "http://embark.local"
        self.cookies = dict()

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
        print(self.cookies)

if __name__=="__main__":
    fwu = FirmwareUploader()
    fwu.authenticate("apiuser", "GpY8V3d25G3gaZg")
