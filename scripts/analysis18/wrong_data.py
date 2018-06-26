import pandas as pd

TITLE_NAME = "Wrong data"
SOURCE_NAME = "wrong_data"
LABELS = ["Scout",
          "Team",
          "Match",
          "Alliance",
          "Double outtakes",
          "Wrong auto line",
          "Wrong climb"]


def get_rows(manager):
    for entry in manager.entries:
        if not entry.board.alliance() == "N":
            tracked_data_types = ['Tele intake',
                                  'Tele scale',
                                  'Tele exchange',
                                  'Tele opponent switch',
                                  'Tele alliance switch']

            outtakes = ['Tele scale',
                        'Tele exchange',
                        'Tele opponent switch',
                        'Tele alliance switch']

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
                        first_outtake_ignored = True
                else:
                    if event in outtakes:
                        if not has_cube:
                            double_outtakes += 1
                        has_cube = False
                    if event == "Tele intake":
                        has_cube = True

            if manager.tba_available:
                try:
                    tba = manager.tba
                    app_climbed = entry.final_value("Climb", default=0) == 2

                    match_key = str(manager.tba_event) + "_qm" + str(entry.match)

                    if entry.board.alliance().lower() == "r":
                        all = "blue"
                    elif entry.board.alliance().lower() == "b":
                        all = "red"
                    else:
                        all = "unknown"

                    alliance_teams = tba.match(key=match_key)['alliances'][all]["team_keys"]
                    if "frc" + str(entry.team) in alliance_teams:
                        tba_robot_number = alliance_teams.index("frc" + str(entry.team)) + 1
                    else:
                        continue

                    tba_climbed = tba.match(key=match_key)['score_breakdown'][all][
                                      "endgameRobot" + str(tba_robot_number)] == "Climbing"
                    tba_auto_line = tba.match(key=match_key)['score_breakdown'][all][
                                        "autoRobot" + str(tba_robot_number)] == "AutoRun"

                    yield {"Scout": entry.name,
                           "Team": entry.team,
                           "Match": entry.match,
                           "Alliance": entry.board.alliance(),
                           "Double outtakes": double_outtakes,
                           "Wrong auto line": not (entry.final_value("Auto line", default=0) == 1) == tba_auto_line,
                           "Wrong climb": not (entry.final_value("Climb", default=0) == 2) == tba_climbed}
                except:
                    import traceback
                    traceback.print_exc()


            else:
                yield {"Scout": entry.name,
                       "Team": entry.team,
                       "Match": entry.match,
                       "Alliance": entry.board.alliance(),
                       "Double outtakes": double_outtakes,
                       "Wrong auto line": "",
                       "Wrong climb": ""}


def compute_table(manager):
    table = pd.DataFrame(get_rows(manager))[LABELS]
    return table
