"""
Manages all the entered entries for navigation
A list of all entries
"""

import pandas as pd

from processor import database


class EntryManager:

    def __init__(self, database_file):

        self.database_file = database_file
        self.edited_data = pd.DataFrame()  # The edited data

        conn = database.get_connection(self.database_file)

        try:
            self.original_data = pd.read_sql("SELECT * FROM RAW_ENTRIES", conn)

            # TODO If Edited Table exists: Read Edited Entries Table;
            # TODO Merge Raw Table with Edited Table to avoid loss of changes by comparing columns
            pass

        except IOError:
            # TODO Change Error Type
            # TODO Handle errors in case the connection is not established or table doesn't exist
            pass

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

                    "Data": [("Type", "Value", "Exclude")], #TODO Change this with actual data

                    # TODO Data can be possibly a pandas table

                    "Comments": self.edited_data['Comments'][index]
                    }
        return {}

    def increment(self, df, index, increment):

        incremented_entry = df[((index + increment + 1) % df.shape[0])]
        unfiltered_index = self.filter(Match=incremented_entry['Match'],
                                       Team=incremented_entry['Team'],
                                       Name=incremented_entry['Name'])['index']

        return self.entry_at(unfiltered_index)

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

    def remove_entry(self, index):
        # TODO Wrong
        self.edited_data.drop(index=index, inplace=True)

    def edit_entry(self, index, data):
        # Used to change data for one entry

        # TODO Call the board to get data type #
        # TODO Call validation and format parser
        # TODO call the encoder
        self.edited_data.set_value(index, "Data", data)

    def save(self):

        conn = database.get_connection(self.database_file)

        self.edited_data.to_sql(name="EDITED_DATA",
                                con=conn,
                                if_exists="replace",
                                dtype=database.EDITED_HEADER)

        conn.close()


if __name__ == "__main__":
    # Do Testing Here
    entry_manager = EntryManager("../data/database/data.warp7")
