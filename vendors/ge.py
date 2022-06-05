from email.mime import base
import requests
from bs4 import BeautifulSoup

directories = ["Orbit_MCR", "Master_Station", "TD-Series"]

def directories_link(url, base_url):
    cont = requests.get(url)
    soup = BeautifulSoup(cont.text, 'html.parser')
    items = soup.find_all("p", style="MARGIN-TOP: 0px; PADDING-LEFT: 15px")
    links=set()
    for item in items:
        items_temp = item.find_all("a")
        for item_temp in items_temp:
            link = item_temp.get("href")
            if(str(link).find("software.asp?directory=") != -1):
                links.add(base_url + link)

if __name__ == "__main__":
    path = "software.asp"
    base_url = "https://www.gegridsolutions.com/communications/mds/"
    url = base_url + path

    directories_link(url, base_url)