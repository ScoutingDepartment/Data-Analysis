import sys

import numpy as np
import pandas as pd
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QComboBox


class displayDataFrame(QWidget):

    def __init__(self, df):
        super().__init__()
        self.title = 'PyQt5 table - pythonspot.com'
        self.left = 100
        self.top = 100
        self.width = 300
        self.height = 200
        self.initUI(df)

    def initUI(self, df):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.createTable(df)

        # Add box layout, add table to box layout and add box layout to widget
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)

        # Show widget
        self.show()

    def createTable(self, df):

        # Create table
        self.tableWidget = QTableWidget()

        row_count = len(list(df.index))
        column_count = len(list(df.columns.values))
        self.tableWidget.setRowCount(row_count)
        self.tableWidget.setColumnCount(column_count)

        dataTypes = ['data type 1', 'Data Type 2', 'dataType 3', 'dayta type 4']

        for r in range(len(df.values)):
            for c in range(len(df.values[r])):
                if c == 0:
                    comboBox = QComboBox()

                    comboBox.addItems(dataTypes)

                    comboBox.setCurrentText(df.values[r][c])

                    self.tableWidget.setCellWidget(r, c, comboBox)
                else:
                    self.tableWidget.setItem(r, c, QTableWidgetItem(df.values[r][c]))

        self.tableWidget.setHorizontalHeaderLabels(list(df.columns.values))
        self.tableWidget.setVerticalHeaderLabels(list(df.index))

        # table selection change
        self.tableWidget.doubleClicked.connect(self.on_click)

    @pyqtSlot()
    def on_click(self):
        pass


if __name__ == '__main__':
    data = np.array([['', 'Col1', 'Col2', 'col3'],
                     ['Row1', 'Data Type 2', 2, 1],
                     ['Row3', 'dayta type 4', 2, 2],
                     ['Row5', 'data type 1', 3, 3],
                     ['Row2', 3, 4, 5]])

    df = pd.DataFrame(data=data[1:, 1:],
                      index=data[1:, 0],
                      columns=data[0, 1:])

    print(df)

    app = QApplication(sys.argv)

    ex = displayDataFrame(df)
    sys.exit(app.exec_())
