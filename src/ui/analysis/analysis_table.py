import sys

import numpy as np
import pandas as pd
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class AnalysisTable(QWidget):
    def __init__(self, parent):
        super().__init__(parent=parent, flags=Qt.Widget)

        self.table = QTableWidget(self)
        self.table.setAlternatingRowColors(True)

        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.setMinimumSize(800, 800)
        self.show()

    def update_contents(self, title, data: "pd.DataFrame"):

        self.setWindowTitle(title)
        self.setUpdatesEnabled(False)
        self.table.clear()
        self.table.setRowCount(data.index.size)
        self.table.setColumnCount(data.columns.size)
        for i in range(data.index.size):
            for j in range(data.columns.size):
                item = QTableWidgetItem()
                item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                d = data.iat[i, j]
                if type(d) is np.int64:
                    item.setData(Qt.DisplayRole, int(d))
                else:
                    item.setData(Qt.DisplayRole, str(d))
                self.table.setItem(i, j, item)

        self.table.setHorizontalHeaderLabels(map(str, data.columns))
        self.table.setVerticalHeaderLabels(map(str, data.index))
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        self.table.setSortingEnabled(True)
        self.setUpdatesEnabled(True)
        self.update()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("../../../assets/app-icon.png"))
    w = AnalysisTable(None)
    sys.exit(app.exec_())
