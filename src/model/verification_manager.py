import time
from os import walk, path
from re import compile

import numpy as np
import pandas as pd

from src.model import database, format_time, boards

FILTER_HEADER = ['Match', 'Team', 'Name', "Board", "Edited"]
FILTER_SORT = ['Match', 'Team']


class VerificationManager:
    """Data model manager for verifying scouting entries"""

    def __init__(self, db_path, csv_dir_path, board_dir_path):
        """
        Initializes the manager by providing file paths required \
        to manage the process of verification.
        This method does not actually load any data because the
        intention at this point may not be clear
        :param db_path: path to the database file (.warp7)
        :param csv_dir_path: path to the directory of the scanned data
        :param board_dir_path: path to the direction containing boards
        """
        self.db_path = db_path
        self.csv_dir_path = csv_dir_path
        self.board_dir_path = board_dir_path

        self.board_finder = boards.Finder(board_dir_path)

        if path.exists(db_path):
            conn = database.get_engine(db_path).connect()
            self.raw_entries = pd.read_sql(sql="SELECT * FROM RAW_ENTRIES",
                                           con=conn,
                                           index_col="index")

            self.edited_entries = pd.read_sql(sql="SELECT * FROM EDITED_ENTRIES",
                                              con=conn,
                                              index_col="index")
            conn.close()
        else:
            self.raw_entries = pd.DataFrame()
            self.edited_entries = pd.DataFrame()
            self.update()
            self.save()

    def __getitem__(self, index):
        """
        Get data for one specific entry based on the index
        :param index: the index to lookup
        :return: The entry info, or empty dict if row does not exist
        """

        if index in self.edited_entries.index:
            # TODO get newer entry object
            # TODO get both raw and edited
            row = self.edited_entries.iloc[index]
            entry_board = self.board_finder.get_board_by_name(row["Board"])
            entry_info = {k: row[k] for k in ["Match", "Team", "Name", "StartTime", "Comments"]}
            entry_info["Board"] = entry_board.name()
            entry_info["Data"] = []
            return entry_info

        raise IndexError()

    def __setitem__(self, index, value):
        """
        Sets a modified entry object into the manager
        :param index: the index to lookup
        :param value: the entry object to set
        """
        if index in self.edited_entries.index:
            # TODO set using newer entry object
            return

        raise IndexError()

    def update(self):
        """
        Updates the two tables with new data saved in the csv dir path
        Directly replaces the raw data table
        Attempts to merge the raw data into the edited data
        :return: The number of new items imported
        """

        def list_files():
            """Search for CSV files"""
            for root, _, files in walk(self.csv_dir_path):
                for f in files:
                    if f.split(".")[-1].lower() == "csv":
                        yield path.join(root, f)

        def read_one(f_path):
            """Read the contents of one CSV file"""
            read_file = open(f_path, "r")
            entries = read_file.readlines()
            read_file.close()
            for entry in entries:
                yield "".join(entry.split(",")[:-1])

        def read_all():
            """Read all found files and yield entries that pass the format test"""
            matcher = compile("\d{1,3}_\d{1,4}_[^_]+_[0-9a-f]{8}_[0-9a-f]{8}_([0-9a-f]{4})*_.*")
            for f in list_files():
                for entry in read_one(f):
                    if matcher.match(entry) is not None:
                        yield entry

        def make_columns(entry):
            """Make the columns to put in the database"""
            split = entry.split("_")
            return {"Match": int(split[0]),
                    "Team": int(split[1]),
                    "Name": split[2],
                    "StartTime": format_time.display_time(int(split[3], 16)),
                    "Board": self.board_finder.get_board_by_id(int(split[4], 16)).name(),
                    "Data": split[5],
                    "Comments": split[6]
                    }

        # Create the DataFrame from list of unique entries
        self.raw_entries = pd.DataFrame([make_columns(entry) for entry in set(read_all())],
                                        columns=database.RAW_HEADER.keys())

        # Compute a boolean array indicating the add values to raw
        condition = ~self.raw_entries.index.isin(self.edited_entries["RawIndex"].dropna())

        # Filter by the condition to get new data values
        new_data = self.raw_entries[condition].reset_index()

        new_data.rename(columns={"index": "RawIndex"},
                        inplace=True)

        new_data["Edited"] = " "

        # Add new data to the edited table
        self.edited_entries = pd.concat([self.edited_entries, new_data],
                                        ignore_index=True)

    def save(self):
        conn = database.get_engine(self.db_path).connect()
        self.raw_entries.to_sql(name="RAW_ENTRIES",
                                con=conn,
                                if_exists="replace",
                                dtype=database.RAW_HEADER
                                )

        self.edited_entries.to_sql(name="EDITED_ENTRIES",
                                   con=conn,
                                   if_exists="replace",
                                   dtype=database.EDITED_HEADER,
                                   index_label="index")

    def search(self, **kwargs):
        """
        Searches the database of entries to show relevant results

        Parameters
        ----------
        team: Team number
        match: Match number
        name: Scout name
        board: Board
        edited: ?

        :return: A filtered DataFrame with the same columns as 
        edited_entries and matches the searching criteria
        """

        filters = {k.capitalize(): kwargs[k] for k in kwargs.keys() if kwargs[k]}

        df = self.edited_entries

        for i in filters.keys():
            if i in FILTER_HEADER:
                df = df[df[i].isin(filters[i])]

        return df.sort_values(by=FILTER_SORT)

    def match_row(self, match, team, name):
        """
        Simpler and more efficient way of matching match, team, and name than search
        :param match:
        :param team:
        :param name:
        :return: a matching row, or an empty DataFrame if entry doesn't exist
        """
        return self.edited_entries[(self.edited_entries["Match"] == match) &
                                   (self.edited_entries["Team"] == team) &
                                   (self.edited_entries["Name"] == name)]

    def append(self, **kwargs):
        """
        Add a new entry to the data
        :param kwargs: entry info dictionary
        :return: The new entry info, or old if match, team, and name already exists
        """

        entry_data = {k.capitalize(): kwargs[k] for k in kwargs.keys()}

        match = entry_data.get("Match")
        team = entry_data.get("Team")
        name = entry_data.get("Name")

        matching_row = self.match_row(match, team, name)

        if matching_row.empty:
            new_data = pd.DataFrame([{
                "Match": match,
                "Team": team,
                "Name": name,
                "StartTime": format_time.display_time(time.time()),
                "Board": self.board_finder.get_first().name(),
                "Data": "",
                "Comments": "",
                "RawIndex": np.nan,
                "Edited": ""

            }], columns=database.EDITED_HEADER.keys())

            self.edited_entries = pd.concat([self.edited_entries, new_data], ignore_index=True)

            return self[self.match_row(match, team, name).index[0]]

        return self[matching_row.index[0]]

    def remove(self, index):
        """Removes the entry at the index"""
        # TODO Possibly Use a removed flag instead of actually dropping to avoid data getting recopied
        self.edited_entries.drop(index=index, inplace=True)