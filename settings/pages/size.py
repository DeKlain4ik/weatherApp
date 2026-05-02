import PyQt6.QtWidgets as widgets
import PyQt6.QtCore as core
import PyQt6.QtGui as gui
from PyQt6.QtGui import QFont, QFontDatabase
import os
from utils import tr


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

        self.label = widgets.QLabel()
        self.label.setFont(QFont(self.font_family[0], 18))
        self.label.setStyleSheet("background: transparent;")
        self.CENTRAL_LAYOUT.addWidget(self.label, alignment=core.Qt.AlignmentFlag.AlignTop | core.Qt.AlignmentFlag.AlignLeft)

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

        self.SAVE_BUTTON_SIZE = widgets.QPushButton()
        self.SAVE_BUTTON_SIZE.setFixedSize(120,40)
        self.SAVE_BUTTON_SIZE.setFont(QFont(self.font_family[0], 12))
        self.SAVE_BUTTON_SIZE.setStyleSheet("background-color:rgba(0, 0, 0, 46)")
        self.SAVE_BUTTON_SIZE.clicked.connect(self.save_button_function)
        self.WINDOW_SIZE_LAYOUT.addWidget(self.SAVE_BUTTON_SIZE)
        self.retranslate_ui()

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

    def retranslate_ui(self):
        self.label.setText(tr("app_size"))
        self.SAVE_BUTTON_SIZE.setText(tr("save"))

    def save_button_function(self):
        if self.RADIO_BUTTOM_SIZE_1.isChecked():
            self.change_size(1200, 800)
            
        elif self.RADIO_BUTTOM_SIZE_2.isChecked():
            self.change_size(1440, 1024)
            
        elif self.RADIO_BUTTOM_SIZE_3.isChecked():
            self.change_size(1512, 982)
            
        elif self.RADIO_BUTTOM_SIZE_4.isChecked():
            self.change_size(1728, 1117)

    def create_radio_button(self, text, width, height):
        radio = widgets.QRadioButton(text)
        radio.setStyleSheet("color: white; background: transparent;")
        radio.setFont(QFont(self.font_family[0], 14))
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
        
