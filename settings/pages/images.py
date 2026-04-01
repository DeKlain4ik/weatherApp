import PyQt6.QtWidgets as widgets
import PyQt6.QtCore as core
import PyQt6.QtGui as gui
from PyQt6.QtGui import QFont, QFontDatabase
import os


class Images(widgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setAttribute(core.Qt.WidgetAttribute.WA_TranslucentBackground)

        self.setStyleSheet("background: transparent; border-radius: 16px;")

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        font_id = QFontDatabase.addApplicationFont(os.path.join(BASE_DIR, "..", "..", "media", "fonts", "Comfortaa-Regular.ttf"))
        font_family = QFontDatabase.applicationFontFamilies(font_id)
        
        self.CENTRAL_LAYOUT = widgets.QVBoxLayout(self)
        self.CENTRAL_LAYOUT.setContentsMargins(10, 30, 10, 10)
        self.CENTRAL_LAYOUT.setSpacing(0)

        label = widgets.QLabel("Списки зображень")
        label.setFont(QFont(font_family[0], 18))
        label.setStyleSheet("background: transparent;")
        self.CENTRAL_LAYOUT.addWidget(label, alignment=core.Qt.AlignmentFlag.AlignTop | core.Qt.AlignmentFlag.AlignLeft)