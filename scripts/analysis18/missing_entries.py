TITLE_NAME = "Missing Entries"
SOURCE_NAME = "missing_entries"
LABELS = ["Match #",
          "Red 1",
          "Red 2",
          "Red 3",
          "Blue 1",
          "Blue 2",
          "Blue 3"
          ]


def compute_table(manager):
    ms = manager["match_schedule"].data
    se = manager["scouted_entries"].data
    return ms[ms != se]
