import PyQt6.QtWidgets as widgets
import PyQt6.QtCore as core
import PyQt6.QtGui as gui
from PyQt6.QtGui import QFont, QFontDatabase


from datetime import datetime, timedelta

import os
import json
from utils import tr

# from .window import main_window  # Убираем циркулярный импорт


class HeadBar(widgets.QFrame):
    # Добавляем сигнал для загрузки города
    city_selected = core.pyqtSignal(str)
    open_settings_signal = core.pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        font_id = QFontDatabase.addApplicationFont(os.path.join(BASE_DIR,  "..", "media", "fonts", "Comfortaa-Regular.ttf"))
        font_family = QFontDatabase.applicationFontFamilies(font_id)

        self.setFixedSize(790, 50)
        self.setStyleSheet("background: transparent")
        

        self.MAIN_LAYOUT = widgets.QHBoxLayout(self)
        self.MAIN_LAYOUT.setAlignment(core.Qt.AlignmentFlag.AlignLeft)
        self.MAIN_LAYOUT.setContentsMargins(10, 10, 10, 0)
        self.MAIN_LAYOUT.setSpacing(10)
        self.MAIN_LAYOUT.setAlignment(core.Qt.AlignmentFlag.AlignVCenter)
        
        self.BUTTON_SETTINGS = widgets.QPushButton()
        self.BUTTON_SETTINGS.setFixedSize(36, 36)
        self.BUTTON_SETTINGS.setIcon(gui.QIcon("media/settings.svg"))
        self.BUTTON_SETTINGS.setIconSize(self.BUTTON_SETTINGS.size())
        self.BUTTON_SETTINGS.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: none;
                    border-radius: 8px;
                }

                QPushButton:hover {
                    background-color: rgba(0, 0, 0, 40);
                }

                QPushButton:pressed {
                    background-color: rgba(0, 0, 0, 80);
                }
                """)
        self.BUTTON_SETTINGS.clicked.connect(self.open_settings)
        

        self.SETTINGS_LABEL = widgets.QLabel()
        self.SETTINGS_LABEL.setStyleSheet("background-color: transparent; ")
        self.SETTINGS_LABEL.setFont(QFont(font_family[0], 16))


        
        self.SEARCH_LINE = widgets.QLineEdit()
        self.SEARCH_LINE.setFixedSize(261, 36)
        self.SEARCH_LINE.setPlaceholderText(tr("search"))
        self.SEARCH_LINE.setStyleSheet("background-color: rgba(0, 0, 0, 46); border-radius: 4px; color: white; padding-left: 10px;")
        self.SEARCH_LINE.setFont(QFont(font_family[0], 12))

        self.MODEL = core.QStringListModel()

        self.DROP_LIST = widgets.QCompleter(self.MODEL)
        self.DROP_LIST.setCaseSensitivity(core.Qt.CaseSensitivity.CaseInsensitive)
        
        self.DROP_LIST.popup().setStyleSheet("background-color: rgba(0, 0, 0, 46); border: none")
        self.DROP_LIST.setCompletionMode(widgets.QCompleter.CompletionMode.PopupCompletion)

        self.SEARCH_LINE.setCompleter(self.DROP_LIST)

        self.CITIES = self.get_cities()

        self.SEARCH_LINE.textChanged.connect(self.drop_list)

        self.MAIN_LAYOUT.addWidget(self.BUTTON_SETTINGS)
        self.MAIN_LAYOUT.addWidget(self.SETTINGS_LABEL)
        self.MAIN_LAYOUT.addWidget(self.SEARCH_LINE, alignment=core.Qt.AlignmentFlag.AlignRight)
        self.retranslate_ui()

    def open_settings(self):
        self.open_settings_signal.emit()
        

    def keyPressEvent(self, event):
        if event.key() == core.Qt.Key.Key_Return or event.key() == core.Qt.Key.Key_Enter:
            city = self.SEARCH_LINE.text().strip()
            if not city:
                return

            self.city_selected.emit(city)

    def get_cities(self):
        with open("static/json/cities.json", mode="r", encoding="utf-8") as file:
            data = json.load(file)
            return data["data"]
        
    def drop_list(self, text): 
        list = [
            city["city"] for city in self.CITIES 
            if city["city"].lower().startswith(text.lower())
        ]

        self.MODEL.setStringList(list[:10])

    def retranslate_ui(self):
        self.SETTINGS_LABEL.setText(tr("settings"))
        self.SEARCH_LINE.setPlaceholderText(tr("search"))
