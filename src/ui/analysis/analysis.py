from src.model.analysis.analysis_manager import AnalysisManager
from src.ui.analysis.analysis_ui import AnalysisUI


class AnalysisCenter(AnalysisUI):
    def __init__(self, *args):
        super().__init__()
        self.manager = AnalysisManager(*args)
