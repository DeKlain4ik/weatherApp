import PyQt6.QtWidgets as widgets
import PyQt6.QtCore as core
import PyQt6.QtGui as gui
from PyQt6.QtGui import QFont, QFontDatabase


class WeatherFrame(widgets.QFrame):
    def __init__(self, position, weather, city, parent=None):
        super().__init__(parent)
        
        self.setStyleSheet("background-color: rgba(0, 0, 0, 25); border-radius: 16px")
        self.setFixedSize(core.QSize(390, 303))

        icon_path="media/weather_icons/02d.svg"
        
        # вказуємо шлях до шрифту та додаємо його до бази даних шрифтів
        font_comfortaa_id = QFontDatabase.addApplicationFont("media/fonts/Comfortaa-Regular.ttf")
          
        # отримуємо ім'я шрифту за його ідентифікатором та встановлюємо його для віджетів
        font_family = QFontDatabase.applicationFontFamilies(font_comfortaa_id)

        self.central_widget = widgets.QWidget(parent=self)
        self.central_widget.setGeometry(0, 0, 390, 303)

        self.vertical_layout = widgets.QVBoxLayout()
        self.vertical_layout.setContentsMargins(0, 16, 0, 16)
        self.central_widget.setLayout(self.vertical_layout)

        self.position = widgets.QLabel(text=position)
        self.position.setStyleSheet("background: transparent")
        self.position.setFont(QFont(font_family, 16))

        self.weather_layout = widgets.QHBoxLayout()
        self.weather_layout.setContentsMargins(0, 0, 120, 0)
        self.weather_layout.setSpacing(5)
        self.weather_layout.addStretch()

        self.WEATHER_ICON = widgets.QLabel()
        self.WEATHER_ICON.setFixedSize(130, 210)
        self.WEATHER_ICON.setStyleSheet("background: transparent")

        self.weather = widgets.QLabel(text=weather)
        self.weather.setFixedWidth(90)
        self.weather.setStyleSheet("background: transparent")

        self.weather.setFont(QFont(font_family, 60))
        self.weather.setAlignment(core.Qt.AlignmentFlag.AlignCenter)

        self.weather_layout.addWidget(self.WEATHER_ICON)
        self.weather_layout.addWidget(self.weather)

        self.city = widgets.QLabel(text=city)
        self.city.setStyleSheet("background: transparent")
        self.city.setFont(QFont(font_family, 44))
        self.city.setAlignment(core.Qt.AlignmentFlag.AlignCenter)

    
        self.vertical_layout.addWidget(self.position)
        self.vertical_layout.addWidget(self.city)
        self.vertical_layout.addLayout(self.weather_layout)

    def set_text(self, position, weather, city, icon):
        self.WEATHER_ICON.setPixmap(gui.QIcon(icon).pixmap(210, 210))
        self.WEATHER_ICON.setAlignment(core.Qt.AlignmentFlag.AlignCenter)

        self.position.setText(position)
        self.city.setText(city)
        self.weather.setText(weather)