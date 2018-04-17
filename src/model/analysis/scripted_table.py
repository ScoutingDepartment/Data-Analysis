from importlib import import_module

import pandas as pd


class ScriptedTable:

    def __init__(self, module_name):
        script = import_module(module_name)

        self.table_name = script.TABLE_NAME
        self.source_name = script.SOURCE_NAME
        self.column_labels = script.COLUMN_LABELS
        self.compute_table = script.compute_table

        self.data = pd.DataFrame(columns=self.column_labels)

    def call_compute(self, data_source):
        self.compute_table(data_source, self.data)
