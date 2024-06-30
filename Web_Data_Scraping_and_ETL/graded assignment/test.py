import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
import logging


data = requests.get("https://web.archive.org/web/20230908091635/https://en.wikipedia.org/wiki/List_of_largest_banks").text

soup = BeautifulSoup(data, 'html.parser')

table = soup.find("table", {"class": "wikitable"})
table_rows = table.find("tbody").find_all("tr")

table_head = [i.text for i in table.find_all("th")]
df = {key: [] for key in table_head}

for row in table_rows[1:]:
    row_data = row.find_all("td")
    try:
        for i, key in enumerate(table_head, start=0):
            df[key].append(row_data[i].text)
    except Exception as e:
        continue
        
df = pd.DataFrame(df)

print(df.head())