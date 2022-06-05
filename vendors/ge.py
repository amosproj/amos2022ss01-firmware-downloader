import requests
from bs4 import BeautifulSoup
import os
from ..database import Database

def insert_into_db():
    Database.insert_data()
    print("insert")

def download_file(url, file_path_to_save):
    print(f"Donwloading {url} and saving as {file_path_to_save}")
    resp = requests.get(url, allow_redirects=True)
    if resp.status_code != 200:
        raise ValueError("Invalid Url or file not found")
    with open(file_path_to_save, "wb") as f:
        f.write(resp.content)

def scraper_parse(url, dest, base_url):
    cont = requests.get(url)
    soup = BeautifulSoup(cont.text, 'html.parser')
    items = soup.find_all("tr", valign="top")
    data = []
    links = []
    for item in items:
        sub_data = []
        items_temp = item.find_all("td")
        for item_temp in items_temp:
            if(items_temp.index(item_temp) == 0):
                link = item_temp.findChild("a").get("href")
                # links.append(link)
                # p_url = parse_qs(urlparse(url).query, keep_blank_values=True)
                # file_name = p_url["p_File_Name"][0]
                file_path = os.path.join(dest, item_temp.get_text())
                # download_file(base_url + link, file_path)
            sub_data.append(item_temp.get_text())
        data.append(sub_data)
            # else:
            #     print(item_temp.findChild("td"))
    
    print(links)

def directories_link(url, base_url, folder):
    dest = os.path.join(os.getcwd(), folder)
    try:
        if not os.path.isdir(dest):
            os.mkdir(dest)
    except Exception as e:
        raise ValueError(f"{e}")
    cont = requests.get(url)
    soup = BeautifulSoup(cont.text, 'html.parser')
    items = soup.find_all("p", style="MARGIN-TOP: 0px; PADDING-LEFT: 15px")
    links=[]
    for item in items:
        items_temp = item.find_all("a")
        for item_temp in items_temp:
            link = item_temp.get("href")
            if(str(link).find("software.asp?directory=") != -1):
                links.append(base_url + "/communications/mds/" + link)
    
    # for link in links:
    print(links[0])
    scraper_parse(links[0], dest, base_url)

if __name__ == "__main__":
    path = "/communications/mds/software.asp"
    base_url = "https://www.gegridsolutions.com"
    url = base_url + path
    folder = 'File_system'
    directories_link(url, base_url, folder)