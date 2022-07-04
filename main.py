#!/usr/bin/env python
# coding: utf-8

# In[2]:

import pandas as pd
import numpy as np
import time

import re
import logging
import sys

# from utils import zealty_data_scrape
from utils import clean_data
# from utils import connect_to_db
# import zealty_data_scrape

# In[2]:

logging.getLogger().setLevel(logging.INFO)

if __name__ == "__main__":

     
    with open('scripts//zealty_data_scrape.py') as infile:
        exec(infile.read())
    
    if len(results) > 0:
        data = clean_data.clean_transform_df(results)
        
    else:
        logging.info("There is no new data today")
        sys.exit()

    # Address
    data["Street Address"] = data["Address"].apply(lambda x: clean_data.clean_split_element(x, attribute = "Street"))
    data['Postal Code'] =  data["Address"].apply(lambda x: clean_data.clean_postal_code(x))
    data['Neighborhood'] =  data["Address"].apply(lambda x: clean_data.clean_neighborhood(x))
    data['City'] = data["Address"].apply(lambda x: clean_data.clean_city(x))

    # Strata
    data['Property Type'] = data["Property Info"].apply(lambda x: clean_data.clean_split_element(x, attribute = "Property Type"))
    data['Property Style'] = data["Property Info"].apply(lambda x: clean_data.clean_split_element(x, attribute = "Property Style"))
    data['Ownership of Interest'] = data["Property Info"].apply(lambda x: clean_data.clean_split_element(x, attribute = "Property Ownership"))
    data['Property Age'] = data["Property Info"].apply(lambda x: clean_data.clean_property_age(x))

    # Prices
    data['Sold Price'] = data['Sale Price'].apply(lambda x: clean_data.clean_split_element(x, attribute = "Street"))
    data['Ask Price'] = data["Sale Price"].apply(lambda x: clean_data.clean_prices(x, fee_type = 'Ask'))
    data['Original Price']  = data["Sale Price"].apply(lambda x: clean_data.clean_prices(x, fee_type = 'Original'))
    data['Maintenance Price'] = data["Sale Price"].apply(lambda x: clean_data.clean_prices(x, fee_type = 'Maint'))

    # Dates
    data['Temp Dates'] = data['Date'].str.split('\n')

    data['Reported Date'] = data["Temp Dates"].apply(lambda x: clean_data.find_reported_dt(x))
    data['Sold Date'] = data["Date"].apply(lambda x: clean_data.find_sold_dt(x))
    data['Days on Market'] = data["Date"].apply(lambda x: clean_data.find_days_on_market(x))

    # Size
    data['Bedrooms'] = data["Size"].apply(lambda x: clean_data.clean_bed_bath_sqft_size(x,'Bed'))
    data['Bathrooms'] = data["Size"].apply(lambda x: clean_data.clean_bed_bath_sqft_size(x, 'Bath'))
    data['Size (in sqft)'] = data["Size"].apply(lambda x: clean_data.clean_bed_bath_sqft_size(x, 'Room'))

    # Brokerage
    data["Listing Brokerage Name"] = data["Listing Brokerage"].apply(lambda x: clean_data.clean_split_element(x, "Listing Brokerage"))
    # data["Comission"] = data["Listing Brokerage"].apply(lambda x: clean_data.clean_comission(x))
    data['Buying Brokerage name'] = data['Buying Brokerage'].apply(lambda x: ','.join(set(x.split('\n'))))


    # In[113]:


    table_cols = ['MLS #', 'Street Address', 'Postal Code', 'Neighborhood', 'City',
                 'Property Type', 'Property Style', 'Property Age',
                 'Sold Price','Ask Price','Original Price','Maintenance Price',
                 'Bedrooms', 'Bathrooms', 'Size (in sqft)',
                 'Reported Date','Sold Date','Days on Market',
                 'Listing Brokerage Name','Buying Brokerage name']

    table = data[table_cols].copy(deep = True)


    # In[114]:


    # Cleaning extensively

    table['Sold Price ($)'] = table['Sold Price'].apply(lambda x: "".join(re.findall(r'\d+', x))).astype(int)
    table['Ask Price ($)'] = table['Ask Price'].apply(lambda x: "".join(re.findall(r'\d+', x))).astype(int)

    table['Maintenance Price'] = np.where(table['Maintenance Price'] == '', '0', table['Maintenance Price'])
    table['Maintenance Price ($)'] = table['Maintenance Price'].apply(lambda x: "".join(re.findall(r'\d+', x))).astype(int)

    table['Original Price'] = np.where(table['Original Price'] == '', table['Ask Price'], table['Original Price'])
    table['Original Price ($)'] = table['Original Price'].apply(lambda x: "".join(re.findall(r'\d+', x))).astype(int)


    # In[115]:


    table['Bedrooms #'] = table['Bedrooms'].apply(lambda x: "".join(re.findall(r'\d+', x))).astype(int)
    table['Bathrooms #'] = table['Bathrooms'].apply(lambda x: "".join(re.findall(r'\d+', x))).astype(int)
    table['Size (in sqft) #'] = table['Size (in sqft)'].apply(lambda x: "".join(re.findall(r'\d+', x))).astype(int)
    table['On Market (days)'] = table['Days on Market'].apply(lambda x: "".join(re.findall(r'\d+', x))).astype(int)

    # Property Aage
    table['Property Age (yrs)'] = table['Property Age'].str.replace('Newly Built','0')
    table['Property Age (yrs)'] = table['Property Age (yrs)'].str.replace('Vacant Lot','99')
    table['Property Age (yrs)'] = table['Property Age (yrs)'].astype(str)
    table['Property Age (yrs)'] = table['Property Age (yrs)'].apply(lambda x: "".join(re.findall(r'\d+', x)))


    # In[116]:


    # TODO: Add Ownership Interest, Price per sqft, Maintence fee per sq

    table['Price per sqft'] = round(table['Sold Price ($)'] / table['Size (in sqft) #'],2)
    table['Maint fee per sqft'] = round(table['Maintenance Price ($)'] / table['Size (in sqft) #'],2)


    # In[117]:


    final_columns = ['MLS #', 'Street Address', 'Postal Code', 'Neighborhood', 'City',
                 'Property Type', 'Property Style', 'Property Age',
                 'Sold Price ($)','Ask Price ($)','Original Price ($)','Maintenance Price ($)',
                 'Bedrooms #', 'Bathrooms #', 'Size (in sqft) #',
                 'Reported Date','Sold Date','On Market (days)',
                 'Listing Brokerage Name', 'Buying Brokerage name',
                 'Price per sqft','Maint fee per sqft']

    table_df = table[final_columns]


    # In[118]:


    table_df.to_csv('sample_data.csv')

    
    with open('scripts//connect_to_db.py') as infile:
        exec(infile.read())
    






