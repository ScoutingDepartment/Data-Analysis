import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
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

        self.setMinimumSize(200, 50)
        self.resize(200, 50)
        self.show()


class TestAppWindow(QMainWindow):

    def __init__(self):
        super().__init__(flags=Qt.Window)

        self.setup_entries_list()
        self.setup_menus()

        self.resize(500, 500)
        self.move(300, 300)
        self.setWindowTitle("Verification Center")
        self.show()

    def setup_entries_list(self):

        import random
        entries = QListWidget(self)

        def on_entry_clicked(item: QListWidgetItem):
            _entry_info = entries.itemWidget(item)
            self.statusBar().showMessage(str(_entry_info.team))

        for i in range(100):
            entry_info = EntryInfoListItemWidget(entries, {"Match": i // 6 + 1,
                                                           "Team": random.randint(1, 7999),
                                                           "Index": random.randint(1, 660),
                                                           "Board": random.choice(["Red 1",
                                                                                   "Red 2",
                                                                                   "Red 3",
                                                                                   "Blue 1",
                                                                                   "Blue 2",
                                                                                   "Blue 3"]),
                                                           "Name": "Yu"})
            widget_item = QListWidgetItem(entries)
            widget_item.setSizeHint(entry_info.sizeHint())
            entries.addItem(widget_item)
            entries.setItemWidget(widget_item, entry_info)

        entries.move(0, 30)

        entries.setFixedWidth(300)
        entries.setFixedHeight(400)

        entries.itemClicked.connect(on_entry_clicked)

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

        def on_open_menu_triggered():
            file_name = QFileDialog.getOpenFileName(self, "Open Database", filter="(*.warp7)")

        def on_import_csv_menu_triggered():
            file_name = QFileDialog.getExistingDirectory(self, "Open Folder", "", QFileDialog.ShowDirsOnly)

        menus = {
            "File": [
                ["Open", on_open_menu_triggered, Qt.CTRL | Qt.Key_O],
                ["Save", None, Qt.CTRL | Qt.Key_S],
                ["Save As", None, Qt.CTRL | Qt.SHIFT | Qt.Key_S],
                ["Close", self.close, Qt.CTRL | Qt.Key_W]
            ],
            "Import": [
                ["From CSV scans", on_import_csv_menu_triggered, Qt.CTRL | Qt.Key_I]
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

    def on_entries_list_selected(self, o):
        self.statusBar().showMessage("hi")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("../../assets/app-icon.png"))
    win = TestAppWindow()
    # w = EntryInfoListItemWidget(None, {"Match": 10, "Team": 20, "Board": "Red 1", "Name": "Yu"})
    sys.exit(app.exec_())
