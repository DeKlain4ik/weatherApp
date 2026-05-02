import PyQt6.QtWidgets as widgets
import PyQt6.QtCore as core
import PyQt6.QtGui as gui
from PyQt6.QtGui import QFont, QFontDatabase

from datetime import datetime, timedelta

import os

from utils import get_weather, city_request
from utils import tr, weekday_name

class TimeFrame(widgets.QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.CITY = city_request()
        
        
        self.setStyleSheet("background-color: rgba(0, 0, 0, 46); border-radius: 16px")
        self.setFixedSize(390,303)


        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        font_id = QFontDatabase.addApplicationFont(os.path.join(BASE_DIR, "..", "..", "media", "fonts", "Comfortaa-Regular.ttf"))
        font_family = QFontDatabase.applicationFontFamilies(font_id)

        self.TIME_WEATHER_FRAME = widgets.QFrame()
        self.TIME_WEATHER_FRAME.setStyleSheet("background: transparent")
        


        self.MAIN_LAYOUT = widgets.QVBoxLayout()
        self.MAIN_LAYOUT.setContentsMargins(20,20,20,20)
        self.MAIN_LAYOUT.setSpacing(0)
        
        self.setLayout(self.MAIN_LAYOUT)
        
        self.TODAY_LABEL = widgets.QLabel()
        self.TODAY_LABEL.setStyleSheet("background: transparent")
        self.TODAY_LABEL.setFixedSize(200, 30)
        self.TODAY_LABEL.setFont(QFont(font_family[0], 12))

        self.LINE_FRAME = widgets.QFrame()
        self.LINE_FRAME.setStyleSheet("background-color: rgba(255, 255, 255, 50); border-radius: 16px")

        self.LINE_FRAME.setFixedHeight(2)

        self.LINE_FRAME.setSizePolicy(
            widgets.QSizePolicy.Policy.Expanding,
            widgets.QSizePolicy.Policy.Fixed
        )

        self.DATA_LAYOUT = widgets.QHBoxLayout()
        self.DATA_LAYOUT.setContentsMargins(0, 20, 0, 10)
        self.DATA_LAYOUT.setSpacing(80)

        self.NOW = datetime.now()
        
        self.DAY = weekday_name(self.NOW)
        self.DATE = self.NOW.strftime("%d.%m.%Y")        

        self.DAY_LABEL = widgets.QLabel(text=self.DAY )

        self.DAY_LABEL.setStyleSheet("background: transparent")
        self.DAY_LABEL.setFont(QFont(font_family[0], 18))

        self.DATA_LABEL = widgets.QLabel(text=self.DATE)

        self.DATA_LABEL.setStyleSheet("background: transparent")
        self.DATA_LABEL.setFont(QFont(font_family[0], 18))
        
        self.DATA_LAYOUT.addWidget(self.DAY_LABEL)
        self.DATA_LAYOUT.addWidget(self.DATA_LABEL)

        self.IMAGE_LABEL = widgets.QLabel()
        self.IMAGE_LABEL.setFixedSize(200, 200)
        self.IMAGE_LABEL.setStyleSheet("background: transparent")

        
        self.FONT_FAMILY = font_family[0]
        
        self.TIME_FONT_SIZE = 20
        self.TIME_FONT_WEIGHT = QFont.Weight.Bold

        self.TIME_FONT_COLOR = gui.QColor('white') 
        self.clock_pixmap = gui.QPixmap("media/clock.svg").scaled(168, 168, 
                                                                core.Qt.AspectRatioMode.KeepAspectRatio, 
                                                                core.Qt.TransformationMode.SmoothTransformation)

        
        self.TIMER = core.QTimer()
        self.TIMER.timeout.connect(self.time_now)
        self.TIMER.start(1000)

        
        self.time_now()

        self.MAIN_LAYOUT.addWidget(self.TODAY_LABEL)
        self.MAIN_LAYOUT.addWidget(self.LINE_FRAME)
        
        self.MAIN_LAYOUT.addLayout(self.DATA_LAYOUT)

        self.MAIN_LAYOUT.addWidget(self.IMAGE_LABEL, alignment=core.Qt.AlignmentFlag.AlignCenter)
        
        
        self.MAIN_LAYOUT.addStretch()
        self.retranslate_ui()


    def time_now(self):
        data = get_weather(self.CITY)
        
        self.TIME_ZONE = data["city"]["timezone"]

        utc_time = datetime.utcnow()
        city_time = utc_time + timedelta(seconds=self.TIME_ZONE)

        formmated_time = city_time.strftime("%H:%M")

        combined_pixmap = gui.QPixmap(200, 200)
        combined_pixmap.fill(core.Qt.GlobalColor.transparent)

        painter = gui.QPainter(combined_pixmap)

        clock_rect = core.QRect((200 - 168) // 2, 
                                (200 - 168) // 2, 
                                168, 168)
        
        painter.drawPixmap(clock_rect, self.clock_pixmap)

        font = QFont(self.FONT_FAMILY, self.TIME_FONT_SIZE)
        font.setWeight(self.TIME_FONT_WEIGHT)
        painter.setFont(font)
        painter.setPen(self.TIME_FONT_COLOR)
        painter.drawText(combined_pixmap.rect(), core.Qt.AlignmentFlag.AlignCenter, formmated_time)
        painter.end()

        self.IMAGE_LABEL.setPixmap(combined_pixmap)

    def retranslate_ui(self):
        self.NOW = datetime.now()
        self.TODAY_LABEL.setText(tr("today"))
        self.DAY_LABEL.setText(weekday_name(self.NOW))
