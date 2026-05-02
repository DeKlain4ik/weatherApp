import PyQt6.QtWidgets as widgets
import PyQt6.QtCore as core
import PyQt6.QtGui as gui
from PyQt6.QtGui import QFont, QFontDatabase
import os
from utils import LANGUAGE_NAMES, get_language, set_language, tr


class Language(widgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setAttribute(core.Qt.WidgetAttribute.WA_TranslucentBackground)

        self.setStyleSheet("background: transparent; border-radius: 16px;")

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        font_id = QFontDatabase.addApplicationFont(os.path.join(BASE_DIR, "..", "..", "media", "fonts", "Comfortaa-Regular.ttf"))
        font_family = QFontDatabase.applicationFontFamilies(font_id)
        
        self.CENTRAL_LAYOUT = widgets.QVBoxLayout(self)
        self.CENTRAL_LAYOUT.setContentsMargins(10, 30, 10, 10)
        self.CENTRAL_LAYOUT.setSpacing(30)

        self.label = widgets.QLabel()
        self.label.setFont(QFont(font_family[0], 18))
        self.label.setStyleSheet("background: transparent;")
        self.CENTRAL_LAYOUT.addWidget(self.label, alignment=core.Qt.AlignmentFlag.AlignTop | core.Qt.AlignmentFlag.AlignLeft)

        self.label2 = widgets.QLabel()
        self.label2.setFont(QFont(font_family[0], 12))
        self.label2.setStyleSheet("background: transparent")
        self.CENTRAL_LAYOUT.addWidget(self.label2)

        self.languages = widgets.QComboBox()
        self.languages.setStyleSheet("background-color:rgba(0, 0, 0, 146); border-radius: 16px; padding: 5px;")
        self.languages.setFixedSize(200, 30)
        for code, name in LANGUAGE_NAMES.items():
            self.languages.addItem(name, code)
        current_index = self.languages.findData(get_language())
        if current_index >= 0:
            self.languages.setCurrentIndex(current_index)
        self.languages.setFont(QFont(font_family[0], 10))
        self.CENTRAL_LAYOUT.addWidget(self.languages, alignment=core.Qt.AlignmentFlag.AlignLeft)

        self.button = widgets.QPushButton()
        self.button.setFont(QFont(font_family[0], 12))
        self.button.setFixedSize(120, 40)
        self.button.setStyleSheet("background-color:rgba(0, 0, 0, 46)")
        self.button.clicked.connect(self.save_language)
        self.CENTRAL_LAYOUT.addWidget(self.button, alignment=core.Qt.AlignmentFlag.AlignLeft)

        self.CENTRAL_LAYOUT.addStretch()
        self.retranslate_ui()

    def save_language(self):
        selected_language = self.languages.currentData()
        set_language(selected_language)

        settings_window = self.window()
        if hasattr(settings_window, "retranslate_ui"):
            settings_window.retranslate_ui()

        main_window = getattr(settings_window, "main_window", None)
        if main_window and hasattr(main_window, "retranslate_ui"):
            main_window.retranslate_ui()

    def retranslate_ui(self):
        self.label.setText(tr("choose_app_language"))
        self.label2.setText(tr("app_language"))
        self.button.setText(tr("save"))
