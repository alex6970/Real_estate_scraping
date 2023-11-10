#! .\im_venv\scripts\python.exe

from time import localtime, sleep, strftime
from tqdm import tqdm
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
from random import randint
import re
import warnings
warnings.filterwarnings("ignore")


# var declarations
df = pd.DataFrame(columns=['Type', 'Rooms', 'Size', 'Location', 'Price', 'Region', 'Bedrooms', 'Bathrooms', 'Equipped kitchen',
                  'Terrace/Balcony', 'Parking space', 'Ground', 'Garage', 'Pool', 'Cellar', 'Construction date', 'Construction materials'])

# basic details
type_list = []
rooms_list = []
size_list = []
location_list = []
price_list = []
region_loc_list = []

# specific details
bedroom_list = []
bathroom_list = []
kitchentype_list = []
terrace_list = []
parkingspace_list = []
ground_list = []
garage_list = []
pool_list = []
cellar_list = []
consdate_list = []
consmaterials_list = []

regions_list = ["ile-de-france", "pays-de-la-loire",
                "nouvelle-aquitaine", "provence-alpes-cote-d-azur"]

# display local time
start_time = strftime("%H:%M:%S", localtime())
print(start_time)

# Open website
browser = webdriver.Chrome()

# Region choice
for region in range(0, 1):
    # for i in tqdm(range(0,4), desc='Total progress'):
    #
    url_reg = f'https://www.orpi.com/recherche/buy?transaction=buy&resultUrl=&locations%5B0%5D%5Bvalue%5D={regions_list[region]}&agency=&minSurface=40&maxSurface=&minLotSurface=&maxLotSurface=&minStoryLocation=&maxStoryLocation=&newBuild=&oldBuild=&minPrice=&maxPrice=&sort=date-down&layoutType=list&page'

    # Scrap data from the 30 first pages of the website
    for page in range(2):

        url = f'{url_reg}={page}'

        browser.get(url)

        # get all page data
        soup = BeautifulSoup(browser.page_source, 'html.parser')

        all_items = soup.find_all('div', attrs={'class': 'c-box__inner c-box__inner--sm c-overlay'})

        for item in all_items:

            region_loc_list.append(regions_list[region])

            item_type = item.find('a').find(text=True, recursive=False).strip()
            type_list.append(item_type)

            item_rooms = item.find('span').find('b').find(recursive=False).get_text()
            rooms_list.append(item_rooms)

            # In case there is no size specified
            try:
                item_space = item.select('span b')[2].get_text(strip=True)
                size_list.append(item_space)

            except IndexError:
                size_list.append("No info")

            item_price = item.find('strong', 'u-text-md u-color-primary').get_text()

            item_price = item_price.replace("€", "").strip()
            price_list.append(item_price)

            item_location = item.find('p', 'u-mt-sm').get_text()
            location_list.append(item_location)

            # scrape details from each house page
            details_url = "https://www.orpi.com" + item.find('a', 'u-link-unstyled c-overlay__link')['href']
            print(details_url)

            browser.get(details_url)
            soup = BeautifulSoup(browser.page_source, 'html.parser')

            all_details = soup.find_all('p', attrs={'class': 'u-flex u-flex-cross-center'})

            bedroom = None
            bathroom = None
            kitchen = 'No'
            terrace = 'No'
            parkingspace = 0
            ground = 0
            garage = 'No'
            pool = 'No'
            cellar = 'No'
            constr_date = None
            constr_materials = None

            for detail in all_details:
                # bedroom
                if 'M82.3 19.9v-9.5C82.3 4.7 77.7 0 71.9 0H18.5C12.7' in detail.find('path')['d']:
                    print(detail.find('span').get_text())
                    bedroom = re.findall(r'\d+', detail.find('span').get_text())[0] # gets only numerical value

                # bathroom
                if 'M84.7 46.1V12.3C84.7 5.5 79.2 0 72.4 0S60.2 5.5 60.2' in detail.find('path')['d']:
                    print(detail.find('span').get_text())
                    bathroom = re.findall(r'\d+', detail.find('span').get_text())[0] # gets only numerical value

                # equipped kitchen
                if 'M88.9 46.6c0-5.3-4.3-9.7-9.7-9.7h-1.1c-1.3-1.8-3.4-2' in detail.find('path')['d']:
                    print(detail.find('span').get_text())
                    kitchen = 'Yes'

                # terrace or balcony
                if 'M244.9 239.4h-39.2v-72.2h112.1c2.1 0 4-1.1 5-2.9 1-1.8' in detail.find('path')['d'] or 'M89.18,61.39h-.3v-22a2,2,0,0,0-2-2H80.35a2,2,0,0,0-2,2v.43h-10V2a2,2' in detail.find('path')['d']:
                    print(detail.find('span').get_text())
                    terrace = 'Yes'

                # parking space
                if 'M30.5 74.7h-5.9c-2.8.1-5.1-2.1-5.1-4.9V18.5c-.1-2.8' in detail.find('path')['d']:
                    print(detail.find('span').get_text())
                    parkingspace = re.findall(r'\d+', detail.find('span').get_text())[0]

                # ground
                if 'M89.7 40.9L78.9 30.2h1.3c1.9 0 3.5-1.5 3.5-3.4v-1.1c.1' in detail.find('path')['d']:
                    print(detail.find('span').get_text())
                    ground = re.findall(r'\d+', detail.find('span').get_text().replace(u'\xa0', ""))[0] # removes &nbsp; separator

                # garage
                if 'M24.08 72.07A6.08 6.08 0 0030.19 66a6.2 6.2 0 00-6.11-6.12' in detail.find('path')['d']:
                    print(detail.find('span').get_text())
                    garage = 'Yes'

                # pool
                if 'M25.53 52.11a13.71 13.71 0 0023.52 0A13.75 13.75 0 0074.58' in detail.find('path')['d']:
                    print(detail.find('span').get_text())
                    pool = 'Yes'

                # cave
                if 'M88.5,26.23,45.77.29a2,2,0,0,0-2.08,0L1,26.23a2,2,0' in detail.find('path')['d']:
                    print(detail.find('span').get_text())
                    cellar = 'Yes'

                # construction date
                if 'M60.5 20.8c-1.1-.2-2.1.4-2.4 1.5l-6.3 28c-.2 1.1.4' in detail.find('path')['d']:
                    print(detail.find('span').get_text())
                    constr_date = re.findall(r'\d+', detail.find('span').get_text())[0]
                    # try:
                    #     constr_date = re.findall(r'\d+', detail.find('span').get_text())[0]

                    # except AttributeError:
                    #     print(details_url)

                # construction materials
                if 'M102.7 35.4V22.1c0-2.4-1.9-4.3-4.3-4.3H86.2V4.3C86.2' in detail.find('path')['d']:
                    print(detail.find('span').get_text())
                    constr_materials = detail.find('span').get_text().split()[-1]  # gets last word of the sentence

            bedroom_list.append(bedroom)
            bathroom_list.append(bathroom)
            kitchentype_list.append(kitchen)
            terrace_list.append(terrace)
            parkingspace_list.append(parkingspace)
            ground_list.append(ground)
            garage_list.append(garage)
            pool_list.append(pool)
            cellar_list.append(cellar)
            consdate_list.append(constr_date)
            consmaterials_list.append(constr_materials)

            print('\n')

    # time.sleep(randint(2,10)) # crawling in short random bursts of time/avoid ip ban

