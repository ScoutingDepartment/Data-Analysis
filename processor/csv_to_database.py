"""
Reads csv files scanned from the QR scanner
"""

import pandas as pd

from processor import indexing

HEADERS = ["Match", "Team", "Name", "StartTime", "Board", "Data", "Comments"]


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
            yield entry


def unique_entries():
    return set(read_all_csv())


# TODO reads and puts into database


def generate_raw_database():
    entries = unique_entries()
    dictionaries = []
    for entry in entries:
        entry = entry.split("_")
        d = {}
        for i, column in enumerate(HEADERS):
            d[column] = entry[i]
        dictionaries.append(d)
    db = pd.DataFrame(dictionaries, columns=HEADERS)
    return db


def get_entry_dict(entry):

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
    return pd.DataFrame([get_entry_dict(e) for e in unique_entries()], columns=HEADERS)

# TODO fix this so that the types are not object
# TODO Check for encode validation
