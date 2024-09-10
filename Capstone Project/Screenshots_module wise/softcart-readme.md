# SoftCart Data Platform Architecture

## Overview

This project implements the data platform architecture for SoftCart, an e-commerce company using a hybrid architecture with both on-premises and cloud databases. The architecture is designed to handle various aspects of data management, from transactional processing to big data analytics.

## Project Structure

The project is divided into 7 modules, each focusing on different aspects of the data platform:

- M1: [Module 1 description]
- M2: [Module 2 description]
- M3: [Module 3 description]
- M4: [Module 4 description]
- M5: [Module 5 description]
- M6: [Module 6 description]
- M7: [Module 7 description]

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

## Setup and Installation

[Include instructions for setting up the project environment, including any necessary software installations, configuration steps, etc.]

## Usage

[Provide instructions on how to run the project, including any commands or scripts to execute.]

## Contributing

[If applicable, include guidelines for contributing to the project.]

## License

[Specify the license under which this project is released.]

## Contact

[Provide contact information for project maintainers or support.]
