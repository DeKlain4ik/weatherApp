import PyQt6.QtWidgets as widgets
import PyQt6.QtCore as core
import PyQt6.QtGui as gui
from PyQt6.QtGui import QFont, QFontDatabase
import os


class Size(widgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setAttribute(core.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet("background: transparent; border-radius: 16px;")

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        font_id = QFontDatabase.addApplicationFont(os.path.join(BASE_DIR, "..", "..", "media", "fonts", "Comfortaa-Regular.ttf"))
        self.font_family = QFontDatabase.applicationFontFamilies(font_id)

        self.main_window = parent.main_window if parent else None

        self.CENTRAL_LAYOUT = widgets.QVBoxLayout(self)
        self.CENTRAL_LAYOUT.setContentsMargins(10, 30, 10, 10)
        self.CENTRAL_LAYOUT.setSpacing(0)

        label = widgets.QLabel("Розмір додатку")
        label.setFont(QFont(self.font_family[0], 18))
        label.setStyleSheet("background: transparent;")
        self.CENTRAL_LAYOUT.addWidget(label, alignment=core.Qt.AlignmentFlag.AlignTop | core.Qt.AlignmentFlag.AlignLeft)

        self.WINDOW_SIZE_LAYOUT = widgets.QVBoxLayout()
        self.WINDOW_SIZE_LAYOUT.setContentsMargins(10, 10, 10, 10)
        self.WINDOW_SIZE_LAYOUT.setSpacing(10)
        self.WINDOW_SIZE_LAYOUT.setAlignment(core.Qt.AlignmentFlag.AlignTop)
        self.CENTRAL_LAYOUT.addLayout(self.WINDOW_SIZE_LAYOUT)

        self.CENTRAL_LAYOUT.addStretch()
        


        self.RADIO_BUTTOM_SIZE_1 = self.create_radio_button("1200x800", 1200, 800)
        self.RADIO_BUTTOM_SIZE_2 = self.create_radio_button("1440x1024", 1440, 1024)
        self.RADIO_BUTTOM_SIZE_3 = self.create_radio_button("1512x982", 1512, 982)
        self.RADIO_BUTTOM_SIZE_4 = self.create_radio_button("1728x1117", 1728, 1117)

        
        current_size = self.main_window.size() 
        if self.main_window else core.QSize(1200, 800)
        
        if current_size.width() == 1200 and current_size.height() == 800:
            self.RADIO_BUTTOM_SIZE_1.setChecked(True)
        elif current_size.width() == 1440 and current_size.height() == 1024:
            self.RADIO_BUTTOM_SIZE_2.setChecked(True)
        elif current_size.width() == 1512 and current_size.height() == 982:
            self.RADIO_BUTTOM_SIZE_3.setChecked(True)
        elif current_size.width() == 1728 and current_size.height() == 1117:
            self.RADIO_BUTTOM_SIZE_4.setChecked(True)
        else:
            self.RADIO_BUTTOM_SIZE_1.setChecked(True) 

    def create_radio_button(self, text, width, height):
        radio = widgets.QRadioButton(text)
        radio.setStyleSheet("color: white; background: transparent;")
        radio.setFont(QFont(self.font_family[0], 14))
        radio.toggled.connect(lambda checked: self.change_size(width, height) if checked else None)
        self.WINDOW_SIZE_LAYOUT.addWidget(radio)
        return radio

    def change_size(self, width, height):
        if self.main_window:
            self.main_window.resize(width, height)


        
        current_size = self.main_window.size() if self.main_window else core.QSize(1200, 800)
        if current_size.width() == 1200 and current_size.height() == 800:
            self.RADIO_BUTTOM_SIZE_1.setChecked(True)

        elif current_size.width() == 1440 and current_size.height() == 1024:
            self.RADIO_BUTTOM_SIZE_2.setChecked(True)

        elif current_size.width() == 1512 and current_size.height() == 982:
            self.RADIO_BUTTOM_SIZE_3.setChecked(True)

        elif current_size.width() == 1728 and current_size.height() == 1117:
            self.RADIO_BUTTOM_SIZE_4.setChecked(True)

        else:
            self.RADIO_BUTTOM_SIZE_1.setChecked(True)

    
        