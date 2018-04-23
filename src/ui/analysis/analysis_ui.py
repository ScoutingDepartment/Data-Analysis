import sys

import numpy as np
import pandas as pd
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QListWidget, QListWidgetItem, QAction, QMenu, QDesktopWidget, QApplication

from src.ui.analysis.analysis_table import AnalysisTable


class AnalysisUI(QMainWindow):
    def __init__(self):
        super().__init__(flags=Qt.Window)

        self.setWindowTitle("Analysis Tables")

        self.tables_nav = QListWidget(self)
        for i in range(5):
            i1 = QListWidgetItem("Table %d" % (i + 1))
            self.tables_nav.addItem(i1)

        self.table_content = AnalysisTable(self)
        self.table_content.update_contents("Hi", pd.DataFrame(np.arange(10000).reshape(100, 100)))

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
            "Analysis": [
                ["Calculate with TBA", None, Qt.CTRL | Qt.Key_T],
                ["Calculate without TBA", None, Qt.CTRL | Qt.ALT | Qt.Key_T],
            ],
            "Window": [
                ["Open Table in New Window", None, Qt.ALT | Qt.Key_0],
                ["Open Table in Excel", None, Qt.CTRL | Qt.ALT | Qt.Key_0]
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
        self.setMinimumSize(600, 400)

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        hardcoded_layout = [
        ]

        for widget, x, y, width, height in hardcoded_layout:
            widget.move(x, y)
            widget.setFixedSize(width, height)

    def resizeEvent(self, event):
        super().resizeEvent(event)

        top = self.menuBar().height()  # get the reduced height
        w_height = self.height()
        w_width = self.width()

        self.tables_nav.move(4, top + 4)
        self.tables_nav.resize(196, w_height - top - 8)

        self.table_content.move(200, top + 4)
        self.table_content.resize(w_width - 204, w_height - top - 8)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("../../../assets/app-icon.png"))
    win = AnalysisUI()
    sys.exit(app.exec_())
