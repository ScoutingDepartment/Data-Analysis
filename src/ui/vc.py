from src.model.vcmanager import VerificationManager
from src.ui.vcwindow import VerificationWindow


class VerificationCenter(VerificationWindow):
    def __init__(self, db_path, csv_dir_path, board_dir_path):
        self.manager = VerificationManager(db_path, csv_dir_path, board_dir_path)

        super().__init__()

    def update_filtered_entries(self):
        for index, row in self.manager.search().iterrows():
            self.add_entry_item(index, row, self.manager.board_finder)