# Storing all data in the dataset
df['Type'] = type_list
df['Rooms'] = rooms_list
df['Size'] = size_list
df['Price'] = price_list
df['Location'] = location_list
df['Region'] = region_loc_list

df['Bedrooms'] = bedroom_list
df['Bathrooms'] = bathroom_list
df['Equipped kitchen'] = kitchentype_list
df['Terrace/Balcony'] = terrace_list
df['Parking space'] = parkingspace_list
df['Ground'] = ground_list
df['Garage'] = garage_list
df['Pool'] = pool_list
df['Cellar'] = cellar_list
df['Construction date'] = consdate_list
df['Construction materials'] = consmaterials_list

# Final insights
print(df.iloc[:5])
print("\n")
print(len(df), "items have been scraped.")
print("\n")
print(df.shape)

# storing the dataframe as a CSV file
df.to_csv('./datasets/real_estate_paris_orpi_df.csv', index=False, encoding='utf-8')


# TODO :
#   Correctcly scrap basic +specific data & merge branch
#   Add tqm/progress bar and check on performance
#   pip freeze
#   PowerBI Analysis and push to github


# https://www.orpi.com/recherche/buy?locations%5B0%5D%5Bvalue%5D=ile-de-france&locations%5B0%5D%5Blabel%5D=Ile-de-France%20-%20R%C3%A9gion&sort=date-down&layoutType=mixte&recentlySold=false

# https://www.orpi.com/recherche/buy?locations%5B0%5D%5Bvalue%5D=pays-de-la-loire&locations%5B0%5D%5Blabel%5D=Pays%20de%20la%20Loire%20-%20R%C3%A9gion&sort=date-down&layoutType=mixte&recentlySold=false
