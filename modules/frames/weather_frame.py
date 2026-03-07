import PyQt6.QtWidgets as widgets
import PyQt6.QtCore as core
import PyQt6.QtGui as gui
from PyQt6.QtGui import QFont, QFontDatabase


class WeatherFrame(widgets.QFrame):
    def __init__(self, position, weather, city, parent=None):
        super().__init__(parent)
        
        self.setStyleSheet("background-color: rgba(0, 0, 0, 46); border-radius: 16px")
        self.setFixedSize(390,303)

        self.CURENT_POSITON_CHECK = False
       
        font_id = QFontDatabase.addApplicationFont("media/fonts/Comfortaa-Regular.ttf")
        font_family = QFontDatabase.applicationFontFamilies(font_id)

        
        self.main_layout = widgets.QVBoxLayout(self)
        self.main_layout.setContentsMargins(16, 16, 16, 16)
        self.main_layout.setSpacing(4)
        self.main_layout.setAlignment(core.Qt.AlignmentFlag.AlignCenter)



        self.CURRENT_POSITION_LABEL = widgets.QLabel()
        self.CURRENT_POSITION_LABEL.setStyleSheet("background: transparent")
        self.CURRENT_POSITION_LABEL.setFixedSize(200, 30)
        self.CURRENT_POSITION_LABEL.setFont(QFont(font_family[0], 12))

        self.LINE_FRAME = widgets.QFrame()
        self.LINE_FRAME.setStyleSheet("background-color: rgba(255, 255, 255, 0); border-radius: 16px")

        self.LINE_FRAME.setFixedHeight(2)

        self.LINE_FRAME.setSizePolicy(
            widgets.QSizePolicy.Policy.Expanding,
            widgets.QSizePolicy.Policy.Fixed
        )


        
        self.city_label = widgets.QLabel(city or "")
        self.city_label.setAlignment(core.Qt.AlignmentFlag.AlignCenter)
        self.city_label.setFont(QFont(font_family[0], 36))
        self.city_label.setStyleSheet("background: transparent; color: white")

       
        self.weather_layout = widgets.QHBoxLayout()
        self.weather_layout.setSpacing(0)
        self.weather_layout.setContentsMargins(0, 0, 0, 0)
        self.weather_layout.setAlignment(core.Qt.AlignmentFlag.AlignHCenter | core.Qt.AlignmentFlag.AlignVCenter)


        self.icon_label = widgets.QLabel()
        self.icon_label.setFixedSize(150, 150)
        self.icon_label.setStyleSheet("background: transparent")
        

        self.temp_label = widgets.QLabel(weather or "")
        self.temp_label.setFont(QFont(font_family[0], 48))
        self.temp_label.setStyleSheet("background: transparent; color: white; font-size: 80px")
        self.temp_label.setAlignment(core.Qt.AlignmentFlag.AlignVCenter)

        self.weather_layout.addWidget(self.icon_label)
        self.weather_layout.addWidget(self.temp_label)

       
        self.description_label = widgets.QLabel("")
        self.description_label.setAlignment(core.Qt.AlignmentFlag.AlignCenter)
        self.description_label.setFont(QFont(font_family[0], 14))
        self.description_label.setStyleSheet("background: transparent; color: white")

        
        self.minmax_label = widgets.QLabel("")
        self.minmax_label.setAlignment(core.Qt.AlignmentFlag.AlignCenter)
        self.minmax_label.setFont(QFont(font_family[0], 12))
        self.minmax_label.setStyleSheet("background: transparent; color: rgba(255,255,255,180)")

        self.main_layout.addWidget(self.CURRENT_POSITION_LABEL)
        self.main_layout.addWidget(self.LINE_FRAME)
        
        self.main_layout.addWidget(self.city_label)
        self.main_layout.addLayout(self.weather_layout)
        self.main_layout.addWidget(self.description_label)
        self.main_layout.addWidget(self.minmax_label)


    def curent_position(self):
        if self.CURENT_POSITON_CHECK:
            self.CURRENT_POSITION_LABEL.setText("Поточна позиція")
            self.LINE_FRAME.setStyleSheet("background-color: rgba(255, 255, 255, 50); border-radius: 16px")

        else:
            self.CURRENT_POSITION_LABEL.setText("")
            self.LINE_FRAME.setStyleSheet("background-color: rgba(255, 255, 255, 0); border-radius: 16px")




    def set_text(self, city, weather, icon, description="", max_temp="", min_temp="", position=None):
        self.city_label.setText(city or "")
        self.temp_label.setText(weather or "")
        self.description_label.setText(description)

        
        if max_temp and min_temp:
            self.minmax_label.setText(f"Макс.: {max_temp}°, мин.: {min_temp}°")

        
        pixmap = gui.QPixmap(icon)
        self.icon_label.setPixmap(
            pixmap.scaled(
                150, 150,
                core.Qt.AspectRatioMode.KeepAspectRatio,
                core.Qt.TransformationMode.SmoothTransformation
            )
        )
        self.icon_label.setAlignment(core.Qt.AlignmentFlag.AlignCenter)