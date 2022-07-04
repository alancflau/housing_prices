#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import sqlite3

import logging


# In[3]:


# data = pd.read_csv("sample_data.csv", index_col =[0])


# In[ ]:


logging.getLogger().setLevel(logging.INFO)

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn    


def create_table(conn):
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS SoldHouses(
            MLS text,
            StreetAddress text,
            PostalCode text,
            Neighborhood text,
            City text,
            PropertyType text,
            PropertyStyle text,
            PropertyAge int,
            SoldPrice int,
            AskPrice int,
            OrigPrice int,
            MaintPrice int,
            Beds int,
            Baths int,
            Size int,
            ReportedDate date,
            SoldDate date,
            OnMarket int,
            ListingBrokerageName text,
            BuyingBrokerageName text,
            PricePerSqft float,
            MaintFeePerSqft float)

    """) 
    
def push_to_db(data):
    
    data.columns = ['MLS', 'StreetAddress','PostalCode','Neighborhood','City','PropertyType','PropertyStyle',
                    'PropertyAge','SoldPrice','AskPrice','OrigPrice','MaintPrice','Beds','Baths','Size',
                    'ReportedDate','SoldDate','OnMarket','ListingBrokerageName','BuyingBrokerageName',
                    'PricePerSqft','MaintFeePerSqft']   

    data.to_sql("SoldHouses", conn, if_exists = 'append', index = False)
    
def close_connection():
    conn.close()


# In[ ]:


if __name__ == '__main__':
    data = pd.read_csv('sample_data.csv', index_col = [0]) # Find a better way to read the data
    conn = create_connection('real_estate.db')
    create_table(conn)
    push_to_db(data)
    close_connection()
    logging.info("Data Insert Complete")
    


# In[40]:


# conn = sqlite3.connect('real_estate.db')

# c = conn.cursor()

# c.execute("""
# CREATE TABLE IF NOT EXISTS SoldHouses(
#         MLS text,
#         StreetAddress text,
#         PostalCode text,
#         Neighborhood text,
#         City text,
#         PropertyType text,
#         PropertyStyle text,
#         PropertyAge int,
#         SoldPrice int,
#         AskPrice int,
#         OrigPrice int,
#         MaintPrice int,
#         Beds int,
#         Baths int,
#         Size int,
#         ReportedDate date,
#         SoldDate date,
#         OnMarket int,
#         ListingBrokerageName text,
#         BuyingBrokerageName text,
#         PricePerSqft float,
#         MaintFeePerSqft float)

# """)


# In[41]:


# data.columns = ['MLS', 'StreetAddress','PostalCode','Neighborhood','City','PropertyType','PropertyStyle',
#                 'PropertyAge','SoldPrice','AskPrice','OrigPrice','MaintPrice','Beds','Baths','Size',
#                 'ReportedDate','SoldDate','OnMarket','ListingBrokerageName','BuyingBrokerageName',
#                 'PricePerSqft','MaintFeePerSqft']


# In[42]:


# data.to_sql("SoldHouses", conn, if_exists = 'append', index = False)


# In[ ]:





# In[43]:


# conn = sqlite3.connect('real_estate.db')
# test_df = pd.read_sql_query("SELECT * FROM SoldHouses", conn)

