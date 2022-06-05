import requests
from bs4 import BeautifulSoup
import os
import sys
sys.path.append(os.path.abspath(os.path.join('..', '')))  
from database import Database

def insert_into_db(data, url, local_uri):
    db_name = '../firmwaredatabase.db'
    db = Database(dbname=db_name)
    print(data)
    db.insert_data(dbdictcarrier={
		'Fwfileid': 'FILE',
		'Manufacturer': 'GE',
		'Modelname': data[0].get_text(),
		'Version': '',
		'Type': '',
		'Releasedate': data[1].get_text(),
		'Checksum': 'None',
		'Embatested': '',
		'Embalinktoreport': '',
		'Embarklinktoreport': '',
		'Fwdownlink': url,
		'Fwfilelinktolocal': local_uri,
		'Fwadddata': ''
	})
    print("inserted")

def download_file(url, file_path_to_save, data, folder, filename):
    # print(f"Downloading {url} and saving as {file_path_to_save}")
    # resp = requests.get(url, allow_redirects=True)
    # if resp.status_code != 200:
    #     raise ValueError("Invalid Url or file not found")
    # with open(file_path_to_save, "wb") as f:
    #     f.write(resp.content)
    local_uri = "./" + folder + "/" + filename
    print(local_uri)
    insert_into_db(data, url, local_uri)

def scraper_parse(url, folder, base_url):
    dest = os.path.join(os.getcwd(), folder)
    try:
        if not os.path.isdir(dest):
            os.mkdir(dest)
    except Exception as e:
        raise ValueError(f"{e}")
    cont = requests.get(url)
    soup = BeautifulSoup(cont.text, 'html.parser')
    items = soup.find_all("tr", valign="top")
    data = []
    for item in items:
        sub_data = []
        items_temp = item.find_all("td")
        if(len(items_temp)):
            if(items_temp[0].get_text().find(".zip") != -1 or items_temp[0].get_text().find(".mpk") != -1 or items_temp[0].get_text().find(".S28") != -1):
                for item_temp in items_temp:
                    if(items_temp.index(item_temp) == 0):
                        link = item_temp.findChild("a").get("href")
                        # links.append(link)
                        # p_url = parse_qs(urlparse(url).query, keep_blank_values=True)
                        # file_name = p_url["p_File_Name"][0]
                        file_path = os.path.join(dest, item_temp.get_text())
                        download_file(base_url + link, file_path, items_temp, folder, item_temp.get_text())
                    sub_data.append(item_temp.get_text())
                data.append(sub_data)

def directories_link(url, base_url, folder):
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
            elif(str(link).find("/Communications/MDS/PulseNET_Download.aspx")):
                links.append(base_url + "/Communications/MDS/PulseNET_Download.aspx")
            elif(str(link).find("/app/resources.aspx?prod=vistanet&type=7")):
                links.append(base_url + "/app/resources.aspx?prod=vistanet&type=7")
    
    for link in links:
        # print(links)
        scraper_parse(link, folder, base_url)

if __name__ == "__main__":
    path = "/communications/mds/software.asp"
    base_url = "https://www.gegridsolutions.com"
    url = base_url + path
    folder = 'File_system'
    directories_link(url, base_url, folder)