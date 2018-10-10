"""
Gets REIGN data from git repository and stages it on db. 
Currently restages full dataset with the latest month's release.
"""

import sys
sys.path.append("../..")
import urllib
import pandas as pd
import numpy as np
from views_utils import dbutils
from bs4 import BeautifulSoup

connectstring = dbutils.make_connectstring(prefix="postgresql", db="views",
                                           uname="VIEWSADMIN", hostname="VIEWSHOST",
                                           port="5432")

def getREIGN(schema="dataprep", 
             table="reign", 
             if_exists="replace"):

    """
    Fetches most recent full REIGN dataset.
    """
    #find current download link
    url = 'https://oefdatascience.github.io/REIGN.github.io/menu/reign_current.html'
    html_doc = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html_doc, 'lxml')
    container = soup.find("div", {"class": "post-container"})
    link = container.find("a", href=True)['href']
    print("downloading data from {}".format(link))

    #fetch
    reign = pd.read_csv(link)

    #drop irrelevant variables
    #reign.drop(['leader'], axis=1, inplace=True)

    #exponentiate variables that have been logged for some unapparent reason
    #not sure about the other floats
    reign['lastelection'] = round(np.exp(reign['lastelection']))
    reign['loss'] = round(np.exp(reign['loss']))
    reign['irregular'] = round(np.exp(reign['irregular']))
    
    #add transforms
    reign['tenure_log'] = np.log1p(reign.tenure_months)
    nomonths = reign['tenure_months'] == 0
    #reign['regimeduration_log'] = np.log(reign.regimeduration)
    print(reign[nomonths])
    print(reign.head())
    #push to db
    dbutils.df_to_db(connectstring, reign, schema, table, if_exists, write_index=True)


getREIGN()

# check duplicates, get zero val count dup
# exponentiate logs to int, 