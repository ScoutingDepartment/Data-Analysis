import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QComboBox, QCheckBox


class EntryDetailsWidget(QWidget):

    def __init__(self, parent, data, dataTypes):
        super().__init__(parent=parent, flags=Qt.Widget)
        self.title = 'PyQt5 table - pythonspot.com'
        self.left = 100
        self.top = 100
        self.width = 300
        self.height = 200
        self.dataTypes = dataTypes
        self.data = data
        self.headers = ["Data Type", "Value", "Undo"]
        self.initUI()

    def initUI(self):
        # self.setWindowTitle(self.title)
        # self.setGeometry(self.left, self.top, self.width, self.height)

        self.createTable()

        # Add box layout, add table to box layout and add box layout to widget
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)
        # Show widget
        self.show()

    def comboBoxChange(self):
        pass

    def createTable(self):


        # Create table
        self.tableWidget = QTableWidget()

        row_count = len(self.data)
        column_count = len(self.data[0])
        self.tableWidget.setRowCount(row_count)
        self.tableWidget.setColumnCount(column_count)

        for r in range(len(self.data)):
            for c in range(len(self.data[r])):
                if c == 0:
                    self.comboBox = QComboBox()

                    self.comboBox.addItems(self.dataTypes)

                    self.comboBox.setCurrentText(str(self.data[r][c]))

                    self.tableWidget.setCellWidget(r, c, self.comboBox)
                elif c == 2:
                    self.checkBox = QCheckBox()

                    if self.data[r][c]:
                        self.checkBox.setCheckState(2)
                    else:
                        self.checkBox.setCheckState(0)

                    self.tableWidget.setCellWidget(r, c, self.checkBox)

                else:
                    print(str(r) + " r")
                    print(str(c) + " c")
                    print(self.data[r][c])
                    self.tableWidget.setItem(r, c, QTableWidgetItem(str(self.data[r][c])))

        self.tableWidget.setHorizontalHeaderLabels(self.headers)
        self.tableWidget.setVerticalHeaderLabels([str(s + 1) for s in range(len(self.data))])

        self.tableWidget.doubleClicked.connect(self.on_click)

    def read(self):
        data = [[''] * (self.tableWidget.columnCount()) for _ in range((self.tableWidget.rowCount()))]

        for r in range(len(data)):
            for c in range(len(data[r])):
                if c == 0:
                    comboBox = self.tableWidget.cellWidget(r, c)
                    data[r][c] = self.dataTypes[comboBox.currentIndex()]
                elif c == 2:
                    checkBox = self.tableWidget.cellWidget(r, c)
                    if checkBox.checkState() == 2:
                        data[r][c] = True
                    else:
                        data[r][c] = False
                else:
                    data[r][c] = self.tableWidget.item(r, c).text()

        return data

    def on_click(self):
        print(self.read())


if __name__ == '__main__':
    data = [['dahta type', 2, True],
            ['dahta type', 2, False],
            ['dayta type', 3, False],
            [3, 4, False]]

    print(data)

    app = QApplication(sys.argv)

    ex = EntryDetailsWidget(data, ['data type', 'dahta type', 'dayta type'])
    sys.exit(app.exec_())
