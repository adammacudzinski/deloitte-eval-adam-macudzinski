import argparse
import json
import logging

from etl_pipelines.utils.db import SQLDatabaseManager
from etl_pipelines.utils.file import UserDataFileReader

log = logging.getLogger(__name__)


def run_etl_pipeline(excel_file_path: str, connection_url: str, batch_id: str):
    """
    Function to read a given Excel file and load the contents into a MYSQL Database

    :param excel_file_path:
    :param connection_url:
    :param batch_id:
    :return:
    """
    file_reader = UserDataFileReader(excel_file_path)
    users = file_reader.get_users()
    country_stats = file_reader.get_country_stats()

    db = SQLDatabaseManager(connection_url)
    db.setup_db()

    def insert_records(model_instances):
        table_name = model_instances[0].__tablename__
        model_class = model_instances[0].__class__

        log.info(f"Deleting existing batch from {table_name}")

        db.delete_batch(model_class, batch_id)

        log.info(f"Inserting: {len(model_instances)} records into table: {table_name}")

        for instance in model_instances:
            instance.batch_id = batch_id

        db.bulk_insert_records(model_instances)
        db.commit()

    insert_records(users)
    insert_records(country_stats)

    db.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--excel_file_path', required=True, help='Path to input Excel data file')
    parser.add_argument('--secrets_json_file', required=True, help='Path to JSON file generated by Terraform')
    parser.add_argument('--batch_id', required=True, help='ID to index batch of users')

    args = parser.parse_args()

    with open(args.secrets_json_file, "r") as secrets_file:
        json_dict = json.load(secrets_file)
        connection_url = json_dict["db_url_string"]["value"]

    run_etl_pipeline(args.excel_file_path, connection_url, args.batch_id)