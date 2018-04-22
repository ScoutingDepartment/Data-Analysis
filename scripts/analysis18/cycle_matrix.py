import pandas as pd
import numpy as np

TITLE_NAME = "Cycle Matrix"

def calc_prs(data, times = []):
    """

    :param data: 2d list where d1 separates by match and d2 separates by Scale Switch Exchange respectively
    :return: List of Scale Switch Exchange cycle speed approximations respectively
    """
    if times == []:
        times = tuple([135] * len(data))
    prs = np.linalg.lstsq(data, times, rcond= 1)
    return prs[0]

def get_values_by_team(manager):
    data_by_team = {}
    for entry in manager.entries:
        if entry.team in data_by_team.keys():
            data_by_team[entry.team].append((entry.count("Tele exchange"), entry.count("Tele alliance switch") + entry.count("Tele opponent switch"), entry.count("Tele scale")))
        else:
            data_by_team[entry.team] = [((entry.count("Tele exchange"), entry.count("Tele alliance switch") + entry.count("Tele opponent switch"), entry.count("Tele scale")))]
    return data_by_team

def calc_speeds(manager):
    final_data_by_team = {}
    data = get_values_by_team(manager)
    for team in data.keys():
        final_data_by_team[team] = calc_prs(data[team])
    return final_data_by_team


def compute_table(manager):
    final = calc_speeds(manager)
    return final
