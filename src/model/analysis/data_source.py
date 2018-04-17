from typing import List

from src.model.analysis.scripted_table import ScriptedTable
from src.model.entrylib import Entry


class DataSource:

    def __init__(self, entries: List["Entry"], tables: List["ScriptedTable"]):
        self.entries = entries
        self.__tables = tables

    def __getattr__(self, n):
        for t in self.__tables:
            if t.source_name == n:
                return t
        raise AttributeError("Attribute Not Found")
