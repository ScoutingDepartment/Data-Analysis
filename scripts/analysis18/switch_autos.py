from itertools import chain

import numpy as np
import pandas as pd

TITLE_NAME = "Switch Autos"
SOURCE_NAME = "switch_autos"
LABELS = ["Team",
          "Minimum Success #",
          "Maximum Success #",
          "Fastest Success Time",
          "Success/Attempt Ratio"
          ]


def get_autos_data(manager):
    switch_autos = {}
    for entry in manager.entries:
        if not entry.board.alliance() == "N":  # Check for Power ups

            if entry.team not in switch_autos.keys():  # Make new list if team doesn't exist
                switch_autos[entry.team] = []

            switch_autos[entry.team].append((entry.look("Auto switch attempt"), entry.look("Auto switch")))

    return switch_autos


def get_rows(manager):
    for team, auto_data in get_autos_data(manager).items():
        attempt, success = zip(*auto_data)

        attempt_counts = list(filter(bool, map(len, attempt)))
        success_counts = list(filter(bool, map(len, success)))
        success_times = list(chain(*success))

        attempt_sum = sum(attempt_counts)
        success_sum = sum(success_counts)

        a = attempt_sum + success_sum

        yield {
            "Team": team,
            "Minimum Success #": min(success_counts) if success_counts else np.nan,
            "Maximum Success #": max(success_counts) if success_counts else np.nan,
            "Fastest Success Time": min(success_times) if success_times else np.nan,
            "Success/Attempt Ratio": success_sum / a if a != 0 else np.nan
        }


def compute_table(manager):
    return pd.DataFrame(get_rows(manager))[LABELS]
