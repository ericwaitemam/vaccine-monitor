import requests
import time
from datetime import datetime
from bs4 import BeautifulSoup

cached_locations = {}
delay = 5


URL = 'https://www.vgregion.se/ov/vaccinationstider/bokningsbara-tider/'

def log(string):
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": " + string)

while True:
    current_locations = {}
    
    page = ''
    while page == '':
        try:
            page = requests.get(URL)
            break
        except:
            time.sleep(5)
            continue

    soup = BeautifulSoup(page.content, 'html.parser')
    raw_locations = soup.find_all('div', class_='media-body')

    for location in raw_locations:
        name = location.find('h3').get_text()
        url = location.find('a')['href']
        current_locations[name] = url

    for location in list(cached_locations):
        if location not in current_locations:
            log("Location " + location + " is no longer available"+ "\n")
            cached_locations.pop(location)

    for location in current_locations:
        if location not in cached_locations:
            log("New location added: " + location)
            log("URL: " + current_locations[location] + "\n")
            cached_locations[location] = current_locations[location]

    time.sleep(delay)
