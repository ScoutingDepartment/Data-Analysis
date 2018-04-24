from itertools import chain

import numpy as np
import pandas as pd

TITLE_NAME = "Scale Autos"
SOURCE_NAME = "scale_autos"
LABELS = ["Team",
          "Minimum Success #",
          "Maximum Success #",
          "Fastest Success Time",
          "Success/Attempt Ratio"
          ]


def get_autos_data(manager):
    scale_autos = {}
    for entry in manager.entries:
        if not entry.board.alliance() == "N":  # Check for Power ups

            if entry.team not in scale_autos.keys():  # Make new list if team doesn't exist
                scale_autos[entry.team] = []

            scale_autos[entry.team].append((entry.look("Auto scale attempt"), entry.look("Auto scale")))

    return scale_autos


def get_rows(manager):
    for team, auto_data in get_autos_data(manager).items():
        attempt, success = zip(*auto_data)

        attempt_counts = list(map(len, attempt))
        success_counts = list(map(len, success))
        success_times = list(chain(*success))

        attempt_sum = sum(attempt_counts)
        success_sum = sum(success_counts)

        # if success_counts:
        #     r_min_success = min(success_counts)
        #     r_max_success

        a = attempt_sum + success_sum

        yield {
            "Team": team,
            "Minimum Success #": min(success_counts) if success_counts else np.nan,
            "Maximum Success #": max(success_counts) if success_counts else np.nan,
            "Fastest Success Time": min(success_times) if success_times else np.nan,
            "Success/Attempt Ratio": success_sum / a if a != 0 else np.nan
        }


def compute_table(manager):
    try:
        return pd.DataFrame(get_rows(manager))[LABELS]
    except:
        import traceback
        traceback.print_exc()
