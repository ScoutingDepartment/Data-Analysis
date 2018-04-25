import numpy as np
import pandas as pd

TITLE_NAME = "Team Averages"
SOURCE_NAME = "team_averages"
LABELS = ["Team",
          "Average Scale",
          "Average Alliance Switch",
          "Average Opponent Switch",
          "Average Exchange"]


def get_team_data(manager):
    teams_data = {}
    for entry in manager.entries:
        if not entry.board.alliance() == "N":  # Check for Power ups

            if entry.team not in teams_data.keys():  # Make new list if team doesn't exist
                teams_data[entry.team] = []

            teams_data[entry.team].append((entry.count("Tele scale"),
                                           entry.count("Tele alliance switch"),
                                           entry.count("Tele opponent switch"),
                                           entry.count("Tele exchange")))

    return teams_data


def get_rows(manager):
    for team, counts in get_team_data(manager).items():
        scale, a_switch, o_switch, exchange = zip(*counts)  # Counts when they don't do it

        yield {"Team": team,
               "Average Scale": sum(scale) / len(scale) if len(scale) > 0 else np.nan,
               "Average Alliance Switch": sum(a_switch) / len(a_switch) if len(a_switch) > 0 else np.nan,
               "Average Opponent Switch": sum(o_switch) / len(o_switch) if len(o_switch) > 0 else np.nan,
               "Average Exchange": sum(exchange) / len(exchange) if len(exchange) > 0 else np.nan
               }


def compute_table(manager):
    return pd.DataFrame(get_rows(manager))[LABELS]
