from PyQt6 import QtCore as core 
from PyQt6 import QtWidgets as widgets
import PyQt6.QtGui as gui



class Title_bar(widgets.QFrame):
    def __init__(self, parent, width):
        widgets.QFrame.__init__(self, parent = parent)
        
        self.LAYOUT = widgets.QHBoxLayout()
        self.LAYOUT.setAlignment(core.Qt.AlignmentFlag.AlignTop)
        self.LAYOUT.setContentsMargins(10, 0, 10, 0)
        
        self.setLayout(self.LAYOUT)
        
        self.setFixedSize(core.QSize(width, 40))
        self.setStyleSheet("background-color: rgba(0, 0, 0, 80); border-top-left-radius: 16px; border-top-right-radius: 16px;")
        
        self.BUTTONS_FRAME = widgets.QFrame(parent = self)
        self.BUTTONS_FRAME.setStyleSheet("background-color: transparent; ")
        self.BUTTONS_FRAME.setFixedSize(150, 50)
        
        self.LAYOUT.addWidget(self.BUTTONS_FRAME)
        
        self.WINDOW = self.window()
        
        self.BUTTONS_FRAME_LAYOUT = widgets.QHBoxLayout()
        self.BUTTONS_FRAME_LAYOUT.setContentsMargins(0, 0, 0, 7)
        self.BUTTONS_FRAME_LAYOUT.setAlignment(core.Qt.AlignmentFlag.AlignVCenter)
        self.BUTTONS_FRAME.setLayout(self.BUTTONS_FRAME_LAYOUT)
        
        self.CLOSE_BUTTON = widgets.QToolButton(parent = self.BUTTONS_FRAME)
        icon = gui.QIcon("media/title_bar/Close_Button.svg")
        self.CLOSE_BUTTON.setIcon(icon)
        self.CLOSE_BUTTON.setStyleSheet("border: none; ")
        self.CLOSE_BUTTON.clicked.connect(self.WINDOW.close)
        
        self.MIN_BUTTON = widgets.QToolButton(parent = self.BUTTONS_FRAME)
        icon = gui.QIcon("media/title_bar/Minimize_Button.svg")
        self.MIN_BUTTON.setIcon(icon)
        self.MIN_BUTTON.setStyleSheet("border: none; ")
        self.MIN_BUTTON.clicked.connect(self.WINDOW.showMinimized)
        
        self.MAX_BUTTON = widgets.QToolButton(parent = self.BUTTONS_FRAME)
        icon = gui.QIcon("media/title_bar/Maximize_Button.svg")
        self.MAX_BUTTON.setIcon(icon)
        self.MAX_BUTTON.setStyleSheet("border: none; ")
        self.MAX_BUTTON.clicked.connect(self.WINDOW.showMaximized)
        
        self.BUTTONS_FRAME_LAYOUT.addWidget(self.CLOSE_BUTTON)
        self.BUTTONS_FRAME_LAYOUT.addWidget(self.MIN_BUTTON)
        self.BUTTONS_FRAME_LAYOUT.addWidget(self.MAX_BUTTON)
    
    
    def mousePressEvent(self, event: gui.QMouseEvent):
        if event.button() == core.Qt.MouseButton.LeftButton:
            self.POS = event.position().toPoint()
    
    def mouseMoveEvent(self, event: gui.QMouseEvent):
        
        pos = event.position().toPoint() - self.POS
        
        self.WINDOW.move(
            self.WINDOW.x() + pos.x(),
            self.WINDOW.y() + pos.y()
        )
