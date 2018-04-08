import os
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__(flags=Qt.Window)

        self.scans_path = ""
        self.boards_path = ""
        self.db_path = ""

        grid = QGridLayout()
        grid.setSpacing(10)

        self.edit_scans = QLineEdit()
        # self.edit_scans.setEnabled(False)
        btn_browse_scans = QPushButton("Browse")
        btn_browse_scans.clicked.connect(self.on_browse_scans_clicked)

        self.edit_boards = QLineEdit()
        # self.edit_boards.setEnabled(False)
        btn_browse_boards = QPushButton("Browse")
        btn_browse_boards.clicked.connect(self.on_browse_boards_clicked)

        self.edit_db = QLineEdit()
        # self.edit_db.setEnabled(False)
        btn_db_new = QPushButton("New")
        btn_db_new.clicked.connect(self.on_new_database_clicked)
        btn_db_existing = QPushButton("Existing")
        btn_db_existing.clicked.connect(self.on_exist_database_clicked)

        btn_vc = QPushButton("Verification Center")
        btn_calc_table = QPushButton("Calculation Tables")
        btn_calc_table.setEnabled(False)
        btn_data_lookup = QPushButton("Data Lookup")
        btn_data_lookup.setEnabled(False)

        version_label = QLabel("Version 1")
        version_label.setStyleSheet("QLabel{color:#808080}")

        grid_widgets = [
            (QLabel("Scans"), (0, 0)),
            (self.edit_scans, (0, 1, 1, 3)),
            (btn_browse_scans, (0, 4)),

            (QLabel("Boards"), (1, 0)),
            (self.edit_boards, (1, 1, 1, 3)),
            (btn_browse_boards, (1, 4)),

            (QLabel(".warp7 File"), (2, 0)),
            (self.edit_db, (2, 1, 1, 2)),
            (btn_db_new, (2, 3)),
            (btn_db_existing, (2, 4)),

            (btn_vc, (3, 3, 1, 2)),
            (btn_calc_table, (4, 3, 1, 2)),
            (btn_data_lookup, (5, 3, 1, 2)),

            (version_label, (5, 0, 1, 2))
        ]

        for w, p in grid_widgets:
            grid.addWidget(w, *p)

        grid_container = QWidget(self, flags=Qt.Widget)
        grid_container.setLayout(grid)

        self.setCentralWidget(grid_container)

        # Setup window position
        self.setMaximumSize(540, 360)
        self.setMinimumSize(480, 320)
        self.setWindowTitle("Scouting Data Utilities")
        self.move(0, 0)
        self.show()

    def on_browse_scans_clicked(self):
        f = QFileDialog.getExistingDirectory(self,
                                             "Open Scans Folder",
                                             "",
                                             QFileDialog.ShowDirsOnly)
        if f:
            self.scans_path = f
        self.edit_scans.setText(self.scans_path)

    def on_browse_boards_clicked(self):
        f = QFileDialog.getExistingDirectory(self,
                                             "Open Boards Folder",
                                             "",
                                             QFileDialog.ShowDirsOnly)
        if f:
            self.boards_path = f
        self.edit_boards.setText(self.boards_path)

    def on_new_database_clicked(self):
        f = QFileDialog.getSaveFileName(self, "Save New Database", "", filter="(*.warp7)")
        if f[0]:
            self.db_path = f[0]
        self.edit_db.setText(self.db_path)

    def on_exist_database_clicked(self):
        f = QFileDialog.getOpenFileName(self, "Open Database", filter="(*.warp7)")
        if f[0]:
            self.db_path = f[0]
        self.edit_db.setText(self.db_path)


def run_app():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(os.path.join(os.getcwd(), "assets/app-icon.png")))
    _ = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    os.chdir("../../")
    run_app()
