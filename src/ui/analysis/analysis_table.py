import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class AnalysisTable(QWidget):
    def __init__(self, parent, title):
        super().__init__(parent=parent, flags=Qt.Widget)
        self.table = QTableWidget(self)
        self.table.setRowCount(100)
        self.table.setColumnCount(100)
        for i in range(0, 100):
            for j in range(0, 100):
                self.table.setItem(i, j, QTableWidgetItem(str(i + 1) + ", " + str(j + 1)))
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.setContentsMargins(0, 0, 0, 0)
        self.table.resizeColumnsToContents()
        self.table.setAlternatingRowColors(True)
        self.setLayout(layout)
        self.setMinimumSize(400, 400)
        self.setWindowTitle(title)
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("../../../assets/app-icon.png"))
    w = AnalysisTable(None, "Table Widget")
    sys.exit(app.exec_())
