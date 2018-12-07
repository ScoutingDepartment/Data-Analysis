from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

from src.model.boards import Finder


class EntryInfoListItemWidget(QWidget):

    def __init__(self, parent, index, entry_info, board_finder: Finder):
        super().__init__(parent, flags=Qt.Widget)

        self.db_index = index

        self.match = entry_info["Match"]
        self.team = entry_info["Team"]
        self.name = entry_info["Name"]
        self.board_name = entry_info["Board"]

        self.team_label = QLabel(str(self.team))
        self.team_label.setFixedWidth(50)

        color = "#808080"
        if board_finder:
            board = board_finder.get_board_by_name(entry_info["Board"])
            alliance = board.alliance()
            if alliance == "red":
                color = "#FF0000"
            if alliance == "blue":
                color = "#0000FF"

        self.team_label.setStyleSheet("QLabel{font:bold; color:" + color + "}")
        self.match_label = QLabel(str(self.match))
        self.match_label.setFixedWidth(50)
        self.name_label = QLabel(str(self.name))
        self.board_label = QLabel(str(self.board_name))
        self.edited_label = QLabel("✓" if entry_info["Edited"].strip() else "")
        self.edited_label.setFixedWidth(20)
        self.edited_label.setStyleSheet("QLabel{color:#00a000}")

        layout = QHBoxLayout()
        layout.addWidget(self.team_label)
        layout.addWidget(self.match_label)
        layout.addWidget(self.name_label)
        # layout.addWidget(self.board_label)
        layout.addWidget(self.edited_label)

        self.setLayout(layout)

        self.setMinimumSize(150, 40)
        self.resize(150, 40)
        self.show()

    def update_edited_state(self, state):
        self.edited_label.setText("✓" if state else "")
