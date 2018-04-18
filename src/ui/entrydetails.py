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
        self.editable = editable
        self.user_edited = False

        self.data_table = QTableWidget()
        self.data_table.doubleClicked.connect(self.on_double_click)

        self.data_table.verticalHeader().setVisible(False)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.data_table)
        self.setLayout(self.layout)
        self.show()

    def update_table_widget(self, data, data_types):
        self.data = data
        self.data_types = data_types

        self.user_edited = False

        row_count = len(self.data)
        column_count = len(HEADERS)

        self.setUpdatesEnabled(False)

        self.data_table.clear()

        self.data_table.setRowCount(row_count)
        self.data_table.setColumnCount(column_count)
        self.data_table.disconnect()

        for row in range(len(self.data)):
            for column in range(len(self.data[row])):

                if column == INDEXES['Data Types']:
                    type_chooser = QComboBox()
                    if self.data[row][column] == None or self.data[row][column] not in self.data_types:
                        type_chooser.addItem(None)
                    type_chooser.addItems(self.data_types)
                    type_chooser.setCurrentText(str(self.data[row][column]))
                    type_chooser.setEnabled(self.editable)
                    type_chooser.currentTextChanged.connect(self.on_edited)
                    self.data_table.setCellWidget(row, list(INDEXES.keys()).index('Data Types'), type_chooser)

                elif column == INDEXES['Undo']:
                    undo_checker = QCheckBox()
                    undo_checker.setCheckState(2 if self.data[row][column] else 0)
                    undo_checker.setEnabled(self.editable)
                    undo_checker.stateChanged.connect(self.on_edited)
                    self.data_table.setCellWidget(row, list(INDEXES.keys()).index('Undo'), undo_checker)

                elif column == INDEXES['Values']:
                    value_item = QTableWidgetItem(str(self.data[row][column]))
                    if not self.editable:
                        value_item.setFlags(value_item.flags() ^ Qt.ItemIsEditable)
                    self.data_table.setItem(row,
                                            list(INDEXES.keys()).index('Values'),
                                            value_item)

        self.data_table.setHorizontalHeaderLabels(HEADERS)
        self.data_table.resizeColumnsToContents()
        self.data_table.scrollToTop()

        self.data_table.itemChanged.connect(self.on_edited)

        self.setUpdatesEnabled(True)

        self.update()  # Call the UI updater in Qt

    def update_data(self):
        for r in range(len(self.data)):
            for c in range(len(self.data[r])):
                if c == INDEXES['Data Types']:
                    combo_box = self.data_table.cellWidget(r, list(INDEXES.keys()).index('Data Types'))
                    self.data[r][c] = self.data_types[combo_box.currentIndex()]
                elif c == INDEXES['Undo']:
                    check_box = self.data_table.cellWidget(r, list(INDEXES.keys()).index('Undo'))
                    if check_box.checkState() == 2:
                        self.data[r][c] = True
                    else:
                        self.data[r][c] = False
                elif c == INDEXES['Values']:
                    str_value = self.data_table.item(r, list(INDEXES.keys()).index('Values')).text()
                    if str_value.isdigit():
                        int_value = int(str_value)
                        if 0 < int_value < 256:
                            self.data[r][c] = int_value

    def on_double_click(self):
        self.update_data()
        # print(self.data)
        text_file = open("temp.txt", "w")
        for r in self.data:
            for c in r:
                text_file.write(str(c))
                text_file.write("\n")
            text_file.write("\n")
        text_file.close()
        #print("hi")

    def on_edited(self):
        self.user_edited = True

    def add_row(self):
        self.data.append([None, False, '', False])
        self.update_table_widget(self.data, self.data_types)
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

    ex = EntryDetailsWidget(None, True)
    ex.update_table_widget(test_data, test_types)
    ex.add_row()
    sys.exit(app.exec_())
