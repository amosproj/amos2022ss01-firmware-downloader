import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import parse_qs, urlparse


def download_file(url, file_path_to_save):
    print(f"Donwloading {url} and saving as {file_path_to_save}")
    resp = requests.get(url, allow_redirects=True)
    if resp.status_code != 200:
        raise ValueError("Invalid Url or file not found")
    with open(file_path_to_save, "wb") as f:
        f.write(resp.content)

def se_firmaware_parser(url, folder):
    dest = os.path.join(os.getcwd(), folder)
    try:
        if not os.path.isdir(dest):
            os.mkdir(dest)
    except Exception as e:
        raise ValueError(f"{e}")
    links = set()
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    items = soup.find_all("div", class_="result-list-options")
    for item in items:
        a_tag = item.findChild("ul").findChild("li").findChild("a", class_="icons")
        links.add("https:" + a_tag.get("href"))
    for url in links:
        p_url = parse_qs(urlparse(url).query, keep_blank_values=True)
        file_name = p_url["p_File_Name"][0]
        file_path = os.path.join(dest, file_name)
        download_file(url, file_path)

if __name__ == "__main__":
    url = "https://www.se.com/ww/en/download/doc-group-type/3541958-Software%20&%20Firmware/?docType=1555893-Firmware&language=en_GB-English&sortByField=Popularity"
    folder = 'File_system'
    se_firmaware_parser(url, folder)