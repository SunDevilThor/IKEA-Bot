# IKEA Bot

import requests
import json
import pandas as pd
import pprint

product_id = input('Enter in product ID from IKEA that you wish to check inventory for: ')

product_url = f"https://api.ingka.ikea.com/cia/availabilities/ru/us?itemNos={product_id}&expand=StoresList,Restocks,SalesLocations"

# product_url = "https://api.ingka.ikea.com/cia/availabilities/ru/us?itemNos=90473151&expand=StoresList,Restocks,SalesLocations"

headers = {
  'Accept': 'application/json;version=2',
  'Origin': 'https://www.ikea.com',
  'Accept-Encoding': 'gzip, deflate, br',
  'Host': 'api.ingka.ikea.com',
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
  'Accept-Language': 'en-us',
  'Referer': 'https://www.ikea.com/us/en/p/malm-3-drawer-chest-white-90473151/',
  'Connection': 'keep-alive',
  'X-Client-ID': 'b6c117e5-ae61-4ef5-b4cc-e0b1e37f0631',
  'Cookie': '_abck=2C3D2B0B493581E6B2C4FE627FFEB5F4~-1~YAAQhmzTFxTdBsp8AQAAqFQQ/gbCNQm297aVkyA0ncQuPudkT8NhGnZQpGZ/AybuskRy73Fg0gYPfIWzBn7ymkZeJz7zGM2tWoxAwsl7KtYyvdpvVKfRU+GL30hbVUW74StDOzjQI0n+luak1B8n20ewqOWAJ77R55A+dXktcY7+F6aBgMSzZcWOgiVqz64eV5/YsazkY8sTbUXCtYk4+Y6yybx2Pe0C2Kn1eZ34ITjWL03Zfoyq98eqSp3YRXBsLm7P/qWpEQWDYZeFUsdCh1kJYJ7casDVKE/HQVMVvjDR2Frvzy6VdL859qU4CLRxAhMmPW58eGc0JloYAuLu6Gl4jlPVPeShtLoW9xOVkMkfivIZv9VE/btB6A==~-1~-1~-1; bm_sz=F19BAA7C8A79933AE141266D5F6C2229~YAAQhmzTFxbdBsp8AQAAqFQQ/g17m6sesPV3P047/CJTc4RHvq6Hqp8F+y+HD7yErKVE4bfqqL9o/jfDI0mpcQU9RFWWwv16Z8uBmfgz6ySWfaHUw6UL7iFR8IReDf/UHqBI//Z7RplO+jTpc6OT4/krwx5A4Zs2Oi98v0UmJojEC9Y1qBxKpu5YuLgk4SDWBL2xFnb+k/ONp3em7FPionUHnxE1bUZZG46S2StEtTWb77MPYDOLAf77lbQxHtsU0w6KlseqM9kCHG/iJlXb2tgyIWa8e2PTyMw0YxYoJY3A~4404276~4539701; ak_bmsc=B4DCD6397F14B3EBC575EAB5A8685708~000000000000000000000000000000~YAAQhmzTFxXdBsp8AQAAqFQQ/g2Cd7Xov9e9FkhXU2a88JUWgXFi7TtjAxXU45vQEoC/3ZduqSAIH3LnV1yrTzApZx0ganaD8qg6If2CA3vzVRJIl9GgyMX0qbNGIN5SMMKoyXFQAtnGRdqvOkNMu0RzWzwsqhfj3MpUJfGgiZpKGlgBRn8DR9izMtvsn1wtbVI28gpRhVbukDSQzSFpyblwiG9wPclFV2Nwu7YBExWATycVzB0M2nVwj4tz/dmAFQ5U47IYm85CFQZS/UzuPQfv0MLZynFEAtMgFNOVG9pE8oYN1X8cRJ7L9dckPFJ4KgRNpJgRpZKIEcvVKvtiSVsjQaADM19H82fHJAtCw+HgCVFR/elTfXa5QgzypTUqTg=='
}

store_api = "https://ww8.ikea.com/ext/iplugins/v2/en_US/data/localstorefinder/data.json"

headers2 = {
  'Cookie': '_abck=2C3D2B0B493581E6B2C4FE627FFEB5F4~-1~YAAQhmzTFxTdBsp8AQAAqFQQ/gbCNQm297aVkyA0ncQuPudkT8NhGnZQpGZ/AybuskRy73Fg0gYPfIWzBn7ymkZeJz7zGM2tWoxAwsl7KtYyvdpvVKfRU+GL30hbVUW74StDOzjQI0n+luak1B8n20ewqOWAJ77R55A+dXktcY7+F6aBgMSzZcWOgiVqz64eV5/YsazkY8sTbUXCtYk4+Y6yybx2Pe0C2Kn1eZ34ITjWL03Zfoyq98eqSp3YRXBsLm7P/qWpEQWDYZeFUsdCh1kJYJ7casDVKE/HQVMVvjDR2Frvzy6VdL859qU4CLRxAhMmPW58eGc0JloYAuLu6Gl4jlPVPeShtLoW9xOVkMkfivIZv9VE/btB6A==~-1~-1~-1; ak_bmsc=0359D5D6CE4DCF613D64436D778C9D21~000000000000000000000000000000~YAAQNC0tF/9zU/l8AQAAP71J/g3AB2jPyG3QkJk+Nh5VWXdsevFKBE8MFaRTvCuRH/FsdTczTcsySdLIvHyRblXLxb8Pq4R3jbYkS5T2SFn0xkrt70eZ7aa8VqPkGg7kekHfPM/N+f7u2Vu5lIGTZgd+qeADH8ac4skik+F2iygNT9k60tGEjtul3/AfaA8CSYR/MrpROywn89GhGE5K2P4O5QeLWx2IsyFEZMQObzSBUSP0c5kiiQWolQHwwy0rLR+/QL6gCwidaJ6czaCdCvWKLPt6gTa7+4a/UoBXIFNFcJT0zIDZMG5j3HRFbCk4sMXVIgEk9TUtEXKxG7F5N6rX3tMsa+AEi9VriJPjkJiWokfPMzWA6BxvVg==; bm_sz=F19BAA7C8A79933AE141266D5F6C2229~YAAQhmzTFxbdBsp8AQAAqFQQ/g17m6sesPV3P047/CJTc4RHvq6Hqp8F+y+HD7yErKVE4bfqqL9o/jfDI0mpcQU9RFWWwv16Z8uBmfgz6ySWfaHUw6UL7iFR8IReDf/UHqBI//Z7RplO+jTpc6OT4/krwx5A4Zs2Oi98v0UmJojEC9Y1qBxKpu5YuLgk4SDWBL2xFnb+k/ONp3em7FPionUHnxE1bUZZG46S2StEtTWb77MPYDOLAf77lbQxHtsU0w6KlseqM9kCHG/iJlXb2tgyIWa8e2PTyMw0YxYoJY3A~4404276~4539701'
}

response = requests.get(product_url, headers=headers)

response2 = requests.get(store_api, headers=headers2)

products = response.json()
store_locator = response2.json()

IKEA_product = []
IKEA_stores = []

for item in store_locator:
    store_number = item['storeNumber']
    if store_number == '':
        store_number = 0

    store_city = item['storeCity']
    store_zip = item['storeZip']
    store_state = item['storeState']
    store_address = item['storeAddress']

    # print(store_number, store_city, store_address, store_state, store_zip)

    store = {
        'store_city': store_city,
        'store_state': store_state,
        'store_number': store_number,
        'store_zip': store_zip,
        'store_address': store_address,
    }

    IKEA_stores.append(store)

# pprint.pprint(IKEA_stores)

for item in products['availabilities']:
    try:
        quantity = item['buyingOption']['cashCarry']['availability']['quantity']
    except: 
        quantity = 'N/A'
    try: 
        class_unit_code = item['classUnitKey']['classUnitCode']
    except: 
        class_unit_code = 'N/A'
    try:
        stock_amount = item['buyingOption']['cashCarry']['availability']['probability']['thisDay']['messageType']
    except:
        stock_amount = 'N/A'
    try:
        update_date = item['buyingOption']['cashCarry']['availability']['updateDateTime']
    except:
        update_date = 'N/A'
    update_date = update_date[:10]
    item_number = item['itemKey']['itemNo']
    #print(item_number)

    product = {
        'quantity': quantity, 
        'class_unit_code': class_unit_code,
        'stock_amount': stock_amount,
        'item_number': item_number,
        'update_date': update_date,
    }

    IKEA_product.append(product)

pprint.pprint(IKEA_product)

# pprint.pprint(IKEA_product)

for store, product in zip(IKEA_stores, IKEA_product):
    combined = store | product
    #pprint.pprint(combined)
    
df_stores = pd.DataFrame(IKEA_stores)
df_products = pd.DataFrame(IKEA_product)
combined_df = pd.concat([df_stores, df_products], axis=1)
# print(combined_df.head())
combined_df.to_csv(f'IKEA-Item-Inventory-{product_id}.csv')
print('Items saved to CSV file.')


# TO-DO: 
# Get item data name

# BUGS:
# 12/21/21 - stocks are not matching up with what is showing up on the website
#  -- The cause of this might be the "Update Date" in the API. 
#  --- The information might not update in real time
# Zip codes will cut off the beginning 0 (ex: 6511 instead of 06511)

# NOTES: 
# Burbank = StoreID 399 
# ClassUnitCodes do not match up with store ID numbers. 
# The site has bot detection from Akamai
