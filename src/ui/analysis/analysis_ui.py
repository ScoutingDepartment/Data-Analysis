import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class AnalysisUI(QMainWindow):
    def __init__(self):
        super().__init__(flags=Qt.Window)

        self.setWindowTitle("Analysis Tables")

        self.setup_menus()
        self.setup_event_handlers()
        self.setup_view_states()
        self.setup_styles()
        self.setup_layouts()

        self.show()

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
            "Analysis Data": [
                ["Calculate Now", None, Qt.CTRL | Qt.Key_T],
                ["Export Tables to Excel", None, Qt.CTRL | Qt.SHIFT | Qt.Key_S]
            ],
            "Window": [
                ["Open Table in New Window"]
            ]
        }

        menu_bar = self.menuBar()

        for menu_name in menus.keys():
            menu_view = QMenu(menu_name, self)

            for menu_item in menus[menu_name]:
                menu_action = create_menu_action(*menu_item)
                menu_view.addAction(menu_action)

            menu_bar.addMenu(menu_view)

    def setup_event_handlers(self):
        pass

    def setup_view_states(self):
        pass

    def setup_styles(self):
        pass

    def setup_layouts(self):

        self.resize(1080, 720)

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        hardcoded_layout = [
        ]

        for widget, x, y, width, height in hardcoded_layout:
            widget.move(x, y)
            widget.setFixedSize(width, height)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("../../../assets/app-icon.png"))
    win = AnalysisUI()
    sys.exit(app.exec_())
