"""
Manages the databases used for storing data
"""

import sqlalchemy


def get_connection(file):
    return sqlalchemy.create_engine(get_sqlite_uri(file)).connect()


def get_sqlite_uri(file):
    return "sqlite:///" + file