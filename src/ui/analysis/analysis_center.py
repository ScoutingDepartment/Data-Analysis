from PyQt5.QtWidgets import QListWidgetItem, QFileDialog

from src.model.analysis.analysis_manager import AnalysisManager
from src.ui.analysis.analysis_ui import AnalysisUI


class AnalysisCenter(AnalysisUI):
    def __init__(self, *args):
        super().__init__()
        self.manager = AnalysisManager(*args)
        for title in self.manager.table_names():
            self.tables_nav.addItem(QListWidgetItem(title))
            self.manager.compute_all(tba_available=False)
        self.tables_nav.setCurrentRow(0)

        # self.table_content.update_contents("Raw Data", self.manager["raw_data"].data)

    def on_table_nav_selected(self):
        selected = self.tables_nav.selectedItems()
        if selected:
            new_table_name = self.manager.title_to_name(selected[0].text())
            new_table = self.manager[new_table_name]
            self.table_content.update_contents(new_table.title, new_table.data)
            self.table_content.table.scrollToTop()

    def on_calculate_with_tba(self):
        self.manager.compute_all(tba_available=True)
        self.on_table_nav_selected()

    def on_calculate_without_tba(self):
        self.manager.compute_all(tba_available=False)
        self.on_table_nav_selected()

    def on_open_tables_in_excel(self):
        self.manager.open_excel_instance()

    def on_save_csv_in_folder(self):
        path_input = QFileDialog.getExistingDirectory(None,
                                                      "Open Scripts Folder",
                                                      "")
        if path_input:
            self.manager.save_csv_folder(path_input)
