#Script for downloading latest World Development Indicators, reshaping them to a proper panel and merging in gwno codes
#converted to .py with the command below
#jupyter nbconvert --to python getwdi.ipynb
import requests
import pandas as pd
import os
import zipfile
import sys

fname_data = "WDIData.csv"
fname_series = "WDISeries.csv"
fname_data_out_csv = "wdi_data_reshaped.csv"
fname_data_out_dta = "wdi_data_reshaped.dta"
fname_gwno = 'wdi-gwno.csv'
dir_temp = "./temp/"
dir_output = "./output"
url = "http://databank.worldbank.org/data/download/WDI_csv.zip"
filename = "./temp/WDI_csv.zip"


for d in [dir_temp, dir_output]:
    if not os.path.isdir(d):
        print(f"Creating {d}")
        os.makedirs(d)

print(f"Fetching {url} to {filename}.")
r = requests.get(url, stream=True)
chunk_size=1024*512
with open(filename, 'wb') as fd:
    for chunk in r.iter_content(chunk_size):
        print(".", end="", flush=True)
        fd.write(chunk)
print("Done fetching.")

print(f"Extracting {filename} to {dir_temp}")
files = ["WDIData.csv", "WDISeries.csv"]
with zipfile.ZipFile(filename, 'r') as z:
    print(filename, "contains:")
    z.printdir()
    for file in files:
        z.extract(file, path=dir_temp)

path = os.path.join(dir_temp, fname_data)
print(f"Reading {path}")
df = pd.read_csv(path, encoding = "ISO-8859-1")

print("Reshaping")
df.rename(columns={'Country Code': 'CountryCode',
    'Indicator Code' : 'IndicatorCode',
    'Country Name' : 'CountryName',
    'Indicator Name' : "IndicatorName"}, inplace=True)

df.drop(['CountryName', 'IndicatorName'], axis=1, inplace=True)
df = df.set_index(['CountryCode','IndicatorCode'])
df.columns.name = 'year'
df = df.stack().unstack('IndicatorCode')
df = df.reset_index()

print(f"Reading {fname_gwno}")
df_gwno = pd.read_csv(fname_gwno)
df = df.merge(df_gwno, how='outer', on='CountryCode')

# Make columns stata-compliant
print("Renaming cols")
for c in df.columns:
    df.rename(columns={c : c.replace(".", "_")}, inplace=True)


path = os.path.join(dir_output, fname_data_out_csv)
print(f"writing {path}", flush=True)
df.to_csv(path, index=False)

path = os.path.join(dir_output, fname_data_out_dta)
print(f"writing {path}", flush=True)
df.to_stata(path, write_index=False)

print("Done")


