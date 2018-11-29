import os
import sys
from importlib import import_module

import pandas as pd
import xlwings as xl
from tbapy import TBA

from src.model import boards, database
from src.model.entrylib import Entry


class AnalysisManager:
    class Table:
        def __init__(self, module):
            self.title = module.TITLE_NAME
            self.name = module.SOURCE_NAME
            self.labels = module.LABELS
            self.compute = module.compute_table
            self.data = pd.DataFrame(columns=self.labels)

    def __init__(self,
                 boards_dir_path,
                 db_path,
                 scripts_path,
                 table_scripts,
                 tba_key,
                 tba_event):

        self.boards_finder = boards.Finder(boards_dir_path)

        if not os.path.exists(db_path):
            raise FileNotFoundError("Database file not found")

        conn = database.get_engine(db_path).connect()

        entries_table = pd.read_sql(sql="SELECT * FROM EDITED_ENTRIES",
                                    con=conn,
                                    index_col="index").sort_values(by=['Match', 'Team'])

        self.entries = [Entry(row, self.boards_finder) for _, row in entries_table.iterrows()]

        if scripts_path not in sys.path:
            sys.path.append(scripts_path)

        self.tables = [self.Table(import_module(s)) for s in table_scripts]

        self.tba = TBA(tba_key)
        self.tba_available = True
        self.tba_event = tba_event

        if self.tba_available:
            self.tba_matches = self.tba.event_matches(self.tba_event)
        else:
            self.tba_matches = None

    def __getitem__(self, name):

        for table in self.tables:
            if table.name == name:
                return table
        return None

    def compute_all(self, tba_available=True):
        self.tba_available = tba_available
        for table in self.tables:
            table.data = table.compute(self)

    def open_excel_instance(self):
        book = xl.Book()
        for table in self.tables:
            sheet = book.sheets.add(table.title)
            sheet.range("A1").options(pd.DataFrame, expand="table").value = table.data

    def save_csv_folder(self, path):
        for table in self.tables:
            fp = os.path.join(path, "{}.csv".format(table.name))
            table.data.to_csv(fp)

    def table_names(self):
        for table in self.tables:
            yield table.title

    def title_to_name(self, title):
        for table in self.tables:
            if table.title == title:
                return table.name
        return None
