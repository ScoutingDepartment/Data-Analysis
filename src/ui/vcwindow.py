import random
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from src.ui.entrydetails import EntryDetailsWidget
from src.ui.entryitem import EntryInfoListItemWidget


class VerificationWindow(QMainWindow):
    """The base interface for verification center"""

    def __init__(self):
        super().__init__(parent=None, flags=Qt.Window)

        self.setWindowTitle("Verification Center")

        self.filtered_entries = QListWidget(self)

        self.details = EntryDetailsWidget(self, True)
        self.original_details = EntryDetailsWidget(self, False)

        (
            self.log,
            self.filter_team_number,
            self.filter_match_number,
            self.filter_scout_name,
            self.current_entry_match_number,
            self.current_entry_team_number,
            self.current_entry_scout_name,
            self.current_entry_time_started,
            self.current_entry_last_time_edited,
            self.current_entry_board,
            self.add_item_in_current_entry,
            self.remove_item_in_current_entry
        ) = (QLineEdit(self) for _ in range(12))

        self.current_entry_comments = QTextEdit(self)  # Use QTextEdit instead to have multiple lines

        self.setup_menus()
        self.setup_event_handlers()
        self.setup_view_states()
        self.setup_styles()
        self.setup_layouts()

        self.update_filtered_entries()

        self.show()

    def read(self):
        self.details.read()

    def setup_event_handlers(self):
        self.filtered_entries.itemSelectionChanged.connect(self.on_entry_selected)
        self.filter_team_number.textEdited.connect(self.on_filter_edited)
        self.filter_match_number.textEdited.connect(self.on_filter_edited)
        self.filter_scout_name.textEdited.connect(self.on_filter_edited)
        self.add_item_in_current_entry.textEdited.connect(self.on_add_item_clicked)
        self.remove_item_in_current_entry.textEdited.connect(self.on_remove_item_clicked)

    def setup_view_states(self):
        self.log.setEnabled(False)
        self.current_entry_match_number.setEnabled(False)
        self.current_entry_team_number.setEnabled(False)
        self.current_entry_scout_name.setEnabled(False)
        self.current_entry_time_started.setEnabled(False)
        self.current_entry_last_time_edited.setEnabled(False)
        self.current_entry_board.setEnabled(False)

    def setup_styles(self):
        self.current_entry_comments.setStyleSheet("QTextEdit{font-size:18px}")
        for w in (self.log,
                  self.filter_team_number,
                  self.filter_match_number,
                  self.filter_scout_name,
                  self.current_entry_match_number,
                  self.current_entry_team_number,
                  self.current_entry_scout_name,
                  self.current_entry_time_started):
            w.setStyleSheet("QLineEdit{font-size:14px}")

    def setup_layouts(self):
        self.resize(1300, 600)

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        hardcoded_layout = [
            (self.log, 10, 30, 1280, 20),

            (self.filter_match_number, 70, 60, 50, 30),
            (self.filter_team_number, 10, 60, 50, 30),
            (self.filter_scout_name, 130, 60, 100, 30),
            (self.filtered_entries, 10, 100, 300, 470),

            (self.current_entry_comments, 320, 60, 970, 100),
            (self.current_entry_match_number, 320, 170, 100, 30),
            (self.current_entry_team_number, 430, 170, 100, 30),
            (self.current_entry_scout_name, 540, 170, 100, 30),
            (self.current_entry_time_started, 650, 170, 150, 30),
            (self.current_entry_last_time_edited, 810, 170, 150, 30),
            (self.current_entry_board, 970, 170, 100, 30),
            (self.add_item_in_current_entry, 810, 210, 30, 30),
            (self.remove_item_in_current_entry, 810, 290, 30, 30),

            (self.details, 310, 200, 500, 380),
            (self.original_details, 840, 200, 500, 380)
        ]

        for widget, x, y, width, height in hardcoded_layout:
            widget.move(x, y)
            widget.setFixedSize(width, height)

    def add_entry_item(self, index, data, finder):
        custom_widget = EntryInfoListItemWidget(parent=self.filtered_entries,
                                                index=index,
                                                entry_info=data,
                                                board_finder=finder)

        widget_item = QListWidgetItem(self.filtered_entries)
        widget_item.setSizeHint(custom_widget.sizeHint())
        self.filtered_entries.addItem(widget_item)
        self.filtered_entries.setItemWidget(widget_item, custom_widget)

    def update_filtered_entries(self):
        for i in range(100):
            self.add_entry_item(1, {"Match": i // 6 + 1,
                                    "Team": random.randint(1, 7999),
                                    "Index": i,
                                    "Board": "",
                                    "Edited": "",
                                    "Name": "Yu"}, None)

    def setup_menus(self):
        """Set up the menus that is part of the UI"""

        def create_menu_action(name, callback=None, shortcut=None, role=None):

            action = QAction(name, self)
            if callback is not None:
                action.triggered.connect(callback)
            if shortcut is not None:
                action.setShortcut(shortcut)
            if role is not None:
                action.setMenuRole(role)
            return action

        menus = {
            "Data": [
                ["Update", self.on_update, Qt.CTRL | Qt.Key_R],
                ["Save", self.on_save, Qt.CTRL | Qt.Key_S]
            ]
        }

        menu_bar = self.menuBar()

        for menu_name in menus.keys():
            menu_view = QMenu(menu_name, self)

            for menu_item in menus[menu_name]:
                menu_action = create_menu_action(*menu_item)
                print(menu_action)
                menu_view.addAction(menu_action)

            menu_bar.addMenu(menu_view)

    def on_entry_selected(self):
        pass

    def on_update(self):
        pass

    def on_save(self):
        pass

    def on_filter_edited(self):
        pass

    def on_remove_item_clicked(self):
        print("2")

    def on_add_item_clicked(self):
        self.details.add_row()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("../../assets/app-icon.png"))
    win = VerificationWindow()
    sys.exit(app.exec_())
