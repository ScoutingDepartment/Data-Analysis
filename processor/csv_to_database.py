"""
Reads csv files scanned from the QR scanner
"""

import pandas as pd

from processor import indexing, database, validation, format_time, board


def write_unique(database_path, scan_folder_path, board_folder_path):
    """
    Writes entries into the database
    """

    find_board = board.get_finder(board_folder_path)

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

        for f in indexing.filtered_files(scan_folder_path, ".csv"):
            for entry in read_one_csv_file(f):
                if validation.check_encode(entry):
                    yield entry

    def get_entry_dict(entry):
        """
        Formats a string entry into a dictionary
        :param entry: The encoded string entry
        :return: Formatted dictionary
        """
        split = entry.split("_")

        return {"Match": int(split[0]),
                "Team": int(split[1]),
                "Name": split[2],
                "StartTime": format_time.display_time(int(split[3], 16)),
                "Board": find_board(int(split[4], 16)).name(),
                "Data": split[5],
                "Comments": split[6]
                }

    def get_entries_table():
        """
        Creates a table of unique entries
        :return: The pandas table of entries
        """
        return pd.DataFrame([get_entry_dict(e) for e in set(read_all_csv())],
                            columns=database.RAW_HEADER.keys())

    conn = database.get_engine(database_path).connect()

    get_entries_table().to_sql(name="RAW_ENTRIES",
                               con=conn,
                               if_exists="replace",  # replaces existing table
                               dtype=database.RAW_HEADER  # sets the column data types
                               )
    conn.close()

if __name__ == "__main__":
    write_unique("../data/database/data.warp7", "../data/scan", "../data/board")