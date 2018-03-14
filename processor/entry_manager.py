"""
Manages all the entered entries for navigation
A list of all entries
"""
import pandas as pd


class EntryManager:
    def __init__(self):
        self.entries = pd.DataFrame()
