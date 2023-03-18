from sqlmodel import create_engine, SQLModel, Session


class SQLDatabaseManager:
    """
    ORM wrapper class for interfacing with SQL Databases
    """
    def __init__(self, connection_url: str):
        self.engine = create_engine(connection_url)
        self.session = Session(self.engine)

    def setup_db(self):
        """
        Automatically create all of the db tables currently declared as SQLModels
        :return:
        """
        SQLModel.metadata.create_all(self.engine)

    def delete_batch(self, model_class, batch_id):
        delete_q = model_class.__table__.delete().where(model_class.batch_id == batch_id)

        self.session.execute(delete_q)
        self.commit()

    def insert_record(self, record):
        """
        Insert a single model instance into a given table
        :param record:
        :return:
        """
        self.session.add(record)

    def bulk_insert_records(self, records):
        """
        Insert a collection of records at once

        :param records:
        :return:
        """
        self.session.bulk_save_objects(records)

    def commit(self):
        """
        Commit current db session
        :return:
        """
        self.session.commit()

    def close(self):
        """
        Close current db session
        :return:
        """
        self.session.close()
