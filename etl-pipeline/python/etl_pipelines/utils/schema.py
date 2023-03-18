import ipaddress

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    email: str
    gender: str
    ip_address: str
    country_code: str = None
    batch_id: str = None


class CountryStats(SQLModel, table=True):
    __tablename__ = "country_stats"

    country_code: str = Field(default=None, primary_key=True)
    user_count: int
    batch_id: str = None
