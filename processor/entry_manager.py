"""
Manages all the entered entries for navigation
A list of all entries
"""

import pandas as pd
from sqlalchemy.exc import SQLAlchemyError

from processor import database, board, decoder

FILTER_HEADER = ['Match', 'Team', 'Name', "Board", "Edited"]
FILTER_SORT = ['Match', 'Team']


class EntryManager:

    def __init__(self, db_file, board_path):
        """
        Loads raw data and edited data from database
        :param db_file: the database file to read from
        """

        self.finder = board.Finder(board_path)

        self.database_file = db_file

        engine = database.get_engine(self.database_file)
        conn = engine.connect()

        try:
            # Read the entire table but use 'index' as the table index
            self.original_data = pd.read_sql(sql="SELECT * FROM RAW_ENTRIES",
                                             con=conn,
                                             index_col="index")

            # Check if we use the existing EDITED_ENTRIES table or create a new one
            if engine.dialect.has_table(connection=conn,
                                        table_name="EDITED_ENTRIES"):

                self.edited_data = pd.read_sql(sql="SELECT * FROM EDITED_ENTRIES",
                                               con=conn,
                                               index_col="index")

                # Compute a boolean array indicating the add values to raw
                condition = ~self.original_data.index.isin(self.edited_data["RawIndex"])

                # Filter by the condition to get new data values
                new_data = self.original_data[condition].reset_index()

                new_data.rename(columns={"index": "RawIndex"},
                                inplace=True)

                new_data["Edited"] = " "

                # Add new data to the edited table
                self.edited_data = pd.concat([self.edited_data, new_data],
                                             ignore_index=True)

            else:
                self.edited_data = self.original_data.reset_index()

                self.edited_data.rename(columns={"index": "RawIndex"},
                                        inplace=True)

                self.edited_data["Edited"] = " "

        except SQLAlchemyError as error:
            self.original_data = pd.DataFrame(columns=database.RAW_HEADER.keys())
            self.edited_data = pd.DataFrame(columns=database.EDITED_HEADER.keys())
            print(error)

        finally:
            conn.close()

    def filter(self, **kwargs):
        """
        Filters the database of entries to show relevant results

        Parameters
        ----------
        team: Team number
        match: Match number
        name: Scout name
        board: Board
        edited: Time edited

        :return: A filtered DataFrame match the criteria
        """

        filters = {k.capitalize(): kwargs[k] for k in kwargs.keys()}

        df = self.edited_data

        for i in filters.keys():
            if i in FILTER_HEADER:
                df = df[df[i].isin(filters[i])]

        return df.sort_values(by=FILTER_SORT)[FILTER_HEADER].reset_index()

    def data_row_at(self, index):
        if index in self.edited_data.index:
            return self.edited_data.iloc[index]
        return None

    def entry_at(self, index):
        """
        Get data for one specific entry based on the index
        :param index: the index to lookup
        :return: The entry info, or empty dict if row does not exist
        """

        row = self.data_row_at(index)

        if row is not None:
            entry_board = self.finder.get_board_by_name(row["Board"])
            entry_info = {k: row[k] for k in ["Match", "Team", "Name", "StartTime", "Comments"]}
            entry_info["Board"] = entry_board.name()
            entry_info["Data"] = list(decoder.decode(row["Data"], entry_board))
            return entry_info

        return {}

    def increment(self, table_from_excel, index, increment_by):
        old_index = ''
        for i in range(len(list(table_from_excel.index.values))):
            if list(table_from_excel.index.values)[i] == index:
                old_index = i
                break

        if old_index == '':
            return ''

        new_index = list(table_from_excel.index.values)[
            (old_index + increment_by) % len(list(table_from_excel.index.values))]
        return self.entry_at(new_index)

    def next(self, df, index):
        return self.increment(df, index, 1)

    def previous(self, df, index):
        return self.increment(df, index, -1, )

    def add_entry(self, **entry_data):

        match = entry_data.get("Match")
        team = entry_data.get("Team")
        name = entry_data.get("Name")

        # Check if entry exists
        if len(self.filter(Match=match, Team=team, Name=name)) == 0:
            self.edited_data.append(entry_data)

            # TODO return the proper index

    def remove_entry(self, match, team, name, index_value):
        match_at_index = str(self.edited_data.loc[index_value, "Match"])
        print(match_at_index)
        team_at_index = str(self.edited_data.loc[index_value, "Team"])
        print(team_at_index)
        name_at_index = str(self.edited_data.loc[index_value, "Name"])
        print(name_at_index)

        match_correct = match_at_index == match
        team_correct = team_at_index == team
        name_correct = name_at_index == name

        if match_correct and team_correct and name_correct:
            self.edited_data.drop(index=index_value, inplace=True)

    def edit_entry(self, index, data):
        # Used to change data for one entry

        # TODO Call the board to get data type #
        # TODO Call validation and format parser
        # TODO call the encoder
        self.edited_data.set_value(index, "Data", data)

    def revert_entry(self, index):
        pass

    def save(self):

        conn = database.get_engine(self.database_file).connect()

        self.edited_data.to_sql(name="EDITED_ENTRIES",
                                con=conn,
                                if_exists="replace",
                                dtype=database.EDITED_HEADER,
                                index_label="index")

        conn.close()


if __name__ == "__main__":
    # Do Testing Here

    entry_manager = EntryManager("../data/database/data.warp7", "../data/board/")
    print(entry_manager.entry_at(11))
    entry_manager.save()
    #print(entry_manager.remove_entry(42, 4152, "Sam.s", 2))
    # print(entry_manager.edited_data)