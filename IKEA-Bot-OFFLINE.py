# IKEA Bot - OFFLINE File for scraping

import json
import pprint
import pandas as pd

with open('products.json') as file:
    file = file.read()

products = json.loads(file)
# print(products)

with open('store_locator.json') as f:
    f = f.read()

store_locator = json.loads(f)
# print(store_locator)

## USE ZIP() Function to iterate over multiple lists at the same time. 

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
        'stock_amount': stock_amount,
        'item_number': item_number,
        'update_date': update_date,
    }

    IKEA_product.append(product)

# pprint.pprint(IKEA_product)

for store, product in zip(IKEA_stores, IKEA_product):
    combined = store | product
    #pprint.pprint(combined)
    
df_stores = pd.DataFrame(IKEA_stores)
df_products = pd.DataFrame(IKEA_product)
combined_df = pd.concat([df_stores, df_products], axis=1)
# print(combined_df.head())
combined_df.to_csv('IKEA-Item-Inventory.csv')
print('Items saved to CSV file.')


# TO-DO: 
## Add aisle and bin (if available)
## See if item URL is available
## If item URL is available, concatenate with store URL

# BUGS: