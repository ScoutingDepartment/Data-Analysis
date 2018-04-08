import sys

import numpy as np
import pandas as pd
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

    def comboBoxChange(self):
        pass

    def createTable(self, df):

        # Create table
        self.tableWidget = QTableWidget()

        row_count = len(list(df.index))
        column_count = len(list(df.columns.values))
        self.tableWidget.setRowCount(row_count)
        self.tableWidget.setColumnCount(column_count)

        self.dataTypes = ['data type', 'dahta type', 'dayta type']

        for r in range(len(df.values)):
            for c in range(len(df.values[r])):
                if c == 0:
                    self.comboBox = QComboBox()

                    self.comboBox.addItems(self.dataTypes)

                    self.comboBox.setCurrentText(df.values[r][c])

                    self.tableWidget.setCellWidget(r, c, self.comboBox)

                else:
                    self.tableWidget.setItem(r, c, QTableWidgetItem(df.values[r][c]))

        self.tableWidget.setHorizontalHeaderLabels(list(df.columns.values))
        self.tableWidget.setVerticalHeaderLabels(list(df.index))

        self.tableWidget.doubleClicked.connect(self.on_click)

    def read(self):
        data = [[''] * (self.tableWidget.columnCount() + 1) for _ in range((self.tableWidget.rowCount() + 1))]
        data[0][1] = 'Data Type'
        data[0][2] = 'Value'
        for r in range(1, self.tableWidget.rowCount() + 1):
            for c in range(1, self.tableWidget.columnCount() + 1):
                if c == 1:
                    cb = self.tableWidget.cellWidget(r - 1, 0)
                    data[r][c] = self.dataTypes[cb.currentIndex()]
                    data[r][0] = r
                else:
                    data[r][c] = self.tableWidget.item(r - 1, c - 1).text()

        npArray = (np.array(data))
        df = pd.DataFrame(data=npArray[1:, 1:],
                          index=npArray[1:, 0],
                          columns=npArray[0, 1:])
        return df

    def on_click(self):
        print(self.read())


if __name__ == '__main__':
    data = np.array([['', 'Col1', 'Col2', 'col3'],
                     ['Row1', 'dahta type', 2, 1],
                     ['Row3', 'dahta type', 2, 2],
                     ['Row5', 'dayta type', 3, 3],
                     ['Row2', 3, 4, 5]])

    df = pd.DataFrame(data=data[1:, 1:],
                      index=data[1:, 0],
                      columns=data[0, 1:])

    print(df)

    app = QApplication(sys.argv)

    ex = displayDataFrame(df)
    sys.exit(app.exec_())
