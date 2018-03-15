"""
Manages the databases used for storing data
"""

import sqlalchemy


def get_connection():
    return sqlalchemy.create_engine("sqlite:///data/database/data.warp7").connect()
