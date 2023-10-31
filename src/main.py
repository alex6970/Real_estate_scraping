#! .\venv\scripts\python.exe

from bs4 import BeautifulSoup
from selenium import webdriver
# import pandas as pd
import time

# df = pd.DataFrame(columns=['Brand', 'Model', 'Description', 'Color', 'Price'])

# display local time
print(time.strftime("%H:%M:%S", time.localtime()))

# Open website
browser = webdriver.Chrome()

url = 'https://www.orpi.com/recherche/buy?transaction=buy&resultUrl=&locations%5B0%5D%5Bvalue%5D=ile-de-france&locations%5B0%5D%5Blabel%5D=Ile-de-France&agency=&minSurface=40&maxSurface=&minLotSurface=&maxLotSurface=&minStoryLocation=&maxStoryLocation=&newBuild=&oldBuild=&minPrice=&maxPrice=&sort=date-down&layoutType=list&page=&recentlySold=false' # Orpi > IDF ; 40m² min
browser.get(url)

# get all page data
soup = BeautifulSoup(browser.page_source, 'html.parser')
# soup = soup.encode("utf-8")


all_items = soup.find_all('div', attrs={'class':'c-box__inner c-box__inner--sm c-overlay'})

for item in all_items:

    item_descr = item.find('span')


    # item_descritpions = item.find_all('div', attrs={'class':'o-grid'})

    print(item_descr)
    print("\n")













# TODO
    # CONTINUE AND GET STUFF FROM SCRAPPED PAGE