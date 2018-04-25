import pandas as pd

TITLE_NAME = "MATCH SCHEDULE"
SOURCE_NAME = "match_schedule"
LABELS = ["Match #",
          "Red 1",
          "Red 2",
          "Red 3",
          "Blue 1",
          "Blue 2",
          "Blue 3"
          ]


def compute_table(manager):
    return pd.DataFrame(columns=LABELS)
