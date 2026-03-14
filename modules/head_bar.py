import PyQt6.QtWidgets as widgets
import PyQt6.QtCore as core
import PyQt6.QtGui as gui
from PyQt6.QtGui import QFont, QFontDatabase

from datetime import datetime, timedelta

import os

class HeadBar(widgets.QFrame):
    def __init__(self, parent):
        super().__init__(parent)

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        font_id = QFontDatabase.addApplicationFont(os.path.join(BASE_DIR,  "..", "media", "fonts", "Comfortaa-Regular.ttf"))
        font_family = QFontDatabase.applicationFontFamilies(font_id)

        self.setFixedSize(790, 50)
        self.setStyleSheet("background: transparent")
        

        self.MAIN_LAYOUT = widgets.QHBoxLayout(self)
        self.MAIN_LAYOUT.setAlignment(core.Qt.AlignmentFlag.AlignLeft)
        self.MAIN_LAYOUT.setSpacing(10)
        
        self.BUTTON_SETTINGS = widgets.QPushButton()
        self.BUTTON_SETTINGS.setFixedSize(36, 36)
        self.BUTTON_SETTINGS.setIcon(gui.QIcon("media/settings.svg"))
        self.BUTTON_SETTINGS.setIconSize(self.BUTTON_SETTINGS.size())

        self.MAIN_LAYOUT.addWidget(self.BUTTON_SETTINGS, alignment=core.Qt.AlignmentFlag.AlignVCenter)

