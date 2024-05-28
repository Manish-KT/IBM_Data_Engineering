import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import sqlite3
import logging

# Setup logging
logging.basicConfig(filename='etl_project_log.txt', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def scrape_gdp_data():
    url = "https://web.archive.org/web/20230902185326/https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", {"class": "wikitable"})
    table_rows = table.find("tbody").find_all("tr")[3:]
    
    df = {
        "Country": [],
        "Region": [],
        "IMF Estimate": [],
        "Year": []
    }

    for row in table_rows:
        row_data = row.find_all("td")
        df["Country"].append(row_data[0].text.strip())
        df["Region"].append(row_data[1].text.strip())
        if row_data[2].text.strip() == "—":
            df["IMF Estimate"].append(None)
            df["Year"].append(None)
        else:
            df["IMF Estimate"].append(int(row_data[2].text.strip().replace(",", "")))
            df["Year"].append(int(row_data[3].text.strip()[-4:]))

    return df

def transform_data(df):
    df = pd.DataFrame(df)
    df.rename(columns={"IMF Estimate": "GDP (billion USDs)"}, inplace=True)
    
    def millions_to_billions(value):
        return round(value / 1000, 2) if value else None

    df["GDP (billion USDs)"] = df["GDP (billion USDs)"].apply(millions_to_billions)
    df["Year"] = df["Year"].astype("Int32")
    return df

def save_to_json(df, filename):
    df.to_json(filename, orient="records", indent=4)

def save_to_db(df, db_name, table_name):
    conn = sqlite3.connect(db_name)
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    conn.close()

def query_db(db_name, query):
    conn = sqlite3.connect(db_name)
    result = pd.read_sql_query(query, conn)
    conn.close()
    return result

def main():
    logging.info("Starting the ETL process")

    try:
        logging.info("Scraping data")
        raw_data = scrape_gdp_data()
        logging.info("Scraping data completed")

        logging.info("Transforming data")
        transformed_data = transform_data(raw_data)
        logging.info("Data transformation completed")

        json_filename = 'Countries_by_GDP.json'
        logging.info(f"Saving data to JSON file: {json_filename}")
        save_to_json(transformed_data, json_filename)
        logging.info(f"Data saved to JSON file: {json_filename}")

        db_name = 'World_Economies.db'
        table_name = 'Countries_by_GDP'
        logging.info(f"Saving data to database: {db_name}, table: {table_name}")
        save_to_db(transformed_data, db_name, table_name)
        logging.info(f"Data saved to database: {db_name}, table: {table_name}")

        query = "SELECT * FROM Countries_by_GDP WHERE `GDP (billion USDs)` > 100"
        logging.info("Querying database for economies with more than 100 billion USD GDP")
        result = query_db(db_name, query)
        logging.info("Query executed successfully")
        logging.info(f"Query result:\n{result}")

    except Exception as e:
        logging.error(f"Error occurred: {e}")
        raise

    logging.info("ETL process completed")

if __name__ == "__main__":
    main()
