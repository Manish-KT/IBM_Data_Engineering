import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
import logging

# Setting up logging
logging.basicConfig(filename='data_processing.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_table_data(url):
    logging.info("Extracting table data from URL...")
    data = requests.get(url).text
    soup = BeautifulSoup(data, "html.parser")
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
            logging.error(f"Error occurred while extracting table data: {e}")
            continue
            
    df = pd.DataFrame(df)
    # convert column to float
    df[table_head[-1]] = df[table_head[-1]].astype(float)
    # rename column
    df.rename(columns={table_head[-1]: "Market_Cap_billion_USDs)"}, inplace=True) 
    df.rename(columns={table_head[1]: "Name"}, inplace=True)
    logging.info("Table data extraction completed.")

    return df

def convert_to_other_currencies(df, exchange_rates):
    logging.info("Converting market capitalization to other currencies...")
    exchanges = ["GBP", "EUR", "INR"]
    
    for i in exchanges:
        col_name = f"Market_Cap_billion_{i}s"
        df[col_name] = df[df.columns[-1]].apply(lambda x: round(x * exchange_rates[i], 2))
        
    logging.info("Currency conversion completed.")
    return df

def save_to_csv(df, filename):
    logging.info(f"Saving data to CSV file: {filename}...")
    df.to_csv(filename, index=False)
    logging.info("Data saved to CSV file.")

def load_to_sql(df, db_filename, table_name):
    logging.info(f"Loading data to SQL database: {db_filename}, table: {table_name}...")
    conn = sqlite3.connect(db_filename)
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    conn.close()
    logging.info("Data loaded to SQL database.")

def run_query(db_filename, query):
    logging.info(f"Running SQL query: {query}...")
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    result = pd.DataFrame(result)
    conn.close()
    logging.info("SQL query execution completed.")
    return result

def main():
    # URL for extracting data
    url = "https://web.archive.org/web/20230908091635/https://en.wikipedia.org/wiki/List_of_largest_banks"
    logging.info(f"Initializing data extraction from URL: {url}...")

    # Fetching currency exchange rates from CSV file
    exchange_rates = pd.read_csv("exchange_rate.csv")
    exchange_rates = dict(zip(exchange_rates["Currency"], exchange_rates["Rate"]))
    logging.info("Currency exchange rates fetched.")

    # Extracting and transforming data
    df = extract_table_data(url)
    df = convert_to_other_currencies(df, exchange_rates)

    # Saving to CSV
    save_to_csv(df, "bank_data.csv")

    # Loading to SQL database
    load_to_sql(df, "bank_data.db", "bank_data")

    print("query: SELECT * FROM bank_data")
    q1 = run_query("bank_data.db", "SELECT * FROM bank_data")
    print("query: SELECT AVG(Market_Cap_billion_GBPs) FROM bank_data")
    q2 = run_query("bank_data.db", "SELECT AVG(Market_Cap_billion_GBPs) FROM bank_data")
    print("query: SELECT Name FROM bank_data LIMIT 5")
    q3 = run_query("bank_data.db", "SELECT Name FROM bank_data LIMIT 5")

    logging.info("Results of SQL queries:")
    logging.info(f"query1: {q1}")
    logging.info(f"query2: {q2}")
    logging.info(f"query3: {q3}")


    # Log progress
    logging.info("Data extraction and processing completed.")

if __name__ == "__main__":
    main()
