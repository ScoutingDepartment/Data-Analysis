from src.model.vcmanager import VerificationManager
from src.ui.vcwindow import VerificationWindow


class VerificationCenter(VerificationWindow):
    def __init__(self, db_path, csv_dir_path, board_dir_path):
        self.manager = VerificationManager(db_path, csv_dir_path, board_dir_path)
        self.working_entry = None
        self.original_entry = None

        super().__init__()

    def update_filtered_entries(self):
        for index, row in self.manager.search().iterrows():
            self.add_entry_item(index, row, self.manager.board_finder)

    def on_entry_selected(self):
        selected = self.filtered_entries.selectedItems()
        if selected:
            entry_item = self.filtered_entries.itemWidget(selected[0])
            self.original_entry, self.working_entry = self.manager[entry_item.db_index]

            self.current_entry_match_number.setText(str(self.working_entry.match))
            self.current_entry_team_number.setText(str(self.working_entry.team))
            self.current_entry_scout_name.setText(str(self.working_entry.name))
            self.current_entry_time_started.setText(str(self.working_entry.start_time))
            self.current_entry_comments.setText(str(self.working_entry.comments))

    def on_update(self):
        self.log.setText("Updating")
        self.manager.update()
        self.update_filtered_entries()
        self.log.setText("Updated")

    def on_save(self):
        self.log.setText("Saving")
        self.manager.save()
        self.log.setText("Saved")
