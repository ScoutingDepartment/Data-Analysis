from PyQt5.QtWidgets import QListWidgetItem

from src.model.analysis.analysis_manager import AnalysisManager
from src.ui.analysis.analysis_ui import AnalysisUI


class AnalysisCenter(AnalysisUI):
    def __init__(self, *args):
        super().__init__()
        self.manager = AnalysisManager(*args)
        self.manager.compute_all()
        for title in self.manager.table_names():
            self.tables_nav.addItem(QListWidgetItem(title))
        self.tables_nav.setCurrentRow(0)

        self.table_content.update_contents("Raw Data", self.manager["raw_data"].data)
