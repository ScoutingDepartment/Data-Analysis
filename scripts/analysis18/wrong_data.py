import pandas as pd

TITLE_NAME = "Wrong data"
SOURCE_NAME = "wrong_data"
LABELS = ["Scout",
          "Team",
          "Match",
          "Alliance",
          "Double outtakes"]


def get_rows(manager):
    for entry in manager.entries:
        if not entry.board.alliance() == "N":
            tracked_data_types = ['Tele intake',
                                  'Tele scale',
                                  'Tele exchange',
                                  'Tele opponent switch',
                                  'Tele alliance switch']

            outtakes = tracked_data_types[1:]

            time_series = [None for _ in range(150)]
            for data_type in tracked_data_types:
                for occurrence_time in entry.look(data_type):
                    time_series[occurrence_time - 1] = data_type

            has_cube = False
            first_outtake_ignored = False
            double_outtakes = 0
            for event in time_series:
                if not first_outtake_ignored:
                    if event in outtakes:
                        first_outtake_ignored == True
                else:
                    if event in outtakes:
                        if not has_cube:
                            double_outtakes += 1
                        has_cube = False
                    if event == "Tele intake":
                        has_cube = True

        yield {"Scout": entry.name,
               "Team": entry.team,
               "Match": entry.match,
               "Alliance": entry.board.alliance(),
               "Double outtakes": double_outtakes}


def compute_table(manager):
    table = pd.DataFrame(get_rows(manager))[LABELS]
    return table
