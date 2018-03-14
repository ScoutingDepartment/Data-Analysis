"""
Manages the databases used for storing data
"""

import sqlite3

def get_connection():
    return sqlite3.connect("data/database/data.warp7")