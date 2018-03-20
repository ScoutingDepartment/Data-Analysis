"""
Manages all the entered entries for navigation
A list of all entries
"""

import pandas as pd

from processor import database

HEADERS = ["Match",
           "Team",
           "Name",
           "StartTime",
           "Board",
           "Data",
           "Comments"
           ]

def find_entries(df, match='', team='', name=''):
    """
    :param df: DataFrame which contains all entries
    :param match: the match you want entries from
    :param team: the team you want entries from
    :param name: the name of the scouter for whom you want matches from (exact spelling)
    :return: DataFrame which contains all of the entries which match all of the given parameters
    """

    if match != '':
        df = df[df['Match'].isin(match)]

    if team != '':
        df = df[df['Team'].isin(team)]

    if name != '':
        df = df[df['Name'].isin(name)]

    return df


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

    def filter(self, match=None, team=None, name=None):
        # TODO other options: filter by time and board
        # TODO consider: use one argument (dictionary) instead of multiple because previous and next also calls

        # Used for searching through entries

        # TODO Return a new DataFrame/List containing the filtered list
        # TODO Add the option for list of filters
        # TODO Return the filtered list excluding data and comments because they don't need to be displayed
        # TODO Sort the data in a logical way

        return pd.DataFrame(self.edited_data)  # TODO Replace this

    def entry_at(self, index):
        # Used for displaying a specific entry

        if not self.edited_data.empty:  # TODO Also check bounds

            # TODO Create data info dictionary
            # TODO Create data list: call the decoder and formatter

            return {"Match": 0,
                    "Team": 0,
                    "Name": "",
                    "StartTime": "",
                    "Board": "",

                    "Data": [
                        ("Type String", "Type Value (Formatted)", "Exclude/Undo")
                    ],

                    # TODO Data can be possibly a pandas table

                    "Comments": ""
                    }
        return {}

    def original_entry_at(self, index):

        # TODO call entry at
        # TODO connect to RAW_ENTRIES database
        # TODO use info from entry at to locate entry in raw database

        # TODO Return a data info dictionary (see entry_at)

        return {}

    def next(self, index, match=None, team=None, name=None):

        # TODO Call self.filter to get list of filtered entries
        # TODO Find the next index
        # TODO Return the next entry, or current entry if no more to be found

        next_index = 0


        return self.entry_at(next_index)

    def previous(self, index, match=None, team=None, name=None):

        # TODO Call self.filter to get list of filtered entries
        # TODO Find the previous index
        # TODO Return the previous entry, or current entry if no more to be found

        previous_index = 0

        return self.entry_at(previous_index)

    def add_entry(self, match, team, name, start_time, data, comments):
        # TODO Append one entry to the edited table
        new_row = pd.DataFrame(
            data={HEADERS[0]: [match], HEADERS[1]: [team], HEADERS[2]: [name], HEADERS[3]: [start_time], HEADERS[
                4]: [data], HEADERS[5]: [comments]})

        if len(find_entries(match, team, name)) > 0:
            self.df.append(new_row)
        else:
            return "Duplicate"

        new_index = 0  # Not sure what this is for
        return new_index

    def remove_entry(self, index):
        # TODO remove a row from the table if such row exists
        self.edited_data.drop(index=index)
        pass

    def edit_entry(self, index, data):
        # Used to change data for one entry

        # TODO Call the board to get data type #
        # TODO Call validation and format parser
        # TODO call the encoder
        self.edited_data.set_value(index, "Data", data)

    def save(self):

        conn = database.get_connection(self.database_file)
        # TODO if exist replace
        self.edited_data.to_sql("EDITED_DATA", conn, if_exists="replace")
        # TODO Save entries table to database

        conn.close()


entry_manager = EntryManager("../data/database/data.warp7")
