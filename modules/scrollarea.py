import PyQt6.QtCore as core
import PyQt6.QtWidgets as widgets




class ScrollArea(widgets.QScrollArea):
    def __init__(self, parent):
        super().__init__(parent)

        
        self.setMinimumWidth(320)
        self.setWidgetResizable(True)
        
        self.setWidgetResizable(True)

        self.setFrameShape(widgets.QFrame.Shape.NoFrame)

        self.setVerticalScrollBarPolicy(core.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        
        self.setStyleSheet("background: transparent")

        self.content = widgets.QFrame()

        self.SCROLL_LAYOUT = widgets.QVBoxLayout(self.content)
        self.SCROLL_LAYOUT.setAlignment(core.Qt.AlignmentFlag.AlignTop)

        self.setWidget(self.content)