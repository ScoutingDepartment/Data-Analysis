from src.model.vcmanager import VerificationManager
from src.ui.vcwindow import VerificationWindow


class VerificationCenter(VerificationWindow):
    def __init__(self, db_path, csv_dir_path, board_dir_path):
        self.manager = VerificationManager(db_path, csv_dir_path, board_dir_path)
        self.working_entry = None
        self.original_entry = None
        self.edited = ""

        super().__init__()

    def update_filtered_entries(self):
        for index, row in self.manager.search().iterrows():
            self.add_entry_item(index, row, self.manager.board_finder)

    def on_entry_selected(self):
        selected = self.filtered_entries.selectedItems()
        if selected:
            entry_item = self.filtered_entries.itemWidget(selected[0])
            self.original_entry, self.working_entry = self.manager[entry_item.db_index]
            # TODO Add edited

            self.current_entry_match_number.setText(str(self.working_entry.match))
            self.current_entry_team_number.setText(str(self.working_entry.team))
            self.current_entry_scout_name.setText(str(self.working_entry.name))
            self.current_entry_time_started.setText(str(self.working_entry.start_time))
            self.current_entry_comments.setText(str(self.working_entry.comments))
            self.current_entry_board.setText(str(self.working_entry.board.name()))
            self.current_entry_last_time_edited.setText("")

            self.details.update_data(self.working_entry.decoded_data,
                                     self.working_entry.board.list_logs())
            self.original_details.update_data(self.original_entry.decoded_data,
                                              self.original_entry.board.list_logs())

    def on_update(self):
        self.log.setText("Updating")
        self.manager.update()
        self.update_filtered_entries()
        self.log.setText("Updated")

    def on_save(self):
        self.log.setText("Saving")
        self.manager.save()
        self.log.setText("Saved")
