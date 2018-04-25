import pandas as pd
import tbapy

TITLE_NAME = "Tba powerups"
SOURCE_NAME = "tba_powerups"
LABELS = ["Match",
          "Red force played", "Red force total",
          "Red levitate played", "Red levitate total",
          "Red boost played", "Red boost total",
          "Blue force played", "Blue force total",
          "Blue levitate played", "Blue levitate total",
          "Blue boost played", "Blue boost total"]


def row_data_generator(manager, tba):
    event = tba.event_matches(manager.tba_event)
    for match in event:

        row_data = {'Match': match}
        for alliance in ['Red', 'Blue']:
            row_data[alliance + " force played"] = match['score_breakdown'][alliance]['vaultForcePlayed']
            row_data[alliance + " force total"] = match['score_breakdown'][alliance]['vaultForceTotal']
            row_data[alliance + " levitate played"] = match['score_breakdown'][alliance]['vaultLevitatePlayed']
            row_data[alliance + " levitate total"] = match['score_breakdown'][alliance]['vaultLevitateTotal']
            row_data[alliance + " boost played"] = match['score_breakdown'][alliance]['vaultBoostPlayed']
            row_data[alliance + " boost total"] = match['score_breakdown'][alliance]['vaultBoostTotal']
        yield row_data


def compute_table(manager):
    tba = tbapy.TBA(manager.tba_key)
    return pd.DataFrame(row_data_generator(manager, tba))[LABELS]
