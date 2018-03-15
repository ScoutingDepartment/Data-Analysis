"""
Reads csv files scanned from the QR scanner
"""

import pandas as pd

from processor.indexing import *

HEADERS = ["Match", "Team", "Name", "Start Time", "ID", "Data", "Comments"]

def read_csv_entries(file_name):
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

    for f in filtered_files("../data/scan", ".csv"):
        for entry in read_csv_entries(f):
            yield entry


def unique_entries():
    return set(read_all_csv())

#TODO reads and puts into database


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


print(generate_raw_database())
print(generate_raw_database().dtypes)
# TODO fix this so that the types are not object
