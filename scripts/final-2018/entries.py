import pandas as pd
import numpy as np

TITLE_NAME = "Entries"
SOURCE_NAME = "entries"
LABELS = [
    "Scout",
    "Team number",

    "Alliance",
    "Driver station number",
    "Match key",
    "Match",

    "Scale assignment",
    "Switch assignment",

    "Start position",
    "Auto line",
    "Auto run TBA",
    "Scale auto successes",
    "Switch auto successes",
    "Scale auto attempts",
    "Switch auto attempts",
    "Auto action 1",
    "Auto action 2",
    "Auto action 3",
    "Auto action 4",
    "Auto action 5",

    "Scale",
    "Alliance switch",
    "Opponent switch",
    "Exchange",
    "Times cube dropped",
    "Defense time",

    "Climbed",
    "Climbing TBA",
    "Climb time",
    "Relative climb time",
    "Climb attempts",
    "Climb failed",
    "Lifted",
    "Lifting"
    "Endgame type",

    "Average scale time",
    "Average alliance switch time",
    "Average opponent switch time",
    "Average exchange time",
    "Average intake time",
    "Std scale time",
    "Std alliance switch time",
    "Std opponent switch time",
    "Std exchange time",
    "Std intake time",

    "Objective",
    "Comments"
]


def raw_data_app(manager, entry):
    START_POSITIONS = [
        "None",
        "Left",
        "Center",
        "Right"
    ]

    ENDGAME_TYPES = [
        "None",
        "Platform",
        "Failed Climb",
        "Single Climb",
        "Double Climb",
        "Single Climb, Lifting Another Robot",
        "Lifted by Another Robot"
    ]

    OBJECTIVES = [
        "Select",
        "Scale",
        "Alliance Switch",
        "Opponent Switch",
        "Exchange",
        "Defense",
        "Support"
    ]

    defense_presses = entry.look("Defense")
    if len(defense_presses) == 0:
        defense_time = 0
    else:
        defense_pairs = []
        start = True
        for index, value in enumerate(defense_presses):
            if start:
                defense_pairs.append([value])
            else:
                defense_pairs[int((index - 1) / 2)].append(value)
            start = not start
        if defense_pairs:
            if len(defense_pairs[-1]) == 1:
                defense_pairs[-1].append(150)
            defence_values = []
            for i in defense_pairs:
                defence_values.append(i[1] - i[0])
            defense_time = sum(defence_values)
        else:
            defense_time = 0

    platform_presses = entry.look("Platform timer")
    platform_pairs = []
    start = True

    for index, value in enumerate(platform_presses):
        if start:
            platform_pairs.append([value])
        else:
            platform_pairs[int((index - 1) / 2)].append(value)
        start = not start

    platform_attempts = len(platform_pairs)

    if platform_pairs and len(platform_pairs[-1]) == 1:
        platform_pairs[-1].append(150)
        last_platform_duration = 150 - platform_pairs[-1][0]
        platform_attempts -= 1
    else:
        last_platform_duration = 0

    total_platform_duration = sum(map(lambda x: x[1] - x[0], platform_pairs))

    climbed_presses = entry.look("Climbed timer")
    climbed_pairs = []
    start = True

    for index, value in enumerate(climbed_presses):
        if start:
            climbed_pairs.append([value])
        else:
            climbed_pairs[int((index - 1) / 2)].append(value)
        start = not start

    climb_attempts = len(climbed_pairs)

    if climbed_pairs and len(climbed_pairs[-1]) == 1:
        climbed_pairs[-1].append(150)
        last_climbed_duration = 150 - climbed_pairs[-1][0]
        climb_attempts -= 1
    else:
        last_climbed_duration = 0  # No climb

    total_climbed_duration = sum(map(lambda x: x[1] - x[0], climbed_pairs))

    row_data = {
        "Scout": entry.name,
        "Team number": entry.team,
        "Alliance": entry.board.alliance(),
        "Match key": manager.tba_event + "_qm" + str(entry.match),
        "Match number": entry.match,

        "Start position": START_POSITIONS[entry.final_value("Start position", 0)],
        "Auto line": entry.final_value("Auto line", default=0),

        "Switch auto successes": entry.count("Auto switch"),
        "Scale auto successes": entry.count("Auto scale"),

        "Switch auto attempts": entry.count("Auto switch attempt"),
        "Scale auto attempts": entry.count("Auto scale attempt"),

        "Exchange": entry.count("Tele exchange"),
        "Alliance switch": entry.count("Tele alliance switch"),
        "Opponent switch": entry.count("Tele opponent switch"),
        "Scale": entry.count("Tele scale"),

        "Times cube dropped": (entry.count("Tele intake") -
                               entry.count("Tele exchange") -
                               entry.count("Tele alliance switch") -
                               entry.count("Tele opponent switch") -
                               entry.count("Tele scale")),

        "Defense time": defense_time,
        "Endgame type": ENDGAME_TYPES[entry.final_value("Endgame type", 0)],

        "Total platform duration": total_platform_duration,
        "Last platform duration": last_platform_duration,
        "Platform attempts": platform_attempts,

        "Total climbed duration": total_climbed_duration,
        "Last climbed duration": last_climbed_duration,
        "Climb attempts": climb_attempts,

        "Relative climb time": last_platform_duration - last_climbed_duration,

        "Objective": OBJECTIVES[entry.final_value("Objective", 0)],
        "Comments": entry.comments
    }

    # Fix times cube dropped

    total_auto = ("Switch auto successes",
                  "Scale auto successes",
                  "Switch auto attempts",
                  "Scale auto attempts",)

    if sum(row_data[auto_data] for auto_data in total_auto) > 1:
        row_data["Times cube dropped"] += 1

    return row_data


def auto(manager, entry):
    auto_data_points = ["Auto scale", "Auto switch", "Auto scale attempt", "Auto switch attempt"]

    times = {i: [] for i in auto_data_points}

    actions = []
    for data_point in auto_data_points:
        for occurrence_time in entry.look(data_point):
            times[data_point].append(occurrence_time)
            actions.append((occurrence_time, data_point))

    actions = sorted(actions, key=lambda x: x[0])  # sort by the first item in tuple

    num_actions = len(actions)
    action_list = []
    for i in range(5):
        if i < num_actions:
            action_list.append(actions[i][1])
        else:
            action_list.append("None")

    scale_auto_successes = entry.count("Auto scale")
    switch_auto_successes = entry.count("Auto switch")
    scale_auto_attempts = entry.count("Auto scale attempt")
    switch_auto_attempts = entry.count("Auto switch attempt")

    starting_pos = entry.final_value("Start position", default=0)
    starting_pos_str = ["None", "Left", "Center", "Right"][starting_pos]

    if manager.tba_available:
        plate_assignments = manager.tba.match(key='2018dar_qm49')['score_breakdown']['red']['tba_gameData']
        if entry.board.alliance() == "R":
            scale_assignment = plate_assignments[1]
            switch_assignment = plate_assignments[0]
        else:
            for i, v in enumerate(plate_assignments):
                if v == "R":
                    plate_assignments[i] = "L"
                elif v == "L":
                    plate_assignments[i] = "R"

            plate_assignments = plate_assignments
            scale_assignment = plate_assignments[1]
            switch_assignment = plate_assignments[0]

        row_data = {
            "Team": entry.team,
            "Match": entry.match,
            "Start position": starting_pos_str,
            "Scale assignment": scale_assignment,
            "Switch assignment": switch_assignment,
            "Scale auto successes": scale_auto_successes,
            "Switch auto successes": switch_auto_successes,
            "Scale auto fails": scale_auto_successes,
            "Switch auto fails": switch_auto_successes,
            "Auto action 1": action_list[0],
            "Auto action 2": action_list[1],
            "Auto action 3": action_list[2],
            "Auto action 4": action_list[3],
            "Auto action 5": action_list[4]
        }
    else:
        row_data = {
            "Team": entry.team,
            "Match": entry.match,
            "Start position": starting_pos_str,
            "Scale assignment": "",
            "Switch assignment": "",
            "Scale auto successes": scale_auto_successes,
            "Switch auto successes": switch_auto_successes,
            "Scale auto attempts": scale_auto_successes,
            "Switch auto attempts": switch_auto_successes,
            "Auto action 1": action_list[0],
            "Auto action 2": action_list[1],
            "Auto action 3": action_list[2],
            "Auto action 4": action_list[3],
            "Auto action 5": action_list[4]
        }
    return row_data


def speeds(manager, entry):
    def n_avg(arr):
        if len(arr) > 0:
            return sum(arr) / len(arr)
        return np.nan

    def n_std(arr):
        if len(arr) > 1:
            return np.std(arr, ddof=1)
        return np.nan

    tracked_data_types = ['Tele scale',
                          'Tele exchange',
                          'Tele opponent switch',
                          'Tele intake',
                          'Tele alliance switch']

    time_series = [None for _ in range(150)]
    for data_type in tracked_data_types:
        for occurrence_time in entry.look(data_type):
            time_series[occurrence_time - 1] = data_type

    first_intake_ignored = False
    robot_doing_outtake = True
    current_cycle_time = 1

    scale = []
    exchange = []
    alliance_switch = []
    opponent_switch = []
    intake = []

    for data_at_second in time_series:

        if first_intake_ignored:

            if data_at_second == "Tele intake" and robot_doing_outtake:
                intake.append(current_cycle_time)
                current_cycle_time = 1
                robot_doing_outtake = False

            elif data_at_second == 'Tele scale' and not robot_doing_outtake:
                scale.append(current_cycle_time)
                current_cycle_time = 1
                robot_doing_outtake = True

            elif data_at_second == 'Tele exchange' and not robot_doing_outtake:
                exchange.append(current_cycle_time)
                current_cycle_time = 1
                robot_doing_outtake = True

            elif data_at_second == 'Tele opponent switch' and not robot_doing_outtake:
                opponent_switch.append(current_cycle_time)
                current_cycle_time = 1
                robot_doing_outtake = True

            elif data_at_second == 'Tele alliance switch' and not robot_doing_outtake:
                alliance_switch.append(current_cycle_time)
                current_cycle_time = 1
                robot_doing_outtake = True

            else:
                current_cycle_time += 1

        if data_at_second and data_at_second != "Tele intake" and not first_intake_ignored:
            first_intake_ignored = True

    return {
        "Team": entry.team,
        "Match": entry.match,
        "Alliance": entry.board.alliance(),
        "Average scale time": n_avg(scale),
        "Average alliance switch time": n_avg(alliance_switch),
        "Average opponent switch time": n_avg(opponent_switch),
        "Average exchange time": n_avg(exchange),
        "Average intake time": n_avg(intake),
        "Std scale time": n_std(scale),
        "Std alliance switch time": n_std(alliance_switch),
        "Std opponent switch time": n_std(opponent_switch),
        "Std exchange time": n_std(exchange),
        "Std intake time": n_std(intake)
    }


def climb(manager, entry):
    row_data = {}

    climbed_look = entry.look("Climbed timer")

    if len(climbed_look) % 2 == 1:
        if entry.look("Platform timer") != []:
            row_data["Relative climb time"] = max(climbed_look) - max(entry.look("Platform timer"))
        else:
            row_data["Relative climb time"] = np.nan
        row_data["Climb time"] = max(climbed_look)
    else:
        row_data["Relative climb time"] = np.nan
        row_data["Climb time"] = np.nan

    return {"Team": entry.team,
            "Match": entry.match,
            "Climbed": len(climbed_look) % 2,
            "Climb time": row_data["Climb time"],
            "Relative climb time": row_data["Relative climb time"],
            "Climb failed": int(entry.final_value("Endgame type") == 2),
            "Lifted": int(entry.final_value("Endgame type") == 6),
            "Lifting": int(entry.final_value("Endgame type") == 5)}


def wrong_data(manager, entry):
    outtakes = [
        'Tele scale',
        'Tele exchange',
        'Tele opponent switch',
        'Tele alliance switch'
    ]

    time_series = [None for _ in range(150)]
    for data_type in outtakes:
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

    return {"Scout": entry.name,
            "Team": entry.team,
            "Match": entry.match,
            "Alliance": entry.board.alliance(),
            "Double outtakes": double_outtakes
            }


def tba_wrong_data(manager, entry):
    match_key = str(manager.tba_event) + "_qm" + str(entry.match)

    if entry.board.alliance().lower() == "r":
        alliance = "red"
    elif entry.board.alliance().lower() == "b":
        alliance = "blue"
    else:
        alliance = "unknown"

    for match in manager.tba_matches:
        if match['key'] == match_key:
            tba_match = match

            alliance_teams = tba_match['alliances'][alliance]["team_keys"]
            if "frc" + str(entry.team) in alliance_teams:
                tba_robot_number = alliance_teams.index("frc" + str(entry.team)) + 1
            else:
                continue

            tba_climbed = tba_match['score_breakdown'][alliance][
                              "endgameRobot" + str(tba_robot_number)] == "Climbing"
            tba_auto_line = tba_match['score_breakdown'][alliance][
                                "autoRobot" + str(tba_robot_number)] == "AutoRun"

            climbed_times = entry.look("Climbed timer")
            climbed = False
            if len(climbed_times) % 2 == 1:
                climbed = True

    return {"Scout": entry.name,
            "Team": entry.team,
            "Match": entry.match,
            "Alliance": entry.alliance,
            "Wrong auto line": not (climbed == tba_auto_line),
            "Wrong climb": not climbed == tba_climbed
            }


def tba_tam(manager, entry):
    match_key = manager.tba_event + "_qm" + str(entry.match)

    ds_number = ''
    auto_run = ''
    climbing = ''
    if manager.tba_available:
        tba = manager.tba

        i = [manager.tba_event + "_qm" + entry.match, entry.team]

        match = tba.match(match_key)

        if 'frc' + str(entry.team) in match['alliances']['red']['team_keys']:
            ds_number = match['alliances']['red']['team_keys'].index('frc' + str(i[1])) + 1
            auto_run = int(match['score_breakdown']['red']['autoRobot' + str(ds_number)] == 'AutoRun')
            climbing = int(match['score_breakdown']['red']['endgameRobot' + str(ds_number)] == 'Climbing')
            ds_number = 'R' + ds_number
        elif 'frc' + str(entry.team) in match['alliances']['blue']['team_keys']:
            ds_number = match['alliances']['blue']['team_keys'].index('frc' + str(i[1])) + 1
            auto_run = int(match['score_breakdown']['blue']['autoRobot' + str(ds_number)] == 'AutoRun')
            climbing = int(match['score_breakdown']['blue']['endgameRobot' + str(ds_number)] == 'Climbing')
            ds_number = 'B' + ds_number

    return {
        "Team": entry.team,
        "Match": entry.match,
        "Alliance": ds_number[0],
        "Match key": match_key,
        "Driver station number": ds_number,
        "Auto line TBA": auto_run,
        "Climbing TBA": climbing
    }


def row_data_generator(manager):
    for entry in manager.entries:
        if entry.board.alliance() == "R" or entry.board.alliance() == "B":
            row_data = {
                **climb(manager, entry),
                **speeds(manager, entry),
                **auto(manager, entry),
                **raw_data_app(manager, entry)
            }

            if manager.tba_available:
                row_data.update({
                    **tba_wrong_data(manager, entry),
                    **tba_tam(manager, entry)
                })

            yield row_data


def compute_table(manager):
    return pd.DataFrame(row_data_generator(manager), columns=LABELS)[LABELS]
