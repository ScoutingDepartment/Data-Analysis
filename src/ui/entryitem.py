from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class EntryInfoListItemWidget(QWidget):

    def __init__(self, parent, entry_info):
        super().__init__(parent, flags=Qt.Widget)

        self.db_index = int(entry_info["Index"])

        self.match = entry_info["Match"]
        self.team = entry_info["Team"]
        self.name = entry_info["Name"]
        self.board_name = entry_info["Board"]

        self.match_label = QLabel(str(self.match))
        self.team_label = QLabel(str(self.team))
        self.name_label = QLabel(str(self.name))
        self.board_label = QLabel(str(self.board_name))

        layout = QHBoxLayout()
        layout.addWidget(self.match_label)
        layout.addWidget(self.team_label)
        layout.addWidget(self.name_label)
        layout.addWidget(self.board_label)

        self.setLayout(layout)

        self.setMinimumSize(200, 30)
        self.resize(200, 30)
        self.show()
