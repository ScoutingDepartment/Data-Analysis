"""This is a template for analysis scripts"""

import pandas as pd

TITLE_NAME = "Auto List"  # The name to display
SOURCE_NAME = "auto_list"  # The name to be accessed by other code
LABELS = ["Team",
          "Match",
          "Total Success",
          "Total Attempt and Success",
          "Scale Success",
          "Switch Success",
          "First Time",
          "Last Time",
          "Action 1",
          "Action 2",
          "Action 3",
          "Action 4",
          "Action 5"
          ]  # Column labels for table, and row labels for lookup (later thing)


def get_rows(manager) -> None:

    for entry in manager.entries:
        auto_data_points = ["Auto scale", "Auto switch", "Auto scale success", "Auto switch success"]
        times = {
            "Auto scale": [],
            "Auto switch": [],
            "Auto scale success": [],
            "Auto switch success": []
        }
        actions = []
        for data_point in auto_data_points:
            for occurrence_time in entry.look(data_point):
                times[data_point].append(occurrence_time)
                actions.append((occurrence_time, data_point))
        actions = sorted(actions, key=lambda x: (x[0]))
        num_actions = len(actions)
        action_list = []
        for i in range(5):
            if i < num_actions:
                action_list.append(actions[i][1])
            else:
                action_list.append("none")

        switch_auto_successes = entry.count("Auto switch")
        scale_auto_successes= entry.count("Auto scale")
        switch_auto_attempts= entry.count("Auto switch attempt")
        scale_auto_attempts= entry.count("Auto scale attempt")
        row_data = {
            "Team": entry.team,
            "Match": entry.match,
            "Total Success": switch_auto_successes + scale_auto_successes,
            "Total Attempt and Success": switch_auto_successes + switch_auto_attempts + scale_auto_successes + scale_auto_attempts,
            "Scale Success": scale_auto_successes,
            "Switch Success": switch_auto_successes,
            "First Time": actions[0] [0] if num_actions > 0 else 0,
            "Last Time": actions[-1] [0] if num_actions > 0 else 0,
            "Action 1": action_list[0],
            "Action 2": action_list[1],
            "Action 3" : action_list[2],
            "Action 4": action_list[3],
            "Action 5": action_list[4]
        }
        yield row_data
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

def compute_table(manager):
    table = pd.DataFrame(get_rows(manager))[LABELS]
    return table
