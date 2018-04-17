from src.model.vcmanager import VerificationManager
from src.ui.tablesui import Interface


class CalculationReader(Interface):
    def __init__(self, db_path, csv_dir_path, board_dir_path):
        self.manager = VerificationManager(db_path, csv_dir_path, board_dir_path)
        super().__init__()
        pass
