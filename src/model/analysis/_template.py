"""This is a template for analysis scripts"""

import pandas as pd

TITLE_NAME = ""  # The name to display
SOURCE_NAME = ""  # The name to be accessed by other code
LABELS = []  # Column labels for table, and row labels for lookup (later thing)


def compute_table(manager, result_table: "pd.DataFrame") -> None:
    """
    Define this function to compute a set of data. It is directly called
    by the table manager whenever it needs to recalculate this specific
    table or the entire list of tables, after this script file is added
    to the manager

    :param manager: The AnalysisManager that calls this function. This
                    variable has access to all the other data that have
                    been computed. A table can be accessed by
                    manager[NAME] where NAME is the SOURCE_NAME specified
                    in its respective file. Entries can be
                    accessed by manager.entries as a list of Entry objects.
                    The function should not try to access any other part
                    of the manager object. See analysis_manager.py

    :param result_table: An instance of pd.DataFrame created to store the
                         result data, and has been given proper column
                         labels. Any resulting data should be placed into
                         this table, because it is referenced by the table
                         manager and data will be lost otherwise. Use the
                         syntax result_table.loc[ROW_LABEL] = ROW_DATA
                         to set the appropriate data (ROW_DATA is a list of
                         ints/strings following the order defined by the
                         LABELS constant). If the compute function has been
                         called before, result_table.loc[ROW_LABEL] will also
                         provide the result of the previous calculation

    :return: Nothing needs to be returned from this function because
             changes to the data use the reference passed by the argument
    """
    pass


"""
import pandas as pd

TITLE_NAME = ""
SOURCE_NAME = ""
LABELS = []


def compute_table(manager, result_table: "pd.DataFrame") -> None:
    pass
"""
