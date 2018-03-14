"""
Reads csv files scanned from the QR scanner
"""

from processor.indexing import *


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

    for f in filtered_files("data/scan", "csv"):
        for entry in read_csv_entries(f):
            yield entry

#TODO reads and puts into database
