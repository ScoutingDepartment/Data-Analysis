import pandas as pd

TITLE_NAME = ""
SOURCE_NAME = ""
LABELS = ["Team Number",
          "Alliance",
          "Match Number",
          "Auto Line",
          "Exchange Auto",
          "Switch Auto",
          "Scale Auto",
          "Exchange",
          "Switch",
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


def compute_table(manager, result_table: "pd.DataFrame") -> None:
    def combine_autos(attempt, success):
        if success == 0:
            if attempt == 0:
                return 0
            return 1
        return 2

    result_table = result_table.iloc[0:0]  # clears the table

    row_count = 0

    for entry in manager.entries:
        if entry.board.alliance() != "N":  # checks that the entry is not for power ups
            result_table.loc[row_count] = {

                "Team Number": entry.team,
                "Alliance": entry.board.alliance(),
                "Match Number": entry.match,

                "Auto Line": entry.final_value("Auto line", default=0),

                "Exchange Auto": combine_autos(entry.count("Auto exchange attempt"), entry.count("Auto exchange")),
                "Switch Auto": combine_autos(entry.count("Auto switch attempt"), entry.count("Auto switch")),
                "Scale Auto": combine_autos(entry.count("Auto scale attempt"), entry.count("Auto scale")),

                "Exchange": entry.count("Tele exchange"),
                "Switch": (entry.count("Tele alliance switch") +
                           entry.count("Tele opponent switch")),
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

                "Defense": (2 if entry.count("Defense") != 0 else 0),
                "Opponents Switch": (1 if entry.count("Tele opponent switch") != 0 else 0),

                "Levitate": "",
                "Force": "",
                "Boost": "",

                "Platform": entry.final_value("Platform", default=0),
                "Climb": entry.final_value("Climb", default=0),
                "Climb Speed": entry.final_value("Climb speed", default=0) // 2,
                "Attachment Speed": entry.final_value("Attachment speed", default=0) // 2
            }

            row_count += 1
