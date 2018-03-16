"""
Manages all the entered entries for navigation
A list of all entries
"""
import pandas as pd


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
    def __init__(self):
        self.entries = pd.DataFrame()
