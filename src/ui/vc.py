import random
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from src.model.verification_manager import VerificationManager
from src.ui.entrydetails import EntryDetailsWidget
from src.ui.entryitem import EntryInfoListItemWidget

TEST_DATA = [['dahta type', 2, True],
             ['dahta type', 2, False],
             ['dayta type', 3, False],
             [3, 4, False]]
TEST_TYPES = ['data type', 'dahta type', 'dayta type']


class VerificationCenter(QMainWindow):
    """The verification center"""

    def __init__(self, db_path=None, csv_dir_path=None, board_dir_path=None):
        super().__init__(parent=None, flags=Qt.Window)

        if db_path and csv_dir_path and board_dir_path:
            self.manager = VerificationManager(db_path, csv_dir_path, board_dir_path)
        else:
            self.manager = None

        self.setWindowTitle("Verification Center")

        self.entries = QListWidget(self)
        self.details = EntryDetailsWidget(self, TEST_DATA, TEST_TYPES)
        self.original_details = EntryDetailsWidget(self, TEST_DATA, TEST_TYPES)

        (
            self.entry_comments,
            self.log,
            self.current_entry_match_number,
            self.current_entry_team_number,
            self.current_entry_scout_name,
            self.current_entry_time_started,
            self.filter_team_number,
            self.filter_match_number,
            self.filter_scout_name
        ) = (QLineEdit(self) for _ in range(9))

        self.setup_entries_list()
        self.setup_menus()
        self.setup_view_states()
        self.setup_layout()

        self.show()

    def setup_view_states(self):
        self.log.setEnabled(False)
        self.current_entry_match_number.setEnabled(False)
        self.current_entry_team_number.setEnabled(False)
        self.current_entry_scout_name.setEnabled(False)
        self.current_entry_time_started.setEnabled(False)

    def setup_layout(self):
        self.resize(1300, 600)

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        # layout variables

        log_top_left = (10, 30)
        log_width = 1280
        log_height = 20

        filter_match_number_top_left = (70, 60)
        filter_match_number_width = 50
        filter_match_number_height = 30

        filter_team_number_top_left = (10, 60)
        filter_team_number_width = 50
        filter_team_number_height = 30

        filter_scout_name_top_left = (130, 60)
        filter_scout_name_width = 50
        filter_scout_name_height = 30

        current_entry_match_number_top_left = (320, 170)
        current_entry_match_number_width = 100
        current_entry_match_number_height = 30

        current_entry_team_number_top_left = (430, 170)
        current_entry_team_number_width = 100
        current_entry_team_number_height = 30

        current_entry_scout_name_top_left = (540, 170)
        current_entry_scout_name_width = 100
        current_entry_scout_name_height = 30

        current_entry_time_started_top_left = (650, 170)
        current_entry_time_started_width = 100
        current_entry_time_started_height = 30

        entry_comments_top_left = (320, 60)
        entry_comments_width = 970
        entry_comments_height = 100

        filtered_entries_table_top_left = (10, 100)
        filtered_entries_table_width = 300
        filtered_entries_table_height = 470

        entry_details_table_top_left = (310, 200)
        entry_details_table_width = 500
        entry_details_table_height = 380

        original_entry_details_table_top_left = (800, 200)
        original_entry_details_table_width = 500
        original_entry_details_table_height = 380

        self.entries.move(*filtered_entries_table_top_left)
        self.entries.setFixedWidth(filtered_entries_table_width)
        self.entries.setFixedHeight(filtered_entries_table_height)

        self.entry_comments.move(*entry_comments_top_left)
        self.entry_comments.setFixedWidth(entry_comments_width)
        self.entry_comments.setFixedHeight(entry_comments_height)

        self.current_entry_match_number.move(*current_entry_match_number_top_left)
        self.current_entry_match_number.setFixedWidth(current_entry_match_number_width)
        self.current_entry_match_number.setFixedHeight(current_entry_match_number_height)

        self.current_entry_team_number.move(*current_entry_team_number_top_left)
        self.current_entry_team_number.setFixedWidth(current_entry_team_number_width)
        self.current_entry_team_number.setFixedHeight(current_entry_team_number_height)

        self.current_entry_scout_name.move(*current_entry_scout_name_top_left)
        self.current_entry_scout_name.setFixedWidth(current_entry_scout_name_width)
        self.current_entry_scout_name.setFixedHeight(current_entry_scout_name_height)

        self.current_entry_time_started.move(*current_entry_time_started_top_left)
        self.current_entry_time_started.setFixedWidth(current_entry_time_started_width)
        self.current_entry_time_started.setFixedHeight(current_entry_time_started_height)

        self.log.move(*log_top_left)
        self.log.setFixedWidth(log_width)
        self.log.setFixedHeight(log_height)

        self.filter_match_number.move(*filter_match_number_top_left)
        self.filter_match_number.setFixedWidth(filter_match_number_width)
        self.filter_match_number.setFixedHeight(filter_match_number_height)

        self.filter_team_number.move(*filter_team_number_top_left)
        self.filter_team_number.setFixedWidth(filter_team_number_width)
        self.filter_team_number.setFixedHeight(filter_team_number_height)

        self.filter_scout_name.move(*filter_scout_name_top_left)
        self.filter_scout_name.setFixedWidth(filter_scout_name_width)
        self.filter_scout_name.setFixedHeight(filter_scout_name_height)

        self.details.move(*entry_details_table_top_left)
        self.details.setFixedWidth(entry_details_table_width)
        self.details.setFixedHeight(entry_details_table_height)

        self.original_details.move(*original_entry_details_table_top_left)
        self.original_details.setFixedWidth(original_entry_details_table_width)
        self.original_details.setFixedHeight(original_entry_details_table_height)

    def setup_entries_list(self):

        for i in range(100):
            entry_info = EntryInfoListItemWidget(self.entries, {"Match": i // 6 + 1,
                                                                "Team": random.randint(1, 7999),
                                                                "Index": random.randint(1, 660),
                                                                "Board": random.choice(["Red 1",
                                                                                        "Red 2",
                                                                                        "Red 3",
                                                                                        "Blue 1",
                                                                                        "Blue 2",
                                                                                        "Blue 3"]),
                                                                "Name": "Yu"})
            widget_item = QListWidgetItem(self.entries)
            widget_item.setSizeHint(entry_info.sizeHint())
            self.entries.addItem(widget_item)
            self.entries.setItemWidget(widget_item, entry_info)

        self.entries.itemSelectionChanged.connect(self.on_entry_selected)

    def setup_menus(self):
        """
        Set up the menus that is part of the UI
        :return:
        """

        def create_menu_action(name, callback=None, shortcut=None, role=None):
            """
            :param name: The lable of the menu
            :param callback: Event handler
            :param shortcut: Keyboard shortcut
            :param role: Menu Role (for Mac OS)
            :return: A QAction that includes the callback
            """

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
                ["Update", None, Qt.CTRL | Qt.Key_R],
                ["Search", None, Qt.CTRL | Qt.Key_F],
                ["Save", None, Qt.CTRL | Qt.Key_S]
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
        selected = self.entries.selectedItems()
        if selected:
            entry = self.entries.itemWidget(selected[0])
            # TODO Use this widget here
            # self.statusBar().showMessage(str(entry.team))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("../../assets/app-icon.png"))
    win = VerificationCenter()
    sys.exit(app.exec_())
