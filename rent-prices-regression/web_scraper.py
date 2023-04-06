# author: Jacek Spalinski

from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

URL = 'https://gaijinpot.com'
DRIVER = '/home/jack/PJATK/PAD/chromedriver'
driver = webdriver.Chrome(DRIVER)
driver.get(URL)

driver.maximize_window()

# filter apratment search only for Tokyo 23 wards area
try:
    apartments = driver.find_element(by=By.XPATH, value='//*[@id="__layout"]/div/div[1]/header/nav/ul/li[4]/a')
    apartments.click()
    filter = driver.find_element(by=By.XPATH, value='//*[@id="prefecture"]')
    filter.click()
    tokyo = driver.find_element(by=By.XPATH, value='//*[@id="prefecture"]/option[2]')
    tokyo.click()
    city = driver.find_element(by=By.XPATH, value='//*[@id="city"]')
    city.click()
    time.sleep(1) # delay needed for webpage to load dynamic searching options
    wards23 = driver.find_element(by=By.XPATH, value='//*[@id="city"]/option[2]')
    wards23.click()
    search = driver.find_element(by=By.XPATH, value='//*[@id="top"]/div[2]/div[2]/div[1]/div[2]/form/div/div[14]/input')
    search.click()
except:
    print('Tried to access non-existing element')


data = {"apartment_type": [],
        "district": [],
        "agency": [],
        "size": [],
        "floor": [],
        "year_built": [],
        "station_distance": [],
        "cost": []
        }

# I decided to get 6000 observation, there are 15 apartments per page, so I need to browse 400 pages
for i in range(1, 401):
    for j in range(1, 16):
        
        # I create seperate try / except for each attribute, in order to in case of error know exactly what went wrong

        try:
            apart = driver.find_element(by=By.XPATH, value=f'//*[@id="top"]/div[2]/div[1]/div[1]/div[{j}]/div[1]/div[2]/div[1]/a/span').text
            data['apartment_type'].append(apart)
        except:
            data['apartment_type'].append('?')
            print(f'Tried to access non-existing element apartment_type for element number {j} at page {i}')

        try: 
            district = driver.find_element(by=By.XPATH, value=f'//*[@id="top"]/div[2]/div[1]/div[1]/div[{j}]/div[1]/div[2]/div[1]/span').text
            data['district'].append(district)
        except:
            data['district'].append('?')
            print(f'Tried to access non-existing element district for element number {j} at page {i}')

        try: 
            agency = driver.find_element(by=By.XPATH, value=f'//*[@id="top"]/div[2]/div[1]/div[1]/div[{j}]/div[3]/a/span/small').get_attribute("innerHTML")
            data['agency'].append(agency)
        except:
            data['agency'].append('?')
            print(f'Tried to access non-existing element agency for element number {j} at page {i}')

        try:
            size = driver.find_element(by=By.XPATH, value=f'//*[@id="top"]/div[2]/div[1]/div[1]/div[{j}]/div[1]/div[3]/div[2]/div[1]').text
            data['size'].append(size)
        except:
            data['size'].append('?')
            print(f'Tried to access non-existing element size for element number {j} at page {i}')

        try:
            floor = driver.find_element(by=By.XPATH, value=f'//*[@id="top"]/div[2]/div[1]/div[1]/div[{j}]/div[1]/div[3]/div[2]/div[4]').text
            data['floor'].append(floor)
        except:
            data['floor'].append('?')
            print(f'Tried to access non-existing element floor for element number {j} at page {i}')

        try:
            year = driver.find_element(by=By.XPATH, value=f'//*[@id="top"]/div[2]/div[1]/div[1]/div[{j}]/div[1]/div[3]/div[2]/div[5]').text
            data['year_built'].append(year)
        except:
            data['year_built'].append('?')
            print(f'Tried to access non-existing element year_built for element number {j} at page {i}')

        try:
            dist = driver.find_element(by=By.XPATH, value=f'//*[@id="top"]/div[2]/div[1]/div[1]/div[{j}]/div[1]/div[3]/div[2]/div[6]/span[2]').text
            data['station_distance'].append(dist)
        except:
            data['station_distance'].append('?')
            print(f'Tried to access non-existing element station_distance for element number {j} at page {i}')

        try:
            cost = driver.find_element(by=By.XPATH, value=f'//*[@id="top"]/div[2]/div[1]/div[1]/div[{j}]/div[1]/div[2]/div[2]').text
            data['cost'].append(cost)
        except:
            data['cost'].append('?')
            print(f'Tried to access non-existing element cost for element number {j} at page {i}')
        
    try:
        next = driver.find_element(by=By.XPATH, value='//*[@id="top"]/div[2]/div[1]/div[2]/ul/li[3]/ul/li[1]/a')
        next.click()
    except:
        print('Could not move to the next page')
        break


df = pd.DataFrame(data)
df.to_csv('./apartments_data.csv')

driver.quit()