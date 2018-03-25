"""
Manages all the entered entries for navigation
A list of all entries
"""

import pandas as pd
from sqlalchemy.exc import SQLAlchemyError

from processor import database


class EntryManager:

    def __init__(self, db_file):
        """
        Loads raw data and edited data from database
        :param db_file: the database file to read from
        """

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
                new_data.rename(columns={"index": "RawIndex"}, inplace=True)
                new_data["Edited"] = " "

                # Add new data to the edited table
                self.edited_data = pd.concat([self.edited_data, new_data], ignore_index=True)

            else:
                self.edited_data = self.original_data.reset_index()
                self.edited_data.rename(columns={"index": "RawIndex"}, inplace=True)
                self.edited_data["Edited"] = " "

        except SQLAlchemyError:
            self.original_data = pd.DataFrame(columns=database.RAW_HEADER.keys())
            self.edited_data = pd.DataFrame(columns=database.EDITED_HEADER.keys())

        finally:
            conn.close()

    def filter(self, **filter_dict):

        df = self.edited_data

        for i in filter_dict.keys():
            df = df[df[i].isin(filter_dict[i])]

        return df.sort_values(by=['Match', 'Team']).loc[:, ['index', 'Match', 'Team', 'Name']]

    def entry_at(self, index):

        if not self.edited_data.empty:  # TODO Also check bounds

            # TODO Create data info dictionary
            # TODO Create data list: call the decoder and formatter

            return {"Match": self.edited_data['Match'][index],
                    "Team": self.edited_data['Team'][index],
                    "Name": self.edited_data['Name'][index],
                    "StartTime": self.edited_data['StartTime'][index],
                    "Board": self.edited_data['Board'][index],

                    "Data": [("Type", "Value", "Exclude")],  # TODO Change this with actual data

                    # TODO Data can be possibly a pandas table

                    "Comments": self.edited_data['Comments'][index]
                    }
        return {}

    def increment(self, df, index, increment):
        old_index = ''
        for i in range(len(list(df.index.values))):
            if list(df.index.values)[i] == index:
                old_index = i
                break

        if old_index == '':
            return ''

        new_index = list(df.index.values)[(old_index + increment) % len(list(df.index.values))]
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
        # TODO Wrong
        # TODO Check if the index is correct
        match_at_index = self.edited_data.loc[index_value, "Match"]
        print(match_at_index)
        team_at_index = self.edited_data.loc[index_value, "Team"]
        print(team_at_index)
        name_at_index = self.edited_data.loc[index_value, "Name"]
        print(name_at_index)

        if match_at_index == match:
            match_correct = True
        else:
            match_correct = False

        match_correct = match_at_index == match

        if team_at_index == team:
            team_correct = True
        else:
            team_correct = False

        if name_at_index == name:
            name_correct = True
        else:
            name_correct = False
        if match_correct and team_correct and name_correct:
            self.edited_data.drop(index=index_value, inplace=True)

    def edit_entry(self, index, data):
        # Used to change data for one entry

        # TODO Call the board to get data type #
        # TODO Call validation and format parser
        # TODO call the encoder
        self.edited_data.set_value(index, "Data", data)

    def save(self):

        conn = database.get_engine(self.database_file).connect()

        self.edited_data.to_sql(name="EDITED_ENTRIES",
                                con=conn,
                                if_exists="replace",
                                dtype=database.EDITED_HEADER, index_label="index")

        conn.close()


if __name__ == "__main__":
    # Do Testing Here
    entry_manager = EntryManager("../data/database/data.warp7")
    # entry_manager.save()
    # print(entry_manager.remove_entry(42, 4152, "Sam.s", 2))
    # print(entry_manager.edited_data)
