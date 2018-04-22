import pandas as pd

TITLE_NAME = "Raw Data"
SOURCE_NAME = "raw_data"
LABELS = ["Team Number",
          "Alliance",
          "Match Number",
          "Auto Line",
          "Exchange Auto Successes",
          "Switch Auto Successes",
          "Scale Auto Successes",
          "Exchange Auto Attempts",
          "Switch Auto Attempts",
          "Scale Auto Attempts",
          "Exchange",
          "Alliance Switch",
          "Opponent Switch",
          "Scale",
          "Times Cube Dropped",
          "Exchange Placement",
          "Switch Placement",
          "Scale Placement",
          "Intake Speed",
          "Intake Consistency",
          "Defense",
          "Opponents Switch",
          "Levitate",
          "Force",
          "Boost",
          "Platform",
          "Climb",
          "Climb Speed",
          "Attachment Speed"]


def row_data_generator(manager):
    for entry in manager.entries:
        if entry.board.alliance() != "N":
            row_data = {
                "Team Number": entry.team,
                "Alliance": entry.board.alliance(),
                "Match Number": entry.match,

                "Auto Line": entry.final_value("Auto line", default=0),

                "Exchange Auto Attempt": entry.count("Auto exchange attempt"),
                "Switch Auto Attempt": entry.count("Auto switch attempt"),
                "Scale Auto Attempt": entry.count("Auto scale attempt"),

                "Exchange Auto Successes": entry.count("Auto exchange"),
                "Switch Auto Successes": entry.count("Auto switch"),
                "Scale Auto Successes": entry.count("Auto scale"),

                "Exchange": entry.count("Tele exchange"),
                "Alliance Switch": entry.count("Tele alliance switch"),
                "Opponent Switch": entry.count("Tele  opponent switch"),
                "Scale": entry.count("Tele scale"),

                "Times Cube Dropped": (entry.count("Tele intake") -
                                       entry.count("Tele exchange") -
                                       entry.count("Tele alliance switch") -
                                       entry.count("Tele opponent switch") -
                                       entry.count("Tele scale")),

                "Exchange Placement": entry.final_value("Exchange speed", default=0),
                "Switch Placement": entry.final_value("Switch speed", default=0),
                "Scale Placement": entry.final_value("Scale speed", default=0),

                "Intake Speed": entry.final_value("Intake speed", default=0),
                "Intake Consistency": entry.final_value("Intake consistency", default=0),

                # TODO make this total time spent defending
                "Defense": (2 if entry.count("Defense") != 0 else 0),

                "Levitate": "",
                "Force": "",
                "Boost": "",

                "Platform": entry.final_value("Platform", default=0),
                "Climb": entry.final_value("Climb", default=0),
                "Climb Speed": entry.final_value("Climb speed", default=0) // 2,
                "Attachment Speed": entry.final_value("Attachment speed", default=0) // 2
            }

            # Fix times cube dropped

            if (row_data["Exchange Auto"] + row_data["Switch Auto"] + row_data["Scale Auto"]) > 1:
                row_data["Times Cube Dropped"] += 1

            yield row_data


def compute_table(manager):
    return pd.DataFrame(row_data_generator(manager))[LABELS]
