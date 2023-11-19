from bs4 import BeautifulSoup
import requests
import pandas as pd
import csv

# Function to format the data and print result
def print_phone_data(phone_data_format, csv_writer):
    for record in phone_data_format:
        csv_writer.writerow(record)
        
num_pages_to_scrape = 50
base_url = 'https://www.jumia.com.ng/mobile-phones/?shipped_from=country_local&page='
url_separator = '#catalog-listing'
headers = {'User-Agent': 'Chrome/58.0.3029.110'}


phone_data_format_all_pages = []

# Loop through the specified number of pages
for page_num in range(1, num_pages_to_scrape + 1):
    url = base_url + str(page_num) + url_separator
    response = requests.get(url)
    soupcontent = BeautifulSoup(response.content, 'html.parser')
    
    phones = soupcontent.find_all('div', {'class': 'info'})
    phone_data_format =[]
    for i in phones:
        name_element = i.find('h3', {'class': 'name'})
        price_element = i.find('div', {'class': 'prc'})
        official_store_element = i.find('div', {'class': 'bdg _mall _xs'})
        discount_element = i.find('div', {'class': 'bdg _dsct _sm'})
        rating_element = i.find('div', {'class':'rev'})
        old_element = i.find('div', {'class':'old'})

    # Check if elements are found before accessing their text
        if name_element:
            name = name_element.get_text().replace('\xa0', ' ')
        else:
            name = 'N/A'

        if price_element:
            price = price_element.get_text().replace('\xa0', ' ')
        else:
            price = 'N/A'

        if official_store_element:
            official_store = official_store_element.get_text().replace('\xa0', ' ')
        else:
            official_store = 'N/A'

        if discount_element:
            discount = discount_element.get_text().replace('\xa0', ' ')
        else:
            discount = 'N/A'
        
        if rating_element:
            rating = rating_element.get_text().replace('\xa0', ' ')
        else:
            rating = 'N/A'
        
        if old_element:
            old_price = old_element.get_text().replace('\xa0', ' ')
        else:
            old_price = 'N/A'
        

    # Format the data
        format_name = ' '.join(name.strip().replace('\n', '').split())
        format_price = ' '.join(price.strip().replace('₦', '').split())
        format_official_store = ' '.join(official_store.strip().replace('\n', '').split())
        format_discount = ' '.join(discount.strip().replace('%', '').split())
        format_rating = ' '.join(rating.strip().replace('\n', '').split())
        format_old = ' '.join(old_price.strip().replace('₦', '').split())

    # Print formatted phone details
        record = [format_name, format_price, format_official_store, format_discount, format_rating, format_old]
        phone_data_format.append(record)
    
    # Extend the phone_data_format_all_pages list with the data from the current page
    phone_data_format_all_pages.extend(phone_data_format)

csv_file_path = 'Jumia1.csv'
with open(csv_file_path, 'w', newline = '', encoding = 'utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    
    # Write Header
    csv_writer.writerow(['Phone Name', 'Price', 'Official Store', 'Discount', 'Rating', 'old price'])
    
    # Write data
    print_phone_data(phone_data_format_all_pages, csv_writer)
    
print(f'data has been saved to {csv_file_path}')

