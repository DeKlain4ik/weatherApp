import PyQt6.QtCore as core
import PyQt6.QtWidgets as widgets
from PyQt6.QtGui import QFont, QFontDatabase
import PyQt6.QtGui as gui
from utils import city_request, get_weather

from datetime import datetime, timedelta

class Cards_widget(widgets.QFrame):
     # створюємо об'єкт сигналу
     frame_clicked = core.pyqtSignal(object)

     def __init__(self, parent, id: int, city_name: str, is_first=False):
          super().__init__(parent)

          self.CITY_NAME = city_name 


          self.ID = id

          self.clicked = False
          self.normalColor()

          
          # вказуємо шлях до шрифту та додаємо його до бази даних шрифтів
          font_comfortaa_id = QFontDatabase.addApplicationFont("media/fonts/Comfortaa-Regular.ttf")
          
          # отримуємо ім'я шрифту за його ідентифікатором та встановлюємо його для віджетів
          font_family = QFontDatabase.applicationFontFamilies(font_comfortaa_id)


          self.setFixedSize(core.QSize(330,90))

          
          self.LEFT_RIGHT_LAYOUT = widgets.QHBoxLayout(self)
          
          self.LEFT_LAYOUT = widgets.QVBoxLayout()
          self.LEFT_LAYOUT.setSpacing(2)

          self.RIGHT_LAYOUT = widgets.QVBoxLayout()
          self.RIGHT_LAYOUT.setSpacing(2)

          self.ARROW_LAYOUT = widgets.QHBoxLayout()
          self.ARROW_LAYOUT.setContentsMargins(0, 0, 0, 0)

          self.ARROW_LABEL_ICON = widgets.QLabel()
          self.ARROW_LABEL_ICON.setFixedWidth(20)
          self.ARROW_LABEL_ICON.setStyleSheet("background: transparent")
          self.ARROW_LABEL_ICON.setPixmap(gui.QIcon("media/Vector.svg").pixmap(15, 15))

          
          self.LABEL_CITY_NAME = widgets.QLabel(city_name)
          self.LABEL_CITY_NAME.setStyleSheet("font-size: 24px; background: transparent; ")
          self.LABEL_CITY_NAME.setFont(QFont(font_family,weight = 24))

          self.LABEL_CITY_TIME = widgets.QLabel()   
          self.LABEL_CITY_TIME.setStyleSheet("font-size: 12px; background: transparent;")
          self.LABEL_CITY_TIME.setFont(QFont(font_family, 12))
          
          self.LABEL_CITY_WEATHER = widgets.QLabel() 
          self.LABEL_CITY_WEATHER.setStyleSheet("font-size: 12px; background: transparent;")
          self.LABEL_CITY_WEATHER.setFont(QFont(font_family, 12))
          

          self.LEFT_LAYOUT.addLayout(self.ARROW_LAYOUT)
         
          if is_first:
               self.CITY_NAME = city_request()
               self.LABEL_CITY_NAME.setText(self.CITY_NAME)
               self.ARROW_LAYOUT.addWidget(self.ARROW_LABEL_ICON)

          self.ARROW_LAYOUT.addWidget(self.LABEL_CITY_NAME)


          self.LEFT_LAYOUT.addWidget(self.LABEL_CITY_TIME)
          self.LEFT_LAYOUT.addWidget(self.LABEL_CITY_WEATHER)


          self.CITY_TEMPERATURE = widgets.QLabel(self)   
          self.CITY_TEMPERATURE.setStyleSheet("font-size: 40px; background: transparent;")
          self.CITY_TEMPERATURE.setFont(QFont(font_family, 40))

          
          self.MAX_MIN_TEMPERATURE = widgets.QLabel()
          self.MAX_MIN_TEMPERATURE.setStyleSheet("font-size: 12px; background: transparent")
          self.MAX_MIN_TEMPERATURE.setFont(QFont(font_family, 12))

          self.load_weather()
          self.update_time()

          self.TIMER = core.QTimer()
          self.TIMER.timeout.connect(self.update_time)
          self.TIMER.start(1000)

          self.RIGHT_LAYOUT.addWidget(self.CITY_TEMPERATURE)
          self.RIGHT_LAYOUT.addWidget(self.MAX_MIN_TEMPERATURE)
     


          self.LEFT_RIGHT_LAYOUT.addLayout(self.LEFT_LAYOUT)
          self.LEFT_RIGHT_LAYOUT.addLayout(self.RIGHT_LAYOUT)

          
         


     def mousePressEvent(self, event : gui.QMouseEvent):
          pressed_button = event.button()
          if pressed_button == core.Qt.MouseButton.LeftButton:
              self.clicked = not self.clicked
              self.clcikedColor()
              self.load_weather()
              #оголошуємо сигнал
              self.frame_clicked.emit(self)
              
     

     def load_weather(self):
          data = get_weather(self.CITY_NAME)
          
          if data is None:
               self.LABEL_CITY_WEATHER.setText("ошибка")
               self.CITY_TEMPERATURE.setText("—°")
               self.MAX_MIN_TEMPERATURE.setText("Max: —, Min: —")
               return

          temp = round(data["list"][0]["main"]["temp"])
          self.weather_description = data["list"][0]["weather"][0]["description"]
          self.max_temp = round(data["list"][0]["main"]["temp_max"])
          self.min_temp = round(data["list"][0]["main"]["temp_min"])
          
          self.TIME_ZONE = data["city"]["timezone"]
          
          self.CITY_TEMPERATURE.setText(f"{temp}°")
          self.LABEL_CITY_WEATHER.setText(self.weather_description)
          self.MAX_MIN_TEMPERATURE.setText(f"Max.: {self.max_temp}, Min.: {self.min_temp}")

          self.TEMP = temp



     def update_time(self):
          if self.TIME_ZONE:
               utc_time = datetime.utcnow()
               city_time = utc_time + timedelta(seconds=self.TIME_ZONE)

               formmated_time = city_time.strftime("%H:%M")

               self.LABEL_CITY_TIME.setText(formmated_time)
               
             

     def clcikedColor(self):
          self.setStyleSheet("background-color: rgba(0, 0, 0, 150); border-radius: 12px")

     def normalColor(self):
          self.setStyleSheet("""
                              QFrame {
                                   background: transparent;
                                   border-radius: 12px;
                              }
                              QFrame:hover{
                                   background-color: rgba(0, 0, 0, 76);
                              }
                              
                              """)
          