import sys

import numpy as np
import pandas as pd
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QTableWidget, QVBoxLayout, QTableWidgetItem, QApplication


class AnalysisTable(QWidget):
    def __init__(self, parent):
        super().__init__(parent=parent, flags=Qt.Widget)

        self.table = QTableWidget(self)
        self.table.setAlternatingRowColors(True)

        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

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
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)

                cell = data.iat[i, j]

                if type(cell) is str:
                    item.setData(Qt.DisplayRole, cell)
                    item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                else:
                    scalar = np.asscalar(cell)
                    item.setData(Qt.DisplayRole, scalar)
                    if type(scalar) is int or type(scalar) is float:
                        item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    else:
                        item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)

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
