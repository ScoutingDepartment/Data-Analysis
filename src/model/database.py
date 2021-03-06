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
    "Board": sql_types.String,
    "Data": sql_types.String,
    "Comments": sql_types.String
}

EDITED_HEADER = {
    "RawIndex": sql_types.Integer,
    "Edited": sql_types.String,
    "Match": sql_types.Integer,
    "Team": sql_types.Integer,
    "Name": sql_types.String,
    "StartTime": sql_types.String,
    "Board": sql_types.String,
    "Data": sql_types.String,
    "Comments": sql_types.String,
}


def get_engine(file):
    return sqlalchemy.create_engine(get_sqlite_uri(file))


def get_sqlite_uri(file):
    return "sqlite:///" + file
