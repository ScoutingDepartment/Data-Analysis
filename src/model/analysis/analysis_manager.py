from importlib import import_module

import pandas as pd


class AnalysisManager:
    class Table:
        def __init__(self, module):
            self.title = module.TITLE_NAME
            self.name = module.SOURCE_NAME
            self.labels = module.LABELS
            self.compute = module.compute_table
            self.data = pd.DataFrame(columns=self.labels)

    def __init__(self, table_scripts):  # , db_path, boards_dir_path):

        # self.boards_finder = boards.Finder(boards_dir_path)
        #
        # if not os.path.exists(db_path):
        #     raise FileNotFoundError("Database file not found")
        #
        # conn = get_engine(db_path).connect()
        #
        # entries_table = pd.read_sql(sql="SELECT * FROM EDITED_ENTRIES",
        #                             con=conn,
        #                             index_col="index").sort_values(by=['Match', 'Team'])
        #
        # self.entries = [Entry(row, self.boards_finder) for _, row in entries_table.iterrows()]

        self.entries = []
        self.tables = [self.Table(import_module(s)) for s in table_scripts]

    def __getitem__(self, name):

        for table in self.tables:
            if table.name == name:
                return table
        return None

    def compute_all(self):
        for table in self.tables:
            table.compute(self, table.data)


if __name__ == "__main__":
    am = AnalysisManager(table_scripts=["_template"])
    am.compute_all()
