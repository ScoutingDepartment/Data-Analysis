from importlib import import_module


class ScriptedTable:

    def __init__(self, module_name):
        script = import_module(module_name)

        self.table_name = script.TABLE_NAME
        self.source_name = script.SOURCE_NAME
        self.dependencies = script.DEPENDENCIES

        self.result_type = script.RESULT_TYPE

        self.compute_function = script.compute_table
        self.data = None

    def call_compute(self, data_source):
        self.data = self.compute_function(data_source)
