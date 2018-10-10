# coding: utf-8
"""Script for downloading all the GEM commodities data from the World Bank, always getting the 700 latest months"""

import requests
import pandas as pd
import json


def flatten_json(y):
    """Credit https://medium.com/@amirziai/flattening-json-objects-in-python-f5343c794b10"""
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out


def make_url(indicator, page=1):
    prefix = "http://api.worldbank.org/v2/countries/all/indicators/"
    suffix = "?format=json&page=" + str(page) + "&MRV=700" + "&frequency=M" 
    
    url = prefix + indicator + suffix
    #print("URL: ", url)
    
    return(url)

def response_to_df(response):
    data = response.json()[1]
    flat_data = [flatten_json(f) for f in data]
    df = pd.DataFrame(flat_data)
    return(df)

def cleanup_df(df):

    return(df)


metadata = pd.read_csv("GEM_metadata.csv")
indicators = list(metadata['Code'])
print(str(len(indicators)), "indicators to download")


dfs = []
for ind in indicators:
    url = make_url(indicator=ind)
    response = requests.get(url)
    if response.ok:
        j = response.json()
        pages = j[0]['pages']

        # if pages is 0 this never runs
        for page in range(1, pages+1):
            if page == 1:
                # we already have this
                df = response_to_df(response)
            else:
                url = make_url(indicator=ind, page=page)
                response = requests.get(url)
                df = df.append(response_to_df(response))
        
        if pages != 0:
            df.reset_index(inplace=True)
            df = df[['country_value', 'countryiso3code', 'date', 'indicator_id','value']]
            df.sort_values('date', inplace=True)    
            dfs.append(df)
            print("Got ", str(pages), "pages for ", ind)

        else:
            print("No pages for ", ind, "at ", url)
    else:
        print("Response wasn't OK")
        print("Offending URL: ", url)
        
print(str(len(dfs)), "indicators downloaded")


merged = pd.DataFrame()
for df in dfs:
    df = df.pivot(index='date', columns='indicator_id', values='value')
    merged = merged.join(df, how='outer')
    
merged.to_hdf("merged.hdf5", key='data')




