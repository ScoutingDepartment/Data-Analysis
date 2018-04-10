import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QComboBox, QCheckBox

INDEXES = {'Data Types': 1,
           'Values': 2,
           'Undo': 3}

HEADERS = INDEXES.keys()


class EntryDetailsWidget(QWidget):

    def __init__(self, parent):
        super().__init__(parent=parent, flags=Qt.Widget)

        self.dataTypes = []
        self.data = []

        self.tableWidget = QTableWidget()
        self.tableWidget.doubleClicked.connect(self.on_click)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)
        self.show()

    def update_data(self, data, dataTypes):
        self.data = data
        self.dataTypes = dataTypes

        self.tableWidget.clear()

        row_count = len(self.data)
        column_count = len(HEADERS)

        self.tableWidget.setRowCount(row_count)
        self.tableWidget.setColumnCount(column_count)

        for row in range(len(self.data)):
            for column in range(len(self.data[row])):

                if column == INDEXES['Data Types']:
                    type_chooser = QComboBox()
                    type_chooser.addItems(self.dataTypes)
                    type_chooser.setCurrentText(str(self.data[row][column]))
                    self.tableWidget.setCellWidget(row, list(INDEXES.keys()).index('Data Types'), type_chooser)

                elif column == INDEXES['Undo']:
                    undo_checker = QCheckBox()
                    undo_checker.setCheckState(2 if self.data[row][column] else 0)
                    self.tableWidget.setCellWidget(row, (list(INDEXES.keys())).index('Undo'), undo_checker)

                elif column == INDEXES['Values']:
                    self.tableWidget.setItem(row,
                                             list(INDEXES.keys()).index('Values'),
                                             QTableWidgetItem(str(self.data[row][column])))
                else:
                    self.tableWidget.setItem(row,
                                             list(INDEXES.keys()).index('Values'),
                                             QTableWidgetItem(str(self.data[row][column])))

        self.tableWidget.setHorizontalHeaderLabels(HEADERS)
        self.tableWidget.setVerticalHeaderLabels([str(s + 1) for s in range(len(self.data))])

    def read(self):
        data = [[''] * (self.tableWidget.columnCount()) for _ in range((self.tableWidget.rowCount()))]

        for r in range(len(data)):
            for c in range(len(data[r])):
                if c == INDEXES['Data Types']:
                    comboBox = self.tableWidget.cellWidget(r, c)
                    data[r][c] = self.dataTypes[comboBox.currentIndex()]
                elif c == INDEXES['Undo']:
                    checkBox = self.tableWidget.cellWidget(r, c)
                    if checkBox.checkState() == 2:
                        data[r][c] = True
                    else:
                        data[r][c] = False
                elif c == INDEXES['Values']:
                    data[r][c] = self.tableWidget.item(r, c).text()

        return data

    def on_click(self):
        pass


if __name__ == '__main__':
    test_types = ['Auto line', 'Auto scale attempt', 'Auto scale', 'Auto switch attempt', 'Auto switch',
                  'Auto exchange attempt', 'Auto exchange', 'Tele intake', 'Defense', 'Tele exchange',
                  'Tele alliance switch', 'Tele opponent switch', 'Tele scale', 'Platform', 'Climb', 'Attachment speed',
                  'Climb speed', 'Intake speed', 'Intake consistency', 'Exchange speed', 'Switch speed', 'Scale speed',
                  'Driver skill']

    test_data = [['Auto line', True, 1, False],
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
    ex.update_data(test_data, test_types)
    sys.exit(app.exec_())
