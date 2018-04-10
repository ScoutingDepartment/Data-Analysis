import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QComboBox, QCheckBox


class EntryDetailsWidget(QWidget):

    def __init__(self, parent):
        super().__init__(parent=parent, flags=Qt.Widget)

        self.dataTypes = []
        self.data = []
        self.indexes = {'Data Types': 0,
                        'Values': 2,
                        'Undo': 3}

        self.headers = self.indexes.keys()

        self.tableWidget = QTableWidget()
        self.tableWidget.doubleClicked.connect(self.on_click)

        # Add box layout, add table to box layout and add box layout to widget
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)
        self.show()

    def create_table(self):

        while (self.tableWidget.rowCount() > 0):
            self.tableWidget.removeRow(0)


        row_count = len(self.data)
        column_count = len(self.headers)
        self.tableWidget.setRowCount(row_count)
        self.tableWidget.setColumnCount(column_count)

        for r in range(len(self.data)):
            for c in range(len(self.data[r])):
                if c == self.indexes['Data Types']:
                    self.comboBox = QComboBox()

                    self.comboBox.addItems(self.dataTypes)

                    self.comboBox.setCurrentText(str(self.data[r][c]))

                    self.tableWidget.setCellWidget(r, list(self.indexes.keys()).index('Data Types'), self.comboBox)
                elif c == self.indexes['Undo']:
                    self.checkBox = QCheckBox()

                    if self.data[r][c]:
                        self.checkBox.setCheckState(2)
                    else:
                        self.checkBox.setCheckState(0)

                    self.tableWidget.setCellWidget(r, (list(self.indexes.keys())).index('Undo'), self.checkBox)

                elif c == self.indexes['Values']:
                    self.tableWidget.setItem(r, list(self.indexes.keys()).index('Values'),
                                             QTableWidgetItem(str(self.data[r][c])))
                else:
                    self.tableWidget.setItem(r, list(self.indexes.keys()).index('Values'),
                                             QTableWidgetItem(str(self.data[r][c])))


        self.tableWidget.setHorizontalHeaderLabels(self.headers)
        self.tableWidget.setVerticalHeaderLabels([str(s + 1) for s in range(len(self.data))])

    def update(self, data, dataTypes):
        self.data = data
        self.dataTypes = dataTypes
        self.create_table()

    def read(self):
        data = [[''] * (self.tableWidget.columnCount()) for _ in range((self.tableWidget.rowCount()))]

        for r in range(len(data)):
            for c in range(len(data[r])):
                if c == self.indexes['Data Types']:
                    comboBox = self.tableWidget.cellWidget(r, c)
                    data[r][c] = self.dataTypes[comboBox.currentIndex()]
                elif c == self.indexes['Undo']:
                    checkBox = self.tableWidget.cellWidget(r, c)
                    if checkBox.checkState() == 2:
                        data[r][c] = True
                    else:
                        data[r][c] = False
                elif c == self.indexes['Values']:
                    data[r][c] = self.tableWidget.item(r, c).text()

        return data

    def on_click(self):
        self.update([['Auto line', True, 1, False],
                     ['Platform', True, 0, False],
                     ['Climb', True, 0, False],
                     ['Attachment speed', True, 0, False],
                     ['Climb speed', True, 0, False],
                     ['Intake speed', True, 3, False],
                     ['Intake consistency', True, 4, False]], self.dataTypes)


if __name__ == '__main__':
    types = ['Auto line', 'Auto scale attempt', 'Auto scale', 'Auto switch attempt', 'Auto switch',
             'Auto exchange attempt', 'Auto exchange', 'Tele intake', 'Defense', 'Tele exchange',
             'Tele alliance switch', 'Tele opponent switch', 'Tele scale', 'Platform', 'Climb', 'Attachment speed',
             'Climb speed', 'Intake speed', 'Intake consistency', 'Exchange speed', 'Switch speed', 'Scale speed',
             'Driver skill']

    data = [['Auto line', True, 1, False],
            ['Platform', True, 0, False],
            ['Climb', True, 0, False],
            ['Attachment speed', True, 0, False],
            ['Climb speed', True, 0, False],
            ['Intake speed', True, 3, False],
            ['Intake consistency', True, 4, False],
            ['Exchange speed', True, 3, False],
            ['Switch speed', True, 2, False],
            ['Scale speed', True, 0, False],
            ['Driver skill', True, 0, False],
            ['Tele alliance switch', True, 44, False],
            ['Tele intake', True, 66, False],
            ['Tele exchange', True, 70, False],
            ['Tele intake', True, 84, False],
            ['Tele exchange', True, 92, False],
            ['Tele exchange', True, 103, False],
            ['Tele intake', True, 108, False],
            ['Tele exchange', True, 114, False],
            ['Tele exchange', True, 130, False]]

    app = QApplication(sys.argv)

    ex = EntryDetailsWidget(None)
    ex.update(data, types)
    sys.exit(app.exec_())
