import numpy as np
import pandas as pd

TITLE_NAME = "Scouted Entries"
SOURCE_NAME = "scouted_entries"
LABELS = [
          "Red 1",
          "Red 2",
          "Red 3",
          "Blue 1",
          "Blue 2",
          "Blue 3"
          ]


def compute_table(manager):
    ms = manager["match_schedule"].data
    scouted_entries = pd.DataFrame(index=ms.index, columns=LABELS)

    for entry in manager.entries:
        if entry.board.alliance() != "N":
            m = "Quals {}".format(entry.match)
            b = entry.board.name()
            t = np.int32(entry.team)
            if m in scouted_entries.index:
                if int(ms.at[m, b]) == entry.team:
                    scouted_entries.at[m, b] = t
    return scouted_entries
