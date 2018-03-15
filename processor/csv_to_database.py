"""
Reads csv files scanned from the QR scanner
"""

import pandas as pd
from sqlalchemy import types as sql_types

from processor import indexing, database, validation

HEADER = {"Match": sql_types.Integer,
          "Team": sql_types.Integer,
          "Name": sql_types.String,
          "StartTime": sql_types.Integer,
          "Board": sql_types.Integer,
          "Data": sql_types.String,
          "Comments": sql_types.String
          }


def read_one_csv_file(file_name):
    """
    Creates a generator that contains match entries read from a csv file
    :param file_name:
    :return:
    """

    read_file = open(file_name, "r")
    entries = read_file.readlines()
    read_file.close()

    for entry in entries:
        yield "".join(entry.split(",")[:-1])


def read_all_csv():
    """
    Reads all CSV entries in the folder
    :return: returns entries
    """

    for f in indexing.filtered_files("data/scan", ".csv"):
        for entry in read_one_csv_file(f):
            if validation.check_encode(entry):
                yield entry


def unique_entries():
    """
    Removes duplicate entries
    :return: A set of unique entries
    """

    return set(read_all_csv())


def get_entry_dict(entry):
    """
    Formats a string entry into a dictionary
    :param entry: The encoded string entry
    :return: Formatted dictionary
    """
    split = entry.split("_")

    return {"Match": split[0],
            "Team": int(split[1]),
            "Name": split[2],
            "StartTime": int(split[3], 16),
            "Board": int(split[4], 16),
            "Data": split[5],
            "Comments": split[6]
            }


def get_entries_table():
    """
    Creates a table of unique entries
    :return: The pandas table of entries
    """
    return pd.DataFrame([get_entry_dict(e) for e in unique_entries()], columns=HEADER.keys())


def write_to_database():
    """
    Writes entries into the database
    """
    conn = database.get_connection()

    get_entries_table().to_sql(name="RAW_ENTRIES",
                               con=conn,
                               if_exists="replace",  # replaces existing table
                               dtype=HEADER  # sets the column data types
                               )
    conn.close()
