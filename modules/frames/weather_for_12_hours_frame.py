import PyQt6.QtWidgets as widgets
import PyQt6.QtCore as core
import PyQt6.QtGui as gui
from PyQt6.QtGui import QFont, QFontDatabase

import os
from utils import load_icon_pixmap, tr, weather_icon_path

OWM_ICON_MAP = { 
    # Гроза 
    200: "200 386", 201: "200 386", 202: "200 386", 
    210: "200 386", 211: "200 386", 212: "200 386", 
    221: "200 386", 230: "200 386", 231: "200 386", 232: "200 386", 
    # Мряка 
    300: "263 266", 301: "263 266", 302: "263 267", 
    310: "263 266", 311: "263 266", 312: "263 267", 
    313: "296 302", 314: "296 303", 321: "263 266", 
    # Дощ 
    500: "296 302", 501: "305 356", 502: "305 357", 503: "305 357", 504: "305 357", 
    511: "311 314", 
    520: "296 302", 521: "296 303", 522: "305 357", 531: "296 303", 
    # Сніг 
    600: "326 332", 601: "326 333", 602: "338", 
    611: "317 320", 612: "317 321", 613: "317 320", 
    615: "323 329 368", 616: "323 329 369", 
    620: "326 332", 621: "326 333", 622: "338", 
    # Атмосфера 
    701: "248", 711: "248", 721: "248", 
    731: "248", 741: "248", 751: "248", 
    761: "248", 762: "248", 771: "248", 781: "248", 
    # Ясно 
    800: "113", 
    # Хмарно 
    801: "116", 802: "119 122", 803: "119 123", 804: "119 123", 
} 

OWM_ICON_MAP_NIGHT = { 
    800: "113", 
    801: "116", 802: "119 122", 803: "119 123", 804: "119 123", 
} 



def get_icon_name(weather_id: int, icon_code: str) -> str: 
    is_night = icon_code.endswith("n") 
    if is_night and weather_id in OWM_ICON_MAP_NIGHT: 
        return OWM_ICON_MAP_NIGHT[weather_id] 
    return OWM_ICON_MAP.get(weather_id, "116")


class WeatherFor12HoursFrame(widgets.QFrame):
    def __init__(self, parent):
        super().__init__(parent)

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        font_id = QFontDatabase.addApplicationFont(os.path.join(BASE_DIR, "..", "..", "media", "fonts", "Comfortaa-Regular.ttf"))
        font_family = QFontDatabase.applicationFontFamilies(font_id)


        self.DATA = {"list": [], "city": {}}
        
        self.setStyleSheet("background-color: rgba(0, 0, 0, 46); border-radius: 16px")
        self.setFixedSize(790, 197)

        self.MAIN_LAYOUT = widgets.QVBoxLayout(self)
        self.MAIN_LAYOUT.setContentsMargins(20,15,20,0)
        self.MAIN_LAYOUT.setSpacing(5)

        self.FORECAST_TEXT = widgets.QLabel()
        self.FORECAST_TEXT.setFixedSize(180, 20)
        self.FORECAST_TEXT.setStyleSheet("background: transparent;")
        self.FORECAST_TEXT.setFont(QFont(font_family[0], 12))
        self.MAIN_LAYOUT.addWidget(self.FORECAST_TEXT)
        
        self.LINE_FRAME = widgets.QFrame()
        self.MAIN_LAYOUT.addWidget(self.LINE_FRAME)
        self.LINE_FRAME.setStyleSheet("background-color: rgba(255, 255, 255, 50); border-radius: 16px")

        self.LINE_FRAME.setFixedHeight(2)

        self.LINE_FRAME.setSizePolicy(
            widgets.QSizePolicy.Policy.Expanding,
            widgets.QSizePolicy.Policy.Fixed)
        

        self.IMAGE_H_LAYOUT = widgets.QHBoxLayout()
        self.IMAGE_H_LAYOUT.setContentsMargins(0, 0, 0, 0)
        self.IMAGE_H_LAYOUT.setSpacing(10)


        self.MAIN_LAYOUT.addLayout(self.IMAGE_H_LAYOUT)

        self.GRAPHIC_H_LAYOUT = widgets.QHBoxLayout()
        self.GRAPHIC_H_LAYOUT.setContentsMargins(0, 10, 0, 0)

        self.MAIN_LAYOUT.addLayout(self.GRAPHIC_H_LAYOUT)
        
        self.GRAPHIC_FRAME = widgets.QFrame()
        self.GRAPHIC_FRAME.setFixedSize(727, 106)
        self.GRAPHIC_FRAME.setStyleSheet("background: transparent;")

        self.IMG = widgets.QLabel(self.GRAPHIC_FRAME)
        self.IMG.setFixedSize(727, 106)
        self.IMG.setStyleSheet("background: transparent;")
        
        pixmap = gui.QPixmap("media/net.svg")
        self.IMG.setPixmap(
                pixmap.scaled(
                    727, 106,
                    core.Qt.AspectRatioMode.KeepAspectRatio,
                    core.Qt.TransformationMode.SmoothTransformation))
        

        self.TEMPERATURE_GRAPH_FRAME_LAYOUT = widgets.QHBoxLayout()
        self.TEMPERATURE_GRAPH_FRAME_LAYOUT.setContentsMargins(0, 0, 0, 0)
        self.TEMPERATURE_GRAPH_FRAME_LAYOUT.setAlignment(core.Qt.AlignmentFlag.AlignBottom)
        self.GRAPHIC_FRAME.setLayout(self.TEMPERATURE_GRAPH_FRAME_LAYOUT)

        self.GRAPHIC_H_LAYOUT.addWidget(self.GRAPHIC_FRAME)


        self.NUMBERS_LAYOUT = widgets.QVBoxLayout()

        self.GRAPHIC_H_LAYOUT.addLayout(self.NUMBERS_LAYOUT)

        list_numbers = ["25°", "20°", "15°", "10°", "5°", "0°", "-5°", "-10°"]

        for i in list_numbers:
            numb = widgets.QLabel(i)
            numb.setStyleSheet("background: transparent")
            numb.setFont(QFont(font_family[0], 6))
            self.NUMBERS_LAYOUT.addWidget(numb)
        
        self.MAIN_LAYOUT.addStretch()
        self.retranslate_ui()
        
    def set_images(self):
        
        self.clear_layout(self.IMAGE_H_LAYOUT)
        self.clear_layout(self.TEMPERATURE_GRAPH_FRAME_LAYOUT)

        for i in range(21):
            list = self.DATA.get("list", [])
            img = get_icon_name(list[i]["weather"][0]["id"], list[i]["weather"][0]["icon"])

            self.IMAGE = widgets.QLabel()
            self.IMAGE.setStyleSheet("background: transparent")
            self.IMAGE.setFixedSize(16, 16)

            pixmap = load_icon_pixmap(
                weather_icon_path(f"media/icons_12hours/{img}.svg", list[i]["weather"][0]["id"]),
                16,
                16,
            )
            self.IMAGE.setPixmap(
                pixmap
            )
            self.IMAGE_H_LAYOUT.addWidget(self.IMAGE)


        for hour_data in self.DATA["list"]:
            temperature = int(hour_data["main"]["temp"])
            
            height = 0
            
            if temperature < 0 :
                height = (temperature * -2)  + 50
            elif temperature == 0:
                height = 50
            else:
                height = temperature * 2 
            
            self.COLUMN = widgets.QFrame(self.GRAPHIC_FRAME)
            self.COLUMN.setFixedSize(core.QSize(15, height))
            self.COLUMN.setStyleSheet("""
                    background: qlineargradient(
                    x1:0, y1:1, x2:1, y2:0,
                    stop:0 #87CEFA,
                    stop:1 #FFDF56
                );
            """)
            self.TEMPERATURE_GRAPH_FRAME_LAYOUT.addWidget(self.COLUMN, alignment = core.Qt.AlignmentFlag.AlignBottom)

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)  
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()  

    def retranslate_ui(self):
        self.FORECAST_TEXT.setText(tr("forecast_12_hours"))
