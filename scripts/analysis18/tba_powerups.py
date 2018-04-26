import pandas as pd

TITLE_NAME = "Tba powerups"
SOURCE_NAME = "tba_powerups"
LABELS = ["Match",
          "Red force played", "Red force total",
          "Red levitate played", "Red levitate total",
          "Red boost played", "Red boost total",
          "Blue force played", "Blue force total",
          "Blue levitate played", "Blue levitate total",
          "Blue boost played", "Blue boost total"]


def row_data_generator(manager):
    tba = manager.tba
    event = tba.event_matches(manager.tba_event)
    for match in event:
        if match['score_breakdown'] != None and match['comp_level'] == 'qm':
            row_data = {'Match': match['match_number']}
            for alliance in ['red', 'blue']:
                row_data[alliance.capitalize() + " force played"] = match['score_breakdown'][alliance][
                    'vaultForcePlayed']
                row_data[alliance.capitalize() + " force total"] = match['score_breakdown'][alliance]['vaultForceTotal']
                row_data[alliance.capitalize() + " levitate played"] = match['score_breakdown'][alliance][
                    'vaultLevitatePlayed']
                row_data[alliance.capitalize() + " levitate total"] = match['score_breakdown'][alliance][
                    'vaultLevitateTotal']
                row_data[alliance.capitalize() + " boost played"] = match['score_breakdown'][alliance][
                    'vaultBoostPlayed']
                row_data[alliance.capitalize() + " boost total"] = match['score_breakdown'][alliance]['vaultBoostTotal']
            yield row_data

    yield {"Match": 0,
           "Red force played": 0,
           "Red force total": 0,
           "Red levitate played": 0,
           "Red levitate total": 0,
           "Red boost played": 0,
           "Red boost total": 0,
           "Blue force played": 0,
           "Blue force total": 0,
           "Blue levitate played": 0,
           "Blue levitate total": 0,
           "Blue boost played": 0,
           "Blue boost total": 0}


def compute_table(manager):
    return pd.DataFrame(row_data_generator(manager))[LABELS]
