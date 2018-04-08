import random
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from src.ui.entryitem import EntryInfoListItemWidget


class VerificationCenter(QMainWindow):

    def __init__(self):
        super().__init__(flags=Qt.Window)

        self.entries = QListWidget(self)

        self.setup_entries_list()
        self.setup_menus()

        self.resize(700, 500)

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        self.setWindowTitle("Verification Center")
        self.show()

    def setup_entries_list(self):

        def on_entry_clicked():
            selected = self.entries.selectedItems()
            if selected:
                entry = self.entries.itemWidget(selected[0])
                # self.statusBar().showMessage(str(entry.team))

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

        self.entries.move(0, 30)

        self.entries.setFixedWidth(300)
        self.entries.setFixedHeight(465)

        self.entries.itemSelectionChanged.connect(on_entry_clicked)

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
                ["Search", None, Qt.CTRL | Qt.Key_F]
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("../../assets/app-icon.png"))
    win = VerificationCenter()
    sys.exit(app.exec_())
