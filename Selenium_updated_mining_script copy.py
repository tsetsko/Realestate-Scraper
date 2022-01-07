from requests_html import HTMLSession
from bs4 import BeautifulSoup
import re
import pandas as pd
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

PATH = '/Applications/chromedriver'
driver = webdriver.Chrome(PATH)

# Paste the link from which you want to extrac  t data here. Make sure that the link is pasted after you have clicked
# on the first page at the bottom of the page.

s = HTMLSession()
url = 'https://www.imoti.net/bg/obiavi/r/prodava/sofia-oblast/?page=1&sid=fZ1ULc'

r = s.get(url)
soup_for_last_page = BeautifulSoup(r.text, 'html.parser')


# Get all the data from the page
def getdata(url):
    r = s.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    # print(soup)
    return soup


def if_area_not_speicified(x):
    if x == 'паркомясто':
        return -1
    elif x == 'Таван':
        return -2
    else:
        return x


def price_per_m2_0(x):
    if x.get_text().strip().find('/:') == -1:
        return 0
    else:
        return float(x.get_text().strip().split('/:')[1].strip().replace('EUR', '').strip().replace(' ', ''))


link_for_offer = []
sqm_area = []
locations = []
property_type = []
agency = []
price_per_m2 = []
intermediate_prices = []
prices = []
location_area = []
description = []


def get_data(link):
    soup1 = getdata(link)
    for one_offer in soup1.find_all('li', {'class': 'clearfix'}):

        # Get the links:
        link_to_add = 'https://www.imoti.net'
        raw_link = one_offer.find('a', {'class': 'box-link'})
        get_each_link = str(raw_link).split('"')[3]
        remove_the_pages_from_the_link = get_each_link.split(';')[0]
        complete_link = link_to_add + remove_the_pages_from_the_link
        link_for_offer.append(complete_link)

        # Get sqm:
        raw_sqm = one_offer.find('div', {'class': 'inline-group'})
        get_sqm = raw_sqm.get_text().split(',')[1].split()[0]
        sqm_check_value = if_area_not_speicified(get_sqm)
        sqm_area.append(float(sqm_check_value))

        # Get the location of the property:
        raw_location = one_offer.find('div', {'class': 'inline-group'})
        get_general_location = raw_location.find('span', {'class': 'location'}).get_text().split(',')[0]
        location_area.append(get_general_location)
        get_location_city = raw_location.get_text().split(',')[-1].strip()
        locations.append(get_location_city)

        # Get the type of property:
        raw_property_type = one_offer.find('div', {'class': 'inline-group'})
        property_type_value = ' '.join(raw_property_type.get_text().split(',')[0].split()[1:3])
        property_type.append(property_type_value)

        # Get real estate agency:
        publisher = one_offer.find_all('span', {'class': 're-offer-type'})[1]
        publisher_value = publisher.get_text().strip()
        agency.append(publisher_value)

        # Get price per sqm.m
        raw_price_per_m2 = one_offer.find('ul', {'class': 'parameters'})
        price_per_m2_value = price_per_m2_0(raw_price_per_m2)
        price_per_m2.append(float(price_per_m2_value))

        # Get total price:
        raw_price = one_offer.find('strong', {'class': 'price'})
        price_text = raw_price.get_text()
        price_arr = re.findall('[0-9]+', price_text)
        intermediate_prices.append(''.join(price_arr))

        # Get description:
        raw_description = one_offer.find_all('p')[-1].get_text()
        description.append(raw_description)


# Get IDs for each real estate
ids = []


def get_id(x):
    for i in x:
        get_the_id = i.split('/')[-2]
        ids.append(get_the_id)


def check_if_price_is_blank(list):
    for i in list:
        if i == '':
            prices.append(-1)
        else:
            prices.append(i)


start_time = time.time()


def moving_pages():
    global driver
    driver.get(url)
    get_data(url)
    while True:
        try:
            button = driver.find_element_by_class_name('next-page-btn')
        except NoSuchElementException:
            print("NO MORE NEXT BUTTON")
            break
        time.sleep(5)
        button.click()
        new_url = driver.current_url
        get_data(new_url)


moving_pages()
get_id(link_for_offer)
check_if_price_is_blank(intermediate_prices)

print("--- %s seconds ---" % (time.time() - start_time))

date_for_each_day = time.strftime("%Y%m%d")

# Convert all of the data into pd.Series and after that to a DataFrame.

dataframe_for_csv_file_structure = {'id': pd.Series(ids), 'date': date_for_each_day, 'type_of_property':
    pd.Series(property_type), 'area': pd.Series(sqm_area), 'city_or_province': pd.Series(location_area), 'location': pd.Series(
    locations), 'price_per_m2': pd.Series(price_per_m2), 'total_price': pd.Series(prices), 'published_by': pd.Series(
    agency), 'description': pd.Series(description), 'link': pd.Series(link_for_offer)}
dataframe_for_cvs = pd.DataFrame(dataframe_for_csv_file_structure)

# Use only the first time the script is run to create the file. After the first run convert the excel into a cvs file.

# filename = 'master_data_for_realestate'
# dataframe_for_cvs.to_excel(filename + '.xlsx')

# Use this code after the first run and comment out the text above.

old_df = pd.read_csv('/Users/tdonov/Desktop/Python/Realestate Scraper/master_data_for_realestate.csv')
old_df = old_df.append(dataframe_for_cvs, ignore_index=True)
old_df.to_csv('/Users/tdonov/Desktop/Python/Realestate Scraper/master_data_for_realestate.csv', index=False)
