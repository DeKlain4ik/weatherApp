import PyQt6.QtWidgets as widgets
import PyQt6.QtCore as core
import PyQt6.QtGui as gui
from PyQt6.QtGui import QFont, QFontDatabase
import os
from utils import get_image_set, load_icon_pixmap, set_image_set, tr


class Images(widgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setAttribute(core.Qt.WidgetAttribute.WA_TranslucentBackground)

        self.setStyleSheet("background: transparent; border-radius: 16px;")

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        font_id = QFontDatabase.addApplicationFont(os.path.join(BASE_DIR, "..", "..", "media", "fonts", "Comfortaa-Regular.ttf"))
        font_family = QFontDatabase.applicationFontFamilies(font_id)
        self.main_window = parent.main_window if parent else None
        self.selected_image_set = get_image_set()
        
        self.CENTRAL_LAYOUT = widgets.QVBoxLayout(self)
        self.CENTRAL_LAYOUT.setContentsMargins(20, 30, 20, 20)
        self.CENTRAL_LAYOUT.setSpacing(20)
        
        self.label = widgets.QLabel()
        self.label.setFont(QFont(font_family[0], 18))
        self.label.setStyleSheet("background: transparent;")
        self.CENTRAL_LAYOUT.addWidget(self.label, alignment=core.Qt.AlignmentFlag.AlignTop | core.Qt.AlignmentFlag.AlignLeft)

        self.buttonAdd = widgets.QPushButton()
        self.buttonAdd.setFont(QFont(font_family[0], 12))
        self.buttonAdd.setStyleSheet("""
                            QPushButton {
                                    background-color: rgba(0, 0, 0, 46); 
                                    border-radius: 8px;
                                    }
                            QPushButton:hover {
                                    background-color: rgba(0, 0, 0, 86);
                                    }


                                    """)
        self.buttonAdd.setFixedSize(97,36)

        self.buttonAdd.setIcon(gui.QIcon(os.path.join(BASE_DIR, "..", "..", "media", "add.svg")))
        self.CENTRAL_LAYOUT.addWidget(self.buttonAdd, alignment=core.Qt.AlignmentFlag.AlignTop | core.Qt.AlignmentFlag.AlignLeft)

        self.farme1 = widgets.QFrame()
        self.farme1.setFixedSize(490,136)
        self.farme1.setCursor(core.Qt.CursorShape.PointingHandCursor)
        self.farme1.mousePressEvent = lambda event: self.select_image_set("set_2")
        self.CENTRAL_LAYOUT.addWidget(self.farme1, alignment=core.Qt.AlignmentFlag.AlignTop | core.Qt.AlignmentFlag.AlignLeft)

        self.FARME1_MAIN_LAYOUT = widgets.QVBoxLayout(self.farme1)
        self.farme1.setLayout(self.FARME1_MAIN_LAYOUT)

        self.farme1_layout = widgets.QHBoxLayout()
        self.farme1_layout.setSpacing(20)
        self.farme1_layout.setAlignment(core.Qt.AlignmentFlag.AlignCenter)

        self.list_images_label = widgets.QLabel()
        self.list_images_label.setFont(QFont(font_family[0], 14))
        self.list_images_label.setStyleSheet("background: transparent;")
        
        self.FARME1_MAIN_LAYOUT.addWidget(self.list_images_label)
        self.FARME1_MAIN_LAYOUT.addLayout(self.farme1_layout)

        icons_n2_examples = [
            "0.svg",
            "1.svg",
            "2.svg",
            "3.svg",
            "4.svg",
        ]
        for icon_name in icons_n2_examples:
            label = widgets.QLabel()
            label.setPixmap(load_icon_pixmap(os.path.join(BASE_DIR, "..", "..", "media", "icons_N2", icon_name), 74, 74))
            label.setStyleSheet("background: transparent;")
            self.farme1_layout.addWidget(label)

        

        self.farme2 = widgets.QFrame()
        self.farme2.setFixedSize(490,136)
        self.farme2.setCursor(core.Qt.CursorShape.PointingHandCursor)
        self.farme2.mousePressEvent = lambda event: self.select_image_set("set_1")
        self.CENTRAL_LAYOUT.addWidget(self.farme2, alignment=core.Qt.AlignmentFlag.AlignTop | core.Qt.AlignmentFlag.AlignLeft)

        self.FARME2_MAIN_LAYOUT = widgets.QVBoxLayout(self.farme2)
        self.farme2.setLayout(self.FARME2_MAIN_LAYOUT)

        self.farme2_layout = widgets.QHBoxLayout()
        self.farme2_layout.setSpacing(20)
        self.farme2_layout.setAlignment(core.Qt.AlignmentFlag.AlignCenter)

        self.list_images_label2 = widgets.QLabel()
        self.list_images_label2.setFont(QFont(font_family[0], 14))
        self.list_images_label2.setStyleSheet("background: transparent;")
        
        self.FARME2_MAIN_LAYOUT.addWidget(self.list_images_label2)
        self.FARME2_MAIN_LAYOUT.addLayout(self.farme2_layout)

        icons_n1_examples = [
            "0.svg",
            "1.svg",
            "2.svg",
            "3.svg",
            "4.svg",
        ]
        for icon_name in icons_n1_examples:
            label2 = widgets.QLabel()
            label2.setPixmap(load_icon_pixmap(os.path.join(BASE_DIR, "..", "..", "media", "icons_N1", icon_name), 74, 74))
            label2.setStyleSheet("background: transparent;")
            self.farme2_layout.addWidget(label2)
        

        self.save_button = widgets.QPushButton()
        self.save_button.setFont(QFont(font_family[0], 12))
        self.save_button.setFixedSize(97,36)

        self.save_button.setStyleSheet("""
                            QPushButton {
                                    background-color: rgba(0, 0, 0, 46); 
                                    border-radius: 8px;
                                    }
                            QPushButton:hover {
                                    background-color: rgba(0, 0, 0, 86);
                                    }
                                    """)
        self.save_button.clicked.connect(self.save_image_set)
        self.CENTRAL_LAYOUT.addWidget(self.save_button, alignment=core.Qt.AlignmentFlag.AlignTop | core.Qt.AlignmentFlag.AlignLeft)

        self.CENTRAL_LAYOUT.addStretch()
        self.retranslate_ui()
        self.update_selected_styles()

    def retranslate_ui(self):
        self.label.setText(tr("image_lists"))
        self.buttonAdd.setText(tr("add"))
        self.list_images_label.setText(tr("images_lists2"))
        self.list_images_label2.setText(tr("images_lists1"))
        self.save_button.setText(tr("save"))

    def select_image_set(self, image_set):
        self.selected_image_set = image_set
        self.update_selected_styles()

    def save_image_set(self):
        set_image_set(self.selected_image_set)
        if self.main_window and hasattr(self.main_window, "refresh_weather_icons"):
            self.main_window.refresh_weather_icons()

    def update_selected_styles(self):
        normal_style = """
            QFrame {
                background-color: rgba(0, 0, 0, 46);
                border: 1px solid rgba(255, 255, 255, 35);
                border-radius: 8px;
            }
            QFrame:hover {
                background-color: rgba(0, 0, 0, 86);
            }
        """
        selected_style = """
            QFrame {
                background-color: rgba(100, 150, 255, 135);
                border: 2px solid rgba(255, 255, 255, 210);
                border-radius: 8px;
            }
            QFrame:hover {
                background-color: rgba(100, 150, 255, 170);
            }
        """
        self.farme1.setStyleSheet(selected_style if self.selected_image_set == "set_2" else normal_style)
        self.farme2.setStyleSheet(selected_style if self.selected_image_set == "set_1" else normal_style)
