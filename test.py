#! .\im_venv\scripts\python.exe

from random import randint
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import re


df = pd.DataFrame(columns=['Bedrooms', 'Bathrooms', 'Test', 'Terrasse'])

bedroom_list = []
bathroom_list = []
test_list = []
terrasse_list = []



browser = webdriver.Chrome()

url = f'https://www.orpi.com/annonce-vente-maison-t4-vigneux-sur-seine-91270-b-e17039/' 

browser.get(url)

soup = BeautifulSoup(browser.page_source, 'html.parser')

all_details = soup.find_all('p', attrs={'class':'u-flex u-flex-cross-center'})

bedroom = None
bathroom = None
test = None
terrasse = None

for detail in all_details:

    

    #bedroom
    if detail.find('path')['d'] == 'M82.3 19.9v-9.5C82.3 4.7 77.7 0 71.9 0H18.5C12.7 0 8.1 4.7 8.1 10.4v9.5C3.2 21.7 0 26.3 0 31.5V47c0 3.1 2.5 5.6 5.6 5.6h79.2c3.1 0 5.6-2.5 5.6-5.6V31.5c0-5.2-3.2-9.8-8.1-11.6zm4.1 27c0 .9-.7 1.6-1.6 1.6H5.6c-.9 0-1.6-.7-1.6-1.6V31.5c0-4.6 3.7-8.3 8.3-8.3H78c4.6 0 8.3 3.7 8.3 8.3v15.4zM18.5 4h53.4c3.5 0 6.4 2.9 6.4 6.4v8.7h-7.8c-.6-5.2-5.1-9.2-10.3-9.2h-3.4c-5.3 0-9.7 4-10.3 9.2h-2.6c-.6-5.2-5.1-9.2-10.3-9.2h-3.4c-5.3 0-9.7 4-10.3 9.2h-7.8v-8.7C12.1 6.9 15 4 18.5 4zm21.4 15.1h-16c.6-3 3.2-5.2 6.3-5.2h3.4c3 .1 5.7 2.2 6.3 5.2zm26.6 0h-16c.6-3 3.2-5.2 6.3-5.2h3.4c3.1.1 5.7 2.2 6.3 5.2z':
        print(re.findall(r'\d+', detail.find('span').get_text())[0])
        bedroom = re.findall(r'\d+', detail.find('span').get_text())[0]

    #bathroom
    if detail.find('path')['d'] == 'M84.7 46.1V12.3C84.7 5.5 79.2 0 72.4 0S60.2 5.5 60.2 12.3v.4c-5.3 1-9.1 5.6-9.2 10.9v2h22.4v-2c-.1-5.4-3.9-10-9.2-10.9v-.4c0-4.6 3.7-8.3 8.3-8.3s8.3 3.7 8.3 8.3v33.2H4.5C2 45.5 0 47.5 0 50v2.8c0 1.6.9 3.1 2.3 3.9v9.8c0 5.8 3.7 10.9 9.2 12.6l-5.7 9.5c-.6.9-.3 2.2.7 2.7s2.2.3 2.7-.7l6.6-10.9h55.5l6.6 10.9c.6.9 1.8 1.3 2.7.7s1.3-1.8.7-2.7l-5.7-9.5c5.5-1.8 9.2-6.9 9.2-12.6v-9.8c1.4-.8 2.3-2.3 2.3-3.9V50c-.1-1.6-1-3.1-2.4-3.9zM69.1 21.6H55.3c1.1-3.8 5.1-6 9-4.8 2.2.6 4.1 2.5 4.8 4.8zM4 50c0-.2.2-.5.4-.5h78.1c.2 0 .5.2.5.4v2.8c0 .2-.2.5-.4.5H4.5c-.2 0-.5-.2-.5-.4V50zm76.7 16.5c0 5.1-4.2 9.3-9.3 9.3H15.6c-5.1 0-9.3-4.2-9.3-9.3v-9.2h74.4v9.2z':
        print(detail.find('span').get_text())
        bathroom = detail.find('span').get_text()

    #Cuisine equipee
    if detail.find('path')['d'] == 'M88.9 46.6c0-5.3-4.3-9.7-9.7-9.7h-1.1c-1.3-1.8-3.4-2.8-5.5-2.8H16.2c-2.2 0-4.2 1-5.5 2.8H9.5C4.2 37-.1 41.4 0 46.7c.1 5.1 4.1 9.3 9.2 9.5v19c0 8.8 7.1 15.9 15.9 15.9h38.5c8.8 0 15.9-7.1 15.9-15.9v-19c5.2-.1 9.4-4.4 9.4-9.6zM13.2 72.5v-7.9h62.3v7.9H13.2zm3-34.4h56.4c1.6 0 2.9 1.3 2.9 2.9v19.6H13.2V41.1c0-1.6 1.4-3 3-3zM3.9 46.6c0-3 2.4-5.5 5.4-5.6V52.3c-3.1-.2-5.4-2.7-5.4-5.7zm59.7 40.6H25.2c-6.1 0-11.2-4.6-11.8-10.6h62.1c-.7 6-5.8 10.6-11.9 10.6zm15.9-34.9V41.1 41c3.1.1 5.5 2.8 5.4 5.9-.1 2.9-2.4 5.2-5.4 5.4zM13.4 29.6h61.9c1.1 0 2-.9 2-2 0-.4-.1-.8-.4-1.2-6.4-8.6-15.9-14.3-26.5-15.9 1.9-3.3.8-7.6-2.5-9.6-3.3-1.9-7.6-.8-9.6 2.5-1.3 2.2-1.3 4.9 0 7-10.6 1.6-20.1 7.3-26.5 15.9-.7.9-.5 2.1.4 2.8.4.4.8.5 1.2.5zm28-22.5c0-1.7 1.3-3 3-3s3 1.3 3 3-1.3 3-3 3c-1.6 0-3-1.3-3-3zm3 7c10.1 0 19.8 4.1 26.7 11.6H17.7c6.9-7.5 16.6-11.7 26.7-11.6z':
        print(detail.find('span').get_text())
        test = detail.find('span').get_text()

    #Terrasse
    if detail.find('path')['d'] == 'M244.9 239.4h-39.2v-72.2h112.1c2.1 0 4-1.1 5-2.9 1-1.8 1-4-.1-5.8-25.5-41.1-69-66.3-117-68.1V84c0-3.1-2.5-5.7-5.7-5.7s-5.7 2.5-5.7 5.7v6.3c-48 1.9-91.4 27-117 68.1-1.1 1.8-1.1 4-.1 5.8 1 1.8 2.9 2.9 5 2.9h112.1v72.2h-39.2c-3.1 0-5.7 2.5-5.7 5.7s2.5 5.7 5.7 5.7h39.2V316c0 3.1 2.5 5.7 5.7 5.7s5.7-2.5 5.7-5.7v-65.2h39.2c3.1 0 5.7-2.5 5.7-5.7S248 239.4 244.9 239.4zM200 101.6c42.8 0 82.1 20.1 107.1 54.2H92.9C117.9 121.7 157.2 101.6 200 101.6zM133.6 269.1c-.8-2.2-3-3.7-5.3-3.7H79.9l-5.4-14.6h38.8c3.1 0 5.7-2.5 5.7-5.7s-2.5-5.7-5.7-5.7h-43L61 214.1c-1.1-3-4.4-4.5-7.3-3.4-3 1.1-4.5 4.4-3.4 7.3l19.9 54.1V316c0 3.1 2.5 5.7 5.7 5.7s5.7-2.5 5.7-5.7v-39.2h42.7l15.3 41.2c.9 2.3 3 3.7 5.3 3.7.7 0 1.3-.1 2-.4 2.9-1.1 4.4-4.4 3.3-7.3L133.6 269.1zM346.3 210.7c-2.9-1.1-6.2.4-7.3 3.4l-9.3 25.3h-43c-3.1 0-5.7 2.5-5.7 5.7s2.5 5.7 5.7 5.7h38.8l-5.4 14.6h-48.4c-2.4 0-4.5 1.5-5.3 3.7L249.6 314c-1.1 2.9.4 6.2 3.3 7.3.7.2 1.3.4 2 .4 2.3 0 4.5-1.4 5.3-3.7l15.3-41.2h42.7V316c0 3.1 2.5 5.7 5.7 5.7s5.7-2.5 5.7-5.7v-43.9l19.9-54.1C350.7 215.1 349.2 211.8 346.3 210.7z':
        print(detail.find('span').get_text())
        terrasse = detail.find('span').get_text()

bedroom_list.append(bedroom)
bathroom_list.append(bathroom)
test_list.append(test)
terrasse_list.append(terrasse)
    
df['Bedrooms'] = bedroom_list
df['Bathrooms'] = bathroom_list
df['Test'] = test_list
df['Terrasse'] = terrasse_list

print(df.iloc[0:])


# TO KEEP

# chambre 
# salle de bain 
# terrain 
# cuisine équipée  0 1
# places de parking
# garage 0 1
# terrasse
# piscine 0 1
# cave 0 1
# date de construction
# cb étages

