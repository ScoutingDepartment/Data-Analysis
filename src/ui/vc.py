from PyQt5.QtWidgets import QFileDialog

from src.model.vc.vcmanager import VerificationManager
from src.ui.vcwindow import VerificationWindow


class VerificationCenter(VerificationWindow):
    def __init__(self, db_path, csv_dir_path, board_dir_path):
        self.manager = VerificationManager(db_path, csv_dir_path, board_dir_path)
        self.working_entry = None
        self.original_entry = None
        self.last_selected = None
        self.working_index = -1
        self.edited = ""

        super().__init__()

        # Patch for the comment edited issue (not good practice)
        self.current_entry_comments.textEdited.connect(self.details.on_edited)

    def read_working_entry_changes(self):
        # Read the edited data
        if self.working_index != -1 and self.details.user_edited:
            if self.last_selected:
                entry_item = self.filtered_entries.itemWidget(self.last_selected)
                entry_item.update_edited_state(True)
            self.details.update_data()
            self.working_entry.comments = self.current_entry_comments.text()
            self.manager[self.working_index] = self.working_entry
            self.log.setText("Copied Changes to RAM: #" + str(self.working_index))

    def on_entry_selected(self):
        selected = self.filtered_entries.selectedItems()
        if selected:
            self.read_working_entry_changes()

            entry_item = self.filtered_entries.itemWidget(selected[0])
            self.original_entry, self.working_entry, last_edited = self.manager[entry_item.db_index]

            self.working_index = entry_item.db_index

            self.current_entry_match_number.setText(str(self.working_entry.match))
            self.current_entry_team_number.setText(str(self.working_entry.team))
            self.current_entry_scout_name.setText(self.working_entry.name)
            self.current_entry_time_started.setText(self.working_entry.start_time)
            self.current_entry_comments.setText(self.working_entry.comments)
            self.current_entry_board.setText(self.working_entry.board.name())
            self.current_entry_last_time_edited.setText(last_edited)

            self.details.update_table_widget(self.working_entry.decoded_data,
                                             self.working_entry.board.list_logs())
            self.original_details.update_table_widget(self.original_entry.decoded_data,
                                                      self.original_entry.board.list_logs())

            self.last_selected = selected[0]

    def on_update(self):
        self.log.setText("Updating")
        self.manager.update()
        self.on_filter_edited()
        self.log.setText("Updated")

    def on_save(self):
        self.log.setText("Saving")
        self.manager.save()
        self.log.setText("Saved")

    def on_filter_edited(self):
        teams = self.filter_team_number.text().split(",")
        teams = [team.strip() for team in teams]
        teams = [int(team) for team in teams if team.isdigit()]

        matches = self.filter_match_number.text().split(",")
        matches = [match.strip() for match in matches]
        matches = [int(match) for match in matches if match.isdigit()]

        names = self.filter_scout_name.text().split(",")
        names = [name.strip() for name in names if name.strip()]

        self.filtered_entries.clear()
        for index, row in self.manager.search(match=matches,
                                              team=teams,
                                              name=names).iterrows():
            self.add_entry_item(index, row, self.manager.board_finder)

        if self.filtered_entries.count() > 0:
            self.filtered_entries.setCurrentRow(0)
            self.working_index = 0
        else:
            self.working_index = -1

    def on_export_csv(self):
        path = QFileDialog.getSaveFileName(self, "Save CSV", "", filter="(*.csv)")
        if path[0]:
            self.manager.write_csv(path[0])
            self.log.setText("Saved CSV to: " + path[0])

    def on_add_item_clicked(self):
        self.details.add_row()

    def closeEvent(self, event):
        # self.read_working_entry_changes()
        # self.manager.save()
        event.accept()
