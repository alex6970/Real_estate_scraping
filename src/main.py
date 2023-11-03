#! .\im_venv\scripts\python.exe

from random import randint
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import time

# var declarations
df = pd.DataFrame(columns=['Type', 'Rooms', 'Size', 'Location', 'Price'])

type_list = []
rooms_list = []
size_list = []
location_list = []
price_list = []

# main website url
url_base = 'https://www.orpi.com/recherche/buy?transaction=buy&resultUrl=&locations%5B0%5D%5Bvalue%5D=ile-de-france&locations%5B0%5D%5Blabel%5D=Ile-de-France&agency=&minSurface=40&maxSurface=&minLotSurface=&maxLotSurface=&minStoryLocation=&maxStoryLocation=&newBuild=&oldBuild=&minPrice=&maxPrice=&sort=date-down&layoutType=list&page' # Orpi > IDF ; 40m² min

# display local time
start_time = time.strftime("%H:%M:%S", time.localtime())
print(start_time)

# Open website
browser = webdriver.Chrome()

# Scrap data from the 30 first pages of the website
for page in range(1, 30):
    
    url = f'{url_base}={page}' 

    browser.get(url)

    # get all page data
    soup = BeautifulSoup(browser.page_source, 'html.parser')


    all_items = soup.find_all('div', attrs={'class':'c-box__inner c-box__inner--sm c-overlay'})

    for item in all_items:

        item_type = item.find('a').find(text=True, recursive=False).strip()
        type_list.append(item_type)

        item_rooms = item.find("span").find("b").find(recursive=False).get_text()
        rooms_list.append(item_rooms)

        # In case there is no size specified
        try:
            item_space = item.select("span b")[2].get_text(strip=True)
            size_list.append(item_space)

        except IndexError:
            size_list.append("No info")

        item_price = item.find("strong", "u-text-md u-color-primary").get_text()
        item_price = item_price.replace("€","").strip()
        price_list.append(item_price)

        item_location = item.find("p", "u-mt-sm").get_text()
        location_list.append(item_location)

    # time.sleep(randint(2,10)) # crawling in short random bursts of time/avoid ip ban

# Storing all data in the dataset
df['Type'] = type_list
df['Rooms'] = rooms_list
df['Size'] = size_list
df['Price'] = price_list
df['Location'] = location_list

# Final insights
print(df.iloc[:5])
print("\n")
print(len(df), "items have been scraped.")
print("\n")
print(df.shape)

# storing the dataframe as a CSV file
df.to_csv('real_estate_paris_orpi_df.csv', index=False, encoding='utf-8')


# TODO :
#   Scrap from multiple regions (website filter)
#   Get more characteristics/info from house description page
