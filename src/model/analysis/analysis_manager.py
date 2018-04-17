import os

import pandas as pd

from src.model import boards
from src.model.analysis.scripted_table import ScriptedTable
from src.model.database import get_engine
from src.model.entrylib import Entry


class AnalysisManager:
    def __init__(self, db_path: "str",
                 boards_dir_path: "str",
                 *table_modules: "str"):
        self.boards_finder = boards.Finder(boards_dir_path)

        if not os.path.exists(db_path):
            raise FileNotFoundError("Database file not found")

        conn = get_engine(db_path).connect()

        entries_table = pd.read_sql(sql="SELECT * FROM EDITED_ENTRIES",
                                    con=conn,
                                    index_col="index").sort_values(by=['Match', 'Team'])

        self.entries: "Entry" = [Entry(row, self.boards_finder) for _, row in entries_table.iterrows()]
        self.tables: "ScriptedTable" = []
        self.update_table_modules(*table_modules)

    def update_table_modules(self, *table_modules: "str"):
        self.tables = [ScriptedTable(m) for m in table_modules]
