# SoftCart Data Platform Architecture

## Overview

This project implements the data platform architecture for SoftCart, an e-commerce company using a hybrid architecture with both on-premises and cloud databases. The architecture is designed to handle various aspects of data management, from transactional processing to big data analytics.

## Project Structure

The project is divided into 7 modules, each focusing on different aspects of the data platform:

- M1: OLTP Database Requirements and Design
- M2: Querying Data in NoSQL Databases
- M3: Data Warehouse Design & Setup & Reporting
- M4: Data Analytics with Cognos and Looker Studio
- M5: ETL 
- M6: Data pipeline using Apache Airflow
- M7: Big data with Spark

Screenshots for each module's tasks are saved in corresponding folders (M1, M2, ..., M7).

## Technologies Used

- OLTP Database: MySQL
- NoSQL Database: MongoDB
- Production Data Warehouse: DB2 on Cloud
- Staging Data Warehouse: PostgreSQL
- Big Data Platform: Hadoop
- Big Data Analytics: Spark
- Business Intelligence Dashboard: IBM Cognos Analytics
- Data Pipelines: Apache Airflow

## Architecture Overview

1. **Web Presence**: SoftCart's website is accessible via various devices (laptops, mobiles, tablets).
2. **Data Storage**:
   - Product catalog data is stored in MongoDB.
   - Transactional data (inventory, sales) is stored in MySQL.
3. **Data Warehousing**:
   - Data is periodically extracted from MongoDB and MySQL into a staging warehouse (PostgreSQL).
   - The production data warehouse runs on IBM DB2 (cloud instance).
4. **Business Intelligence**:
   - BI teams connect to IBM DB2 for operational dashboard creation.
   - IBM Cognos Analytics is used for dashboard creation.
5. **Big Data Analytics**:
   - All data is collected in a Hadoop cluster for analytics purposes.
   - Spark is used for data analysis on the Hadoop cluster.
6. **Data Movement**:
   - ETL pipelines running on Apache Airflow move data between OLTP, NoSQL, and data warehouse systems.


## Usage

These screenshorts can be used as a refrence for project completion and idea derivation.

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.

## Contact
This project was created by Manish Kumar Tailor. For more projects and information, visit my portfolio at [Portfolio](https://manish-kt.github.io/portfolio-website/).
