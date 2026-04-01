from PyQt6 import QtCore as core 
from PyQt6 import QtWidgets as widgets
import PyQt6.QtGui as gui
import os
from PyQt6.QtGui import QFont, QFontDatabase


class Title_bar(widgets.QFrame):
    def __init__(self, parent, width):
        widgets.QFrame.__init__(self, parent = parent)

                
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        font_id = QFontDatabase.addApplicationFont(os.path.join(BASE_DIR, "..", "media", "fonts", "Comfortaa-Regular.ttf"))
        font_family = QFontDatabase.applicationFontFamilies(font_id)
        
        self.LAYOUT = widgets.QHBoxLayout()
        self.LAYOUT.setContentsMargins(10, 0, 10, 0)
        self.LAYOUT.setSpacing(0)
        
        self.setLayout(self.LAYOUT)
        
        self.setFixedHeight(40)
        self.setStyleSheet("background: transparent;")
        
        self.WINDOW = self.window()

        self.text_settings = widgets.QLabel("Налаштування")
        self.text_settings.setFont(QFont(font_family[0], 24))

        self.text_settings.setStyleSheet("background: transparent; ")
        
        self.CLOSE_BUTTON = widgets.QToolButton(parent = self)
        icon = gui.QIcon("media/x.svg")
        self.CLOSE_BUTTON.setIcon(icon)
        self.CLOSE_BUTTON.setIconSize(core.QSize(24, 24))
        self.CLOSE_BUTTON.setStyleSheet("border: none; ")
        self.CLOSE_BUTTON.clicked.connect(self.WINDOW.close)
        
        self.LAYOUT.addWidget(self.text_settings, alignment=core.Qt.AlignmentFlag.AlignLeft | core.Qt.AlignmentFlag.AlignVCenter)
        self.LAYOUT.addStretch()
        self.LAYOUT.addWidget(self.CLOSE_BUTTON, alignment=core.Qt.AlignmentFlag.AlignRight | core.Qt.AlignmentFlag.AlignVCenter)

    

    def toggle_maximize(self):
        if self.WINDOW.isMaximized():
            self.WINDOW.showNormal()  
        else:
            self.WINDOW.showMaximized()
