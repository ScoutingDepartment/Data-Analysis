import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QComboBox, QCheckBox

INDEXES = {'Data Types': 0,
           'Values': 2,
           'Undo': 3}

HEADERS = INDEXES.keys()


class EntryDetailsWidget(QWidget):

    def __init__(self, parent, editable):
        super().__init__(parent=parent, flags=Qt.Widget)

        self.data_types = []
        self.data = []

        self.data_table = QTableWidget()
        self.data_table.doubleClicked.connect(self.on_click)
        self.data_table.setEnabled(editable)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.data_table)
        self.setLayout(self.layout)
        self.show()

    def update_data(self, data, data_types):
        self.data = data
        self.data_types = data_types

        self.data_table.clear()

        row_count = len(self.data)
        column_count = len(HEADERS)

        self.data_table.setRowCount(row_count)
        self.data_table.setColumnCount(column_count)

        for row in range(len(self.data)):
            for column in range(len(self.data[row])):

                if column == INDEXES['Data Types']:
                    type_chooser = QComboBox()
                    type_chooser.addItems(self.data_types)
                    print(self.data[row][column])
                    type_chooser.setCurrentText(str(self.data[row][column]))
                    self.data_table.setCellWidget(row, list(INDEXES.keys()).index('Data Types'), type_chooser)

                elif column == INDEXES['Undo']:
                    undo_checker = QCheckBox()
                    undo_checker.setCheckState(2 if self.data[row][column] else 0)
                    self.data_table.setCellWidget(row, (list(INDEXES.keys())).index('Undo'), undo_checker)

                elif column == INDEXES['Values']:
                    self.data_table.setItem(row,
                                            list(INDEXES.keys()).index('Values'),
                                            QTableWidgetItem(str(self.data[row][column])))
                else:
                    self.data_table.setItem(row,
                                            list(INDEXES.keys()).index('Values'),
                                            QTableWidgetItem(str(self.data[row][column])))

        self.data_table.setHorizontalHeaderLabels(HEADERS)
        self.data_table.setVerticalHeaderLabels([str(s + 1) for s in range(len(self.data))])

    def read(self):
        data = [[''] * (self.data_table.columnCount()) for _ in range((self.data_table.rowCount()))]

        for r in range(len(data)):
            for c in range(len(data[r])):
                if c == INDEXES['Data Types']:
                    comboBox = self.data_table.cellWidget(r, c)
                    data[r][c] = self.data_types[comboBox.currentIndex()]
                elif c == INDEXES['Undo']:
                    checkBox = self.data_table.cellWidget(r, c)
                    if checkBox.checkState() == 2:
                        data[r][c] = True
                    else:
                        data[r][c] = False
                elif c == INDEXES['Values']:
                    data[r][c] = self.data_table.item(r, c).text()

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

    ex = EntryDetailsWidget(None, False)
    ex.update_data(test_data, test_types)
    sys.exit(app.exec_())
