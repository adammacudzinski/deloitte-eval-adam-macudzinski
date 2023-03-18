# ETL Pipeline Exercise

## High-level Summary

The key objective of this exercise was to build an ETL pipeline that
extracted generic user dimensional data from an Excel spreadsheet 
file (provided upfront), applied a transormation, and then loaded
the data into a database of my choice. 

**Database Selection**: Ultimately, given the relational nature of 
the input data, I decided to for with: MYSQL, a tried and true 
SQL database which I've had a lot of success with both for 
production systems as well as analytical data warehouses. 

**Data Transformation**: Since **ip_address** is a field included
in the input data, I thought that generating an aggregate view of 
the number of users for each country would be an interesting 
result, so I decided to run the IPs through a geo location lookup
API and then group the users by country code. 

**Ingest Model**: In order to prevent duplicates, I decided to use 
an external batch_id to index all of the user records. As a result, this
pipeline shoudl very easily be able to be incorporated into an automated
ETL platform ala Airflow.

## Key System Components

- **Terraform**: IaC tool to provision the MYSQL database as an AWS 
    RDS instance.

- **MYSQL Database**: Destination database of the ETL. Provisioned
    as an AWS RDS

- **Poetry**: Python package management tool used to manage the 
    pipeline env. 

- **SQLModel**: Powerful Python ORM library which merges the
    functionality of SQLAlchemy and Pydantic (schema enforcement)

- **Pandas**: Python data wranging library used for data processing

## Important Scripts

### Environment Setup

[run_terraform_depoyment.sh](infra//run_terraform_deployment.sh)

This script provisions all of the necessary resources in AWS using 
Terraform. 

`infra/run_terraform_depoyment.sh <Path_to_TF_input_vars> 
    <Path_to_output_TF_secrets`

### Deploy Env and Run ETL
[deploy_db_and_run_etl.sh](deploy_db_and_run_etl.sh)
This script calls the environment setup script first then runs the ETL 
pipeline. 

`deploy_db_and_run_etl.sh <Path_to_TF_input_vars> 
    <Path_to_output_TF_secrets <Path_to_input_Excel_file>`



