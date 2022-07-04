import pandas as pd
import numpy as np
import re

def clean_transform_df(dataframe):
    """
    Result of the scraped data is in one long series. The data needs to be transformed into a clean dataframe
    """
    df = dataframe[dataframe[0]!= ''].reset_index(drop = True)
    df['Index'] = np.divmod(np.arange(len(df)),9)[0]+1  # For every 9 rows same index, using index to group data in following step
    
    df.columns = ['temp_data','Index']
    
    df = (df.groupby('Index', as_index=False)
                  .agg({'temp_data': lambda x: x.dropna().tolist()})
    )
    
    columns_of_interest = ['Filler','MLS #','Address','Property Info',
                           'Size','Sale Price','Date','Listing Brokerage','Buying Brokerage']
    
    outcome_result = pd.DataFrame(df.temp_data.tolist())
    outcome_result.columns = columns_of_interest
    
    return outcome_result



def clean_split_element(text, attribute):
    """
    Params:
    - text --> String
    - attribute --> field of attribute to clean
        - Street [0]
        - Property Type [0]
        - Propety Style [1]
        - Property Ownership [1]
        - Brokerage Listing [0]
        - Sale Price [0]
        
    """
    
    index_0 = ["Street", "Property Type", "Listing Brokerage", "Sale Price"]
    index_1 = ["Property Style", "Property Ownership"]
    
    
    if attribute in index_0:
        string = text.split('\n')[0]
    
    elif attribute in index_1:
        string = text.split('\n')[1]
       
    
    return string
     
    
def clean_postal_code(text):
    """
    Clean and retrieve postal name
    
    Params: text --> Address
    """
    postal_code = re.compile(r'[A-Z]\d[A-Z]\s\d[A-Z]\d')
    
    try:
        p_code = postal_code.search(text.split('\n')[-2]).group()
        
    except:
        p_code = None
        
    return p_code


def clean_neighborhood(text):
    """
    Clean and retrieve neighborhood
    
    Params: text --> Address
    """    
    try:
        search_neigh = re.search('\(.*?\)', text)
        neigh = search_neigh.group(0)
        neigh = neigh.strip('()')

    except:
        neigh = None
        
    return neigh    
    
    
    
def clean_city(text):
    """
    Clean city and add a column
    
    """
    
    # Check to see if string contains any of the cities
    cities_keys = ['West Vancouver', 'North Vancouver','Vancouver','Richmond', 'Burnaby', 'New Westminster','Port Moody', 
                   'Anmore', 'Belcarra','Port Coquitlam','Coquitlam','Pitt Meadows', 'Maple Ridge', 'Delta', 'Tsawwassen', 
                  'Surrey','White Rock', 'Langley']

    mystring = " BC"
    cities_keys = [s + mystring for s in cities_keys]

    cities_values = cities_keys
    dict_cities = dict(zip(cities_keys, cities_values))
               
    try:
        city = None
        for substr in text.split('\n'):
            if substr in dict_cities.keys():
                city = dict_cities[substr]
                city = city[:-3]
         

    except:
        city = None      
    
        
    return city
    

def clean_property_age(text):
    """
    Clean and retrieve property age
    
    Params: text --> Property Info
    """
    
    try:
        age_str = re.search('\d+ years? old', text).group(0)
    except:    
        try:
            age_str = re.search('Newly Built', text).group(0)
        except:
            age_str = None

    
    return age_str
    
    
    
def clean_prices(text, fee_type):
    """
    Clean and retrieve price
    Params: Fee Type
        - Ask
        - Orig
        - Maint
        
    """
    
    if fee_type == "Ask":
        pattern = re.compile(r'\n(ask)\s+\$\d{1,3}(?:,\d{3})*', re.DOTALL)
    elif fee_type == "Original":
        pattern = re.compile(r'\n(orig)\s+\$\d{1,3}(?:,\d{3})*', re.DOTALL)
    elif fee_type == "Maint":
        pattern = re.compile(r'\nMaint.\s+fee\s+\$\d{1,3}(?:.\d{2})*', re.DOTALL)
    
    try:
        price = pattern.search(text).group()
        price = price.split('\n')[1]
        
    except:
        price = ''
        
    return price
    
        
def find_between_tags(lst, start_tag, end_tag):
    start_index = lst.index(start_tag)
    end_index = lst.index(end_tag, start_index)
    return lst[start_index + 1: end_index]    
    
def find_reported_dt(text_dt):
    return find_between_tags(text_dt, "Sale Reported", "Sale Date")[0]


def find_sold_dt(text_dt):
    
    sold_dt1 = re.compile(r'Sale Date\s+[\w\W]+', re.DOTALL)
    result_1 = sold_dt1.search(text_dt).group()

    sold_dt2 = re.compile(r'\n(.*)\n',re.DOTALL)
    result_2 = sold_dt2.search(result_1).group()
    sold_dt_result = result_2.replace('\n','').strip()    
    
    return sold_dt_result
    
    
def find_days_on_market(text_dt):
    
    return re.search('\(.*?\)', text_dt).group()
    
    
def clean_bed_bath_sqft_size(text, size_type):
    """
    Clean and retrieve size
    Params: Type
        - Bed
        - Bath
        - Room (in sqft)
        
    """
    
    DEFAULT_ANS = "99" # This is a dummy value
    
    if size_type == "Bed":
        pattern = re.compile(r'\b\d{1,3}(?:,\d{3})*(?:\.\d+)?(?!\d) bed',re.DOTALL)
    elif size_type == "Bath":
        pattern = re.compile(r'\b\d{1,3}(?:,\d{3})*(?:\.\d+)?(?!\d) bath',re.DOTALL)
    elif size_type == "Room":
        pattern = re.compile(r'\b\d{1,3}(?:,\d{3})*(?:\.\d+)?(?!\d) sqft',re.DOTALL)
    
    try:
        size = pattern.search(text).group()
        
    except:
        size = DEFAULT_ANS
        
    return size    
    
    
    
    
    
    
    
    
    
    