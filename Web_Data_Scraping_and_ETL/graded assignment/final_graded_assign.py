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
    table = soup.find("table", {"style": "border-collapse: collapse;"})
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
    df.rename(columns={"Market Cap": "Market Cap (billion USDs)"}, inplace=True)
    df["Rank & Bank"] = df["Rank & Bank"].apply(lambda x: " ".join(x.split(" ")[1:]))
    df["Market Cap (billion USDs)"] = df["Market Cap (billion USDs)"].apply(lambda x: float(x.replace("B", "").replace("$", "")))
    df["Market Cap (billion USDs)"] = df["Market Cap (billion USDs)"].apply(lambda x: round(x, 2))
    
    logging.info("Table data extraction completed.")
    return df

def convert_to_other_currencies(df, exchange_rates):
    logging.info("Converting market capitalization to other currencies...")
    exchanges = ["GBP", "EUR", "INR"]
    
    for i in exchanges:
        col_name = f"Market Cap (billion {i}s)"
        df[col_name] = df["Market Cap (billion USDs)"].apply(lambda x: round(x * exchange_rates[i], 2))
        
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
    conn.close()
    logging.info("SQL query execution completed.")
    return result

def main():
    # URL for extracting data
    url = "https://www.forbesindia.com/article/explainers/the-10-largest-banks-in-the-world/86967/1"
    logging.info(f"Initializing data extraction from URL: {url}...")

    # Fetching currency exchange rates from API
    exchange_api_url = "https://open.er-api.com/v6/latest/USD"
    logging.info(f"Fetching currency exchange rates from API: {exchange_api_url}...")
    response = requests.get(exchange_api_url)
    exchange_rates = response.json()["rates"]
    logging.info("Currency exchange rates fetched.")

    # Extracting and transforming data
    df = extract_table_data(url)
    df = convert_to_other_currencies(df, exchange_rates)

    # Saving to CSV
    save_to_csv(df, "bank_data.csv")

    # Loading to SQL database
    load_to_sql(df, "bank_data.db", "bank_data")

    # Running queries
    query_london = "SELECT `Rank & Bank`, `Market Cap (billion GBPs)` FROM bank_data WHERE `Headquarters` LIKE '%London%';"
    query_beijing = "SELECT `Rank & Bank`, `Market Cap (billion EURs)` FROM bank_data WHERE `Headquarters` LIKE '%Beijing%';"
    query_mumbai = "SELECT `Rank & Bank`, `Market Cap (billion INRs)` FROM bank_data WHERE `Headquarters` LIKE '%Mumbai%';"

    result_london = run_query("bank_data.db", query_london)
    result_berlin = run_query("bank_data.db", query_beijing)
    result_delhi = run_query("bank_data.db", query_mumbai)

    logging.info("Results of SQL queries:")
    logging.info(f"London: {result_london}")
    logging.info(f"Berlin: {result_berlin}")
    logging.info(f"Delhi: {result_delhi}")


    # Log progress
    logging.info("Data extraction and processing completed.")

if __name__ == "__main__":
    main()
