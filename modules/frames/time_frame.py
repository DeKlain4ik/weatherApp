import PyQt6.QtWidgets as widgets
import PyQt6.QtCore as core
import PyQt6.QtGui as gui


class TimeFrame(widgets.QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        
        self.setStyleSheet("background-color: rgba(0, 0, 0, 46); border-radius: 16px")
        self.setFixedSize(core.QSize(390, 303))