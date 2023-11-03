#! .\im_venv\scripts\python.exe

from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import time

df = pd.DataFrame(columns=['Type', 'Rooms', 'Size', 'Location', 'Price'])

type_list = []
rooms_list = []
size_list = []
location_list = []
price_list = []

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

    item_type = item.find('a').find(text=True, recursive=False).strip()
    type_list.append(item_type)

    item_rooms = item.find("span").find("b").find(recursive=False).get_text()
    rooms_list.append(item_rooms)

    item_space = item.select("span b")[2].get_text(strip=True)
    size_list.append(item_space)
    
    item_price = item.find("strong", "u-text-md u-color-primary").get_text()
    item_price = item_price.replace("€","").strip()
    price_list.append(item_price)

    item_location = item.find("p", "u-mt-sm").get_text()
    location_list.append(item_location)


    print(item_type)
    print(item_rooms)
    print(item_space)
    print(item_price)
    print(item_location)
    print("\n")


df['Type'] = type_list
df['Rooms'] = rooms_list
df['Size'] = size_list
df['Price'] = price_list
df['Location'] = location_list

print(df.iloc[0:])
print(len(df), "items have been scraped from this category.")
print(df.shape)








# TODO
    # push github
    # CONTINUE AND scrap multiple paages then store in df