"""
Manages the databases used for storing data
"""

import sqlalchemy
from sqlalchemy import types as sql_types

RAW_HEADER = {
    "Match": sql_types.Integer,
    "Team": sql_types.Integer,
    "Name": sql_types.String,
    "StartTime": sql_types.String,
    "Board": sql_types.Integer,
    "Data": sql_types.String,
    "Comments": sql_types.String
}

EDITED_HEADER = {
    "Match": sql_types.Integer,
    "Team": sql_types.Integer,
    "Name": sql_types.String,
    "StartTime": sql_types.String,
    "Board": sql_types.Integer,
    "Data": sql_types.String,
    "Comments": sql_types.String,

    "RawIndex": sql_types.Integer,
    "Edited": sql_types.Integer
}


def get_connection(file):
    return sqlalchemy.create_engine(get_sqlite_uri(file)).connect()


def get_sqlite_uri(file):
    return "sqlite:///" + file
