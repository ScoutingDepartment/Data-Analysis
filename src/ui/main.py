import os
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *

from src.ui.analysis.analysis import AnalysisCenter
from src.ui.verification.vc import VerificationCenter

CONFIG_PATH = "paths.config"


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__(flags=Qt.Window | Qt.MSWindowsFixedSizeDialogHint)

        self.vc = None
        self.analysis = None

        self.db_path = ""
        self.scans_path = ""
        self.boards_path = ""
        self.scripts_path = ""
        self.tba_key = ""

        self.edit_scans = QLabel()
        self.btn_browse_scans = QPushButton("Browse")

        self.edit_boards = QLabel()
        self.btn_browse_boards = QPushButton("Browse")

        self.edit_db = QLabel()
        self.btn_db_new = QPushButton("New")
        self.btn_db_existing = QPushButton("Existing")

        self.edit_scripts = QLabel()
        self.btn_scripts = QPushButton("Browse")

        self.edit_tba = QLineEdit()
        self.edit_tables = QLineEdit()
        self.edit_tba_event = QLineEdit()

        self.btn_vc = QPushButton("Verification Center")
        self.btn_calc_table = QPushButton("Analysis")

        self.setup_layouts()
        self.setup_styles()
        self.setup_events()
        self.setup_config()

        self.setWindowTitle("Scouting Data Analysis/Verification V1 Setup")

        self.show()

    def setup_layouts(self):
        self.setFixedSize(640, 320)
        self.move(0, 0)

        grid = QGridLayout()
        grid.setSpacing(5)

        grid_widgets = [
            (QLabel("Scans:"), (0, 0)),
            (self.edit_scans, (0, 1, 1, 5)),
            (self.btn_browse_scans, (0, 6)),

            (QLabel("Boards:"), (1, 0)),
            (self.edit_boards, (1, 1, 1, 5)),
            (self.btn_browse_boards, (1, 6)),

            (QLabel(".Warp7:"), (2, 0)),
            (self.edit_db, (2, 1, 1, 4)),
            (self.btn_db_new, (2, 5)),
            (self.btn_db_existing, (2, 6)),

            (QLabel("Scripts:"), (3, 0)),
            (self.edit_scripts, (3, 1, 1, 5)),
            (self.btn_scripts, (3, 6)),

            (QLabel("Tables:"), (4, 0)),
            (self.edit_tables, (4, 1, 1, 6)),

            (QLabel("TBA key:"), (5, 0)),
            (self.edit_tba, (5, 1, 1, 6)),

            (QLabel("TBA event:"), (6, 0)),
            (self.edit_tba_event, (6, 1, 1, 6)),

            (self.btn_vc, (7, 4, 1, 3)),
            (self.btn_calc_table, (7, 1, 1, 3)),
        ]

        for widget, grid_position in grid_widgets:
            grid.addWidget(widget, *grid_position)

        grid_container = QWidget(self, flags=Qt.Widget)
        grid_container.setLayout(grid)

        self.setCentralWidget(grid_container)

    def setup_styles(self):
        s = "QPushButton{color:#1e2d4a; font-weight:bold; font-size: 18px}"
        self.btn_vc.setStyleSheet(s)
        self.btn_calc_table.setStyleSheet(s)

    def setup_events(self):
        self.btn_browse_scans.clicked.connect(self.on_browse_scans_clicked)
        self.btn_browse_boards.clicked.connect(self.on_browse_boards_clicked)
        self.btn_db_new.clicked.connect(self.on_new_database_clicked)
        self.btn_db_existing.clicked.connect(self.on_exist_database_clicked)
        self.btn_vc.clicked.connect(self.on_open_vc_clicked)
        self.btn_calc_table.clicked.connect(self.on_open_calc_table_clicked)

    def setup_config(self):
        if os.path.exists(CONFIG_PATH):
            config_path = open(CONFIG_PATH, "r")
            lines = config_path.readlines()
            self.db_path = lines[0].strip()
            self.scans_path = lines[1].strip()
            self.boards_path = lines[2].strip()
            config_path.close()

        self.edit_scans.setText(self.scans_path)
        self.edit_boards.setText(self.boards_path)
        self.edit_db.setText(self.db_path)
        self.btn_scripts.setEnabled(False)

    def on_browse_scans_clicked(self):
        path_input = QFileDialog.getExistingDirectory(self,
                                                      "Open Scans Folder",
                                                      "",
                                                      QFileDialog.ShowDirsOnly)
        if path_input:
            self.scans_path = path_input
        self.edit_scans.setText(self.scans_path)

    def on_browse_boards_clicked(self):
        path_input = QFileDialog.getExistingDirectory(self,
                                                      "Open Boards Folder",
                                                      "",
                                                      QFileDialog.ShowDirsOnly)
        if path_input:
            self.boards_path = path_input
        self.edit_boards.setText(self.boards_path)

    def on_new_database_clicked(self):
        path_input = QFileDialog.getSaveFileName(self,
                                                 "Save New Database",
                                                 "",
                                                 filter="(*.warp7)")
        if path_input[0]:
            self.db_path = path_input[0]
        self.edit_db.setText(self.db_path)

    def on_exist_database_clicked(self):
        path_input = QFileDialog.getOpenFileName(self,
                                                 "Open Database",
                                                 filter="(*.warp7)")
        if path_input[0]:
            self.db_path = path_input[0]
        self.edit_db.setText(self.db_path)

    def on_open_vc_clicked(self):
        paths = (self.db_path, self.scans_path, self.boards_path)

        if all(paths):
            config_file = open(CONFIG_PATH, "w")
            config_file.writelines("\n".join(paths))
            config_file.close()

            self.vc = VerificationCenter(*paths)
        else:
            QMessageBox.warning(self, "Cannot Open Verification Center",
                                "Not all of the fields are filled in")

    def on_open_calc_table_clicked(self):
        self.analysis = AnalysisCenter()

    def closeEvent(self, event):
        if self.vc is not None:
            self.vc.close()
        event.accept()


def run_app():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(os.path.join(os.getcwd(), "assets/app-icon.png")))
    _ = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    os.chdir("../../")
    run_app()
