import json
import os
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *

from src.ui.analysis.analysis import AnalysisCenter
from src.ui.verification.vc import VerificationCenter

CONFIG_PATH = "config.json"


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__(flags=Qt.Window | Qt.MSWindowsFixedSizeDialogHint)

        self._config = {}  # Config dictionary
        self._vc, self._analysis = None, None  # Active reference to windows

        (self.label_scans,
         self.label_boards,
         self.label_db,
         self.label_scripts) = (QLabel(), QLabel(), QLabel(), QLabel())

        (self.edit_tables,
         self.edit_tba,
         self.edit_tba_event) = (QLineEdit(), QLineEdit(), QLineEdit())

        self.btn_browse_scans = QPushButton("Browse")
        self.btn_browse_boards = QPushButton("Browse")
        self.btn_db_new = QPushButton("New")
        self.btn_db_existing = QPushButton("Existing")
        self.btn_scripts = QPushButton("Browse")
        self.btn_analysis = QPushButton("Analysis")
        self.btn_vc = QPushButton("Verification Center")

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
            (self.label_scans, (0, 1, 1, 5)),
            (self.btn_browse_scans, (0, 6)),

            (QLabel("Boards:"), (1, 0)),
            (self.label_boards, (1, 1, 1, 5)),
            (self.btn_browse_boards, (1, 6)),

            (QLabel(".Warp7:"), (2, 0)),
            (self.label_db, (2, 1, 1, 4)),
            (self.btn_db_new, (2, 5)),
            (self.btn_db_existing, (2, 6)),

            (QLabel("Scripts:"), (3, 0)),
            (self.label_scripts, (3, 1, 1, 5)),
            (self.btn_scripts, (3, 6)),

            (QLabel("Tables:"), (4, 0)),
            (self.edit_tables, (4, 1, 1, 6)),

            (QLabel("TBA key:"), (5, 0)),
            (self.edit_tba, (5, 1, 1, 6)),

            (QLabel("TBA event:"), (6, 0)),
            (self.edit_tba_event, (6, 1, 1, 6)),

            (self.btn_analysis, (7, 1, 1, 3)),
            (self.btn_vc, (7, 4, 1, 3)),
        ]

        for widget, grid_position in grid_widgets:
            grid.addWidget(widget, *grid_position)

        grid_container = QWidget(self, flags=Qt.Widget)
        grid_container.setLayout(grid)

        self.setCentralWidget(grid_container)

    def setup_styles(self):
        s = "QPushButton{color:#1e2d4a; font-weight:bold; font-size: 18px}"
        self.btn_vc.setStyleSheet(s)
        self.btn_analysis.setStyleSheet(s)

    def setup_events(self):
        self.btn_browse_scans.clicked.connect(self.on_browse_scans_clicked)
        self.btn_browse_boards.clicked.connect(self.on_browse_boards_clicked)
        self.btn_db_new.clicked.connect(self.on_new_database_clicked)
        self.btn_db_existing.clicked.connect(self.on_exist_database_clicked)
        self.btn_scripts.clicked.connect(self.on_browse_scripts_clicked)
        self.btn_vc.clicked.connect(self.on_open_vc_clicked)
        self.btn_analysis.clicked.connect(self.on_open_analysis_clicked)

    def setup_config(self):
        if os.path.exists(CONFIG_PATH):
            config_file = open(CONFIG_PATH, "r")
            self._config = json.load(config_file)
            config_file.close()

            self.label_scans.setText(self._config["scans"])
            self.label_boards.setText(self._config["boards"])
            self.label_db.setText(self._config["db"])
            self.label_scripts.setText(self._config["scripts"])

            self.edit_tables.setText(", ".join(self._config["tables"]))
            self.edit_tba.setText(self._config["tba"])
            self.edit_tba_event.setText(self._config["tba_event"])
        else:
            self.read_config()

    def read_config(self):
        self._config = {
            "scans": self.label_scans.text(),
            "boards": self.label_boards.text(),
            "db": self.label_db.text(),
            "scripts": self.label_scripts.text(),
            "tables": list(filter(bool, map(lambda s: s.strip(), self.edit_tables.text().split(",")))),
            "tba": self.edit_tba.text(),
            "tba_event": self.edit_tba_event.text()
        }
        config_file = open(CONFIG_PATH, "w")
        json.dump(self._config, config_file, indent=4, separators=(",", ": "))
        config_file.close()

    def on_browse_scans_clicked(self):
        path_input = QFileDialog.getExistingDirectory(None,
                                                      "Open Scans Folder",
                                                      "",
                                                      QFileDialog.ShowDirsOnly)
        if path_input:
            self.label_scans.setText(path_input)

    def on_browse_boards_clicked(self):
        path_input = QFileDialog.getExistingDirectory(None,
                                                      "Open Boards Folder",
                                                      "",
                                                      QFileDialog.ShowDirsOnly)
        if path_input:
            self.label_boards.setText(path_input)

    def on_new_database_clicked(self):
        path_input = QFileDialog.getSaveFileName(None,
                                                 "Save New Database",
                                                 "",
                                                 filter="(*.warp7)")
        if path_input[0]:
            self.label_db.setText(path_input[0])

    def on_exist_database_clicked(self):
        path_input = QFileDialog.getOpenFileName(None,
                                                 "Open Database",
                                                 filter="(*.warp7)")
        if path_input[0]:
            self.label_db.setText(path_input[0])

    def on_browse_scripts_clicked(self):
        path_input = QFileDialog.getExistingDirectory(None,
                                                      "Open Scripts Folder",
                                                      "",
                                                      QFileDialog.ShowDirsOnly)
        if path_input:
            self.label_scripts.setText(path_input)

    def on_open_vc_clicked(self):
        self.read_config()
        config = (self._config["db"], self._config["scans"], self._config["boards"])
        if all(config):
            self._vc = VerificationCenter(*config)

    def on_open_analysis_clicked(self):
        self.read_config()
        config = (self._config["boards"],
                  self._config["db"],
                  self._config["scripts"],
                  self._config["tables"],
                  self._config["tba"],
                  self._config["tba_event"])
        if all(config):
            self._analysis = AnalysisCenter(*config)

    def closeEvent(self, event):
        if self._vc is not None:
            self._vc.close()
        if self._analysis is not None:
            self._analysis.close()
        event.accept()


def run_app():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(os.path.join(os.getcwd(), "assets/app-icon.png")))
    _ = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    os.chdir("../../")
    run_app()
