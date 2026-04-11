import PyQt6.QtWidgets as widgets
import PyQt6.QtCore as core
import PyQt6.QtGui as gui
from PyQt6.QtGui import QFont, QFontDatabase
import os

from modules import app_obj
from .pages import SearchPlace, Size, Language, Images

from .settings_titel_bar import Title_bar

class Settings(widgets.QWidget):
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.setFixedSize(790, 688)

        self.setWindowFlags(core.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(core.Qt.WidgetAttribute.WA_TranslucentBackground)

        self.main_window = main_window

        self.container = widgets.QFrame(self)
        self.container.setGeometry(self.rect())

        self.container.setStyleSheet("""
            background-color: rgba(0, 0, 0, 190);
            border-radius: 16px;
        """)



        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        font_id = QFontDatabase.addApplicationFont(os.path.join(BASE_DIR, "..", "media", "fonts", "Comfortaa-Regular.ttf"))
        font_family = QFontDatabase.applicationFontFamilies(font_id)
        
        self.CENTRAL_LAYOUT = widgets.QVBoxLayout(self)
        self.CENTRAL_LAYOUT.setContentsMargins(10, 30, 10, 10)
        self.CENTRAL_LAYOUT.setSpacing(0)



        self.TITLE_BAR = Title_bar(self, width = 790)
        self.CENTRAL_LAYOUT.addWidget(self.TITLE_BAR, alignment = core.Qt.AlignmentFlag.AlignTop)

        self.MAIN_LAYOUT = widgets.QHBoxLayout()
        self.MAIN_LAYOUT.setContentsMargins(0, 0, 0, 0)
        self.MAIN_LAYOUT.setSpacing(10)
        self.CENTRAL_LAYOUT.addLayout(self.MAIN_LAYOUT)

        self.LEFT_SCROLL_AREA = widgets.QScrollArea()
        self.LEFT_SCROLL_AREA.setWidgetResizable(True)
        self.LEFT_SCROLL_AREA.setFrameShape(widgets.QFrame.Shape.NoFrame)
        self.LEFT_SCROLL_AREA.setVerticalScrollBarPolicy(core.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.LEFT_SCROLL_AREA.setHorizontalScrollBarPolicy(core.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.LEFT_SCROLL_AREA.setFixedWidth(200)
        self.LEFT_SCROLL_AREA.setFixedHeight(600)
        self.LEFT_SCROLL_AREA.setStyleSheet("background: transparent; border: none;")
        
        self.content = widgets.QFrame()

        self.SCROLL_LAYOUT = widgets.QVBoxLayout(self.content)
        self.SCROLL_LAYOUT.setAlignment(core.Qt.AlignmentFlag.AlignTop)
        self.SCROLL_LAYOUT.setSpacing(10)

        self.LEFT_SCROLL_AREA.setWidget(self.content)

        self.buttons_dict = {}
        self.button_list = []
        
        button_names = ["Пошук міста", "Розмір додатку", "Мова додатку", "Списки зображень"]
        
        for idx, name in enumerate(button_names):
            btn = widgets.QPushButton(name)
            btn.setFont(QFont(font_family[0], 14))
            btn.setStyleSheet("background: transparent; color: rgba(255,255,255,150); border: none; text-align: left; padding: 10px;")
            btn.setCursor(core.Qt.CursorShape.PointingHandCursor)
            btn.setObjectName(name)
            self.SCROLL_LAYOUT.addWidget(btn, alignment=core.Qt.AlignmentFlag.AlignTop)
            self.buttons_dict[name] = btn
            self.button_list.append(btn)
        
        self.button_list[0].clicked.connect(self.on_button_0_clicked)
        self.button_list[1].clicked.connect(self.on_button_1_clicked)
        self.button_list[2].clicked.connect(self.on_button_2_clicked)
        self.button_list[3].clicked.connect(self.on_button_3_clicked)

        

        self.LINE_FRAME = widgets.QFrame()
        self.LINE_FRAME.setFixedWidth(2)
        self.LINE_FRAME.setSizePolicy(
            widgets.QSizePolicy.Policy.Fixed,
            widgets.QSizePolicy.Policy.Expanding
        )
        self.LINE_FRAME.setStyleSheet("background-color: rgba(255, 255, 255, 50); border-radius: 1px;")

        # QStackedWidget для переключения страниц
        self.pages_widget = widgets.QStackedWidget()
        
        self.MAIN_LAYOUT.addWidget(self.LEFT_SCROLL_AREA)
        self.MAIN_LAYOUT.addWidget(self.LINE_FRAME)
        self.MAIN_LAYOUT.addWidget(self.pages_widget)


        self.MAIN_LAYOUT.setStretch(0, 0)  
        self.MAIN_LAYOUT.setStretch(1, 0)  
        self.MAIN_LAYOUT.setStretch(2, 1)
        self.CENTRAL_LAYOUT.addStretch()

        self.pages_widget.setStyleSheet("background: transparent;")

        self.pages_widget.addWidget(SearchPlace(main_window = self.main_window, parent=self)) 
        self.pages_widget.addWidget(Size(self))  
        self.pages_widget.addWidget(Language(self))  
        self.pages_widget.addWidget(Images(self)) 
        
        self.show_page(0)
    
    def show_page(self, index):
        self.pages_widget.setCurrentIndex(index)
        for btn in self.button_list:
            btn.setStyleSheet("background: transparent; color: rgba(255,255,255,150); border: none; text-align: left; padding: 10px;")
        self.button_list[index].setStyleSheet("background: rgba(100, 150, 255, 150); color: white; border: none; text-align: left; padding: 10px; border-radius: 8px;")
    
    def on_button_0_clicked(self):
        self.show_page(0)

    
    def on_button_1_clicked(self):
        self.show_page(1)
    
    def on_button_2_clicked(self):
        self.show_page(2)
    
    def on_button_3_clicked(self):
        self.show_page(3)
    
 

    def closeEvent(self, event):
        if hasattr(self, 'main_window') and self.main_window is not None:
            self.main_window.WINDOW_CONTAINER.setGraphicsEffect(None)
        super().closeEvent(event)