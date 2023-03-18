import pandas as pd
import requests

from etl_pipelines.utils.schema import User, CountryStats


class UserDataFileReader:
    """
    File Reader class to read data from a local Excel file which conforms to the etl_pipelines.utils.schema.User
    schema
    """
    ip_lookup_url = "https://geolocation-db.com/json"

    def __init__(self, file_path: str):
        self.df = pd.read_excel(file_path)

        self._set_country_code()

    @staticmethod
    def _get_country_code(ip_address):
        """
        Return country code string for a given ip_address by looking up API
        :param ip_address:
        :return:
        """
        try:
            location_dict = requests.get(
                f"{UserDataFileReader.ip_lookup_url}/{ip_address}&position=true"
            ).json()
            country_code = location_dict["country_code"]

        except:
            country_code = None
        return country_code

    def _set_country_code(self):
        self.df['country_code'] = self.df["ip_address"].apply(self._get_country_code)

    def get_users(self):
        """
        Get list of User objects from given Excel file
        :return:
        """
        records = self.df.to_dict('records')
        users = [User(**record) for record in records]
        return users

    def get_country_stats(self):
        """
        Get list of CountryStats objects from a given Excel file
        :return:
        """
        stats_df = self.df.groupby('country_code').size()
        return [CountryStats(country_code=u, user_count=v) for (u, v) in stats_df.iteritems()]


