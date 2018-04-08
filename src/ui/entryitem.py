from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class EntryInfoListItemWidget(QWidget):

    def __init__(self, parent, entry_info):
        from random import choice
        alliance = choice(["R", "B", "R", "B", "R", "B", "N"])
        super().__init__(parent, flags=Qt.Widget)

        self.db_index = int(entry_info["Index"])

        self.match = entry_info["Match"]
        self.team = entry_info["Team"]
        self.name = entry_info["Name"]
        self.board_name = entry_info["Board"]

        self.team_label = QLabel(str(self.team))
        self.team_label.setFixedWidth(50)
        color = "#808080"
        if alliance == "R":
            color = "#FF0000"
        if alliance == "B":
            color = "#0000FF"
        self.team_label.setStyleSheet("QLabel{font:bold; color:" + color + "}")
        self.match_label = QLabel(str(self.match))
        self.match_label.setFixedWidth(50)
        self.name_label = QLabel(str(self.name))
        self.board_label = QLabel(str(self.board_name))
        e = choice(["✓", ""])
        self.edited_label = QLabel(e)
        self.edited_label.setFixedWidth(20)
        self.edited_label.setStyleSheet("QLabel{color:#00a000}")

        layout = QHBoxLayout()
        layout.addWidget(self.team_label)
        layout.addWidget(self.match_label)
        layout.addWidget(self.name_label)
        # layout.addWidget(self.board_label)
        layout.addWidget(self.edited_label)

        self.setLayout(layout)

        self.setMinimumSize(150, 20)
        self.resize(150, 20)
        self.show()
