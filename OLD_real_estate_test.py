from requests_html import HTMLSession
from bs4 import BeautifulSoup
import re
import time
import pandas as pd


s = HTMLSession()
url = 'https://www.imoti.net/bg/obiavi/r/prodava/sofia/?page=1&sid=iJKYgL'
link_to_add = 'https://www.imoti.net'

r = s.get(url)
soup_for_last_page = BeautifulSoup(r.text, 'html.parser')


# Get all the data from the page
def getdata(url):
    r = s.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    # print(soup)
    return soup


def getnextpage(soup):
    page = soup.find('nav', {'class': 'paginator'})
    if page.find('a', {'class': 'next-page-btn'}):
        url = str(page.find('a', {'class': 'next-page-btn'})['href'])
        return url
    else:
        return


last_page = soup_for_last_page.find('a', {'class': 'last-page'})
last_page_number = int(last_page.get_text())

urls = []
for page in range(1, last_page_number + 1):
    url = f'https://www.imoti.net/bg/obiavi/r/prodava/sofia/?page={page}&sid=iJKYgL'
    urls.append(url)

date_for_each_sheet = time.strftime("%Y%m%d")


# while True:
#     soup = getdata(url)
#     url = getnextpage(soup)
#     if not url:
#         break
#     urls.append(url)
#     #print(url)


prices = []
type_of_property = []
sqm_area = []
locations = []
publisher = []
price_per_m2 = []
link_for_offer = []


def if_parking_space(x):
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


def get_link_for_offer(links):
    for i in links:
        soup = getdata(i)
        for link in soup.find('ul', {'class': 'list-view real-estates'}).find_all('a', {'class': 'box-link'}):
            get_only_link = str(link).split('"')[3]
            get_the_pages_removed = get_only_link.split(';')[0]
            add_link = link_to_add + get_the_pages_removed
            link_for_offer.append(add_link)
    return link_for_offer


def get_sqm(links):
    for i in links:
        soup = getdata(i)
        for sqm in soup.find('ul', {'class': 'list-view real-estates'}).find_all('div', {'class': 'inline-group'}):
            sqm_value = sqm.get_text().split(',')[1].split()[0]
            sqm_value_check = if_parking_space(sqm_value)
            sqm_area.append(sqm_value_check)
    return sqm_area


def get_location(links):
    for i in links:
        soup = getdata(i)
        for location in soup.find('ul', {'class': 'list-view real-estates'}).find_all('div', {'class': 'inline-group'}):
            location_value = location.get_text().split(',')[-1].strip()
            locations.append(location_value)
    return locations


def get_type(links):
    for i in links:
        soup = getdata(i)
        for property_type in soup.find('ul', {'class': 'list-view real-estates'}).find_all('div', {'class': 'inline-group'}):
            property_type_value = ' '.join(
                property_type.get_text().split(',')[0].split()[1:3])
            type_of_property.append(property_type_value)
    return type_of_property


def get_publisher(links):
    for i in links:
        soup = getdata(i)
        for publish in soup.find('ul', {'class': 'list-view real-estates'}).find_all('span', {'class': 're-offer-type'})[1::2]:
            publish_value = publish.get_text().strip()
            publisher.append(publish_value)
    return publisher


def get_price_per_m2(links):
    for i in links:
        soup = getdata(i)
        for price_per_m2_ in soup.find('ul', {'class': 'list-view real-estates'}).find_all('ul', {'class': 'parameters'}):
            price_per_m2_value = price_per_m2_0(price_per_m2_)
            price_per_m2.append(price_per_m2_value)
    return price_per_m2


def total_price(links):
    for i in links:
        soup = getdata(i)
        for price in soup.find('ul', {'class': 'list-view real-estates'}).find_all('strong', {'class': 'price'}):
            price_text = price.get_text()
            price_arr = re.findall('[0-9]+', price_text)
            final_price = ''
            for each_sub_price in price_arr:
                final_price += each_sub_price
            prices.append(final_price)
    return prices


get_sqm(urls)
get_location(urls)
get_type(urls)
get_publisher(urls)
get_price_per_m2(urls)
total_price(urls)
get_link_for_offer(urls)

print(prices)
print(type_of_property)
print(sqm_area)
print(locations)
print(publisher)
print(price_per_m2)
print(link_for_offer)

# Get IDs for each real estate
ids = []


def get_id(x):
    for i in x:
        get_the_id = i.split('/')[-2]
        ids.append(get_the_id)


get_id(link_for_offer)

# Export all data to a new Excel File.

dataframe_for_excel_file_structure = {'id': pd.Series(ids) ,'date': date_for_each_sheet, 'type_of_property': pd.Series(type_of_property), 'area': pd.Series(sqm_area), 'location': pd.Series(
    locations), 'price_per_m2': pd.Series(price_per_m2), 'total_price': pd.Series(prices), 'published_by': pd.Series(publisher), 'link': pd.Series(link_for_offer)}
dataframe_for_excel = pd.DataFrame(dataframe_for_excel_file_structure)


filename_for_sqm = time.strftime("%Y%m%d")
dataframe_for_excel.to_excel(filename_for_sqm + '.xlsx')
