import sys

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from src.ui.vcwindow import VerificationWindow


class VerificationCenter(VerificationWindow):
    def __init__(self, db_path, csv_dir_path, board_dir_path):
        super().__init__()

        QMessageBox.information(self, "VC started", "{}\n{}\n{}".format(db_path, csv_dir_path, board_dir_path))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("../../assets/app-icon.png"))
    vc = VerificationCenter("warp7 file", "b", "c")
    sys.exit(app.exec_())
