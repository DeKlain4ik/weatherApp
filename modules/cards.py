import PyQt6.QtCore as core
import PyQt6.QtWidgets as widgets
from PyQt6.QtGui import QFont, QFontDatabase
import PyQt6.QtGui as gui
# from PyQt6.QtGui import QPixmap

class Cards_widget(widgets.QFrame):
     def __init__(self, parent, city_name: str, time: str, weather: str, temp: str, max_temp: str, min_temp: str, is_first = False):
          super().__init__(parent)
          
          # вказуємо шлях до шрифту та додаємо його до бази даних шрифтів
          font_comfortaa_id = QFontDatabase.addApplicationFont("media/fonts/Comfortaa-Regular.ttf")
          
          # отримуємо ім'я шрифту за його ідентифікатором та встановлюємо його для віджетів
          font_family = QFontDatabase.applicationFontFamilies(font_comfortaa_id)


          self.setFixedSize(core.QSize(330,90))

          self.setStyleSheet("""
                              QFrame {
                                   background: transparent;
                                   border-radius: 12px;
                              }
                              QFrame:hover{
                                   background-color: rgba(0, 0, 0, 76);
                              }
                              """)
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
          self.LABEL_CITY_NAME.setStyleSheet("font-size: 24px; background: transparent;")
          self.LABEL_CITY_NAME.setFont(QFont(font_family,weight = 24))

          self.LABEL_CITY_TIME = widgets.QLabel(time)   
          self.LABEL_CITY_TIME.setStyleSheet("font-size: 12px; background: transparent;")
          self.LABEL_CITY_TIME.setFont(QFont(font_family, 12))

          self.LABEL_CITY_WEATHER = widgets.QLabel(weather) 
          self.LABEL_CITY_WEATHER.setStyleSheet("font-size: 12px; background: transparent;")
          self.LABEL_CITY_WEATHER.setFont(QFont(font_family, 12))
          

          self.LEFT_LAYOUT.addLayout(self.ARROW_LAYOUT)
         
          if is_first:
               self.ARROW_LAYOUT.addWidget(self.ARROW_LABEL_ICON)

          self.ARROW_LAYOUT.addWidget(self.LABEL_CITY_NAME)


          self.LEFT_LAYOUT.addWidget(self.LABEL_CITY_TIME)
          self.LEFT_LAYOUT.addWidget(self.LABEL_CITY_WEATHER)


          self.CITY_TEMPERATURE = widgets.QLabel(f"{temp}°", self)   
          self.CITY_TEMPERATURE.setStyleSheet("font-size: 40px; background: transparent;")
          self.CITY_TEMPERATURE.setFont(QFont(font_family, 40))

          
          self.MAX_MIN_TEMPERATURE = widgets.QLabel(f"Max.:{max_temp}, Min.:{min_temp}")
          self.MAX_MIN_TEMPERATURE.setStyleSheet("font-size: 12px; background: transparent")
          self.MAX_MIN_TEMPERATURE.setFont(QFont(font_family, 12))

          self.RIGHT_LAYOUT.addWidget(self.CITY_TEMPERATURE)
          self.RIGHT_LAYOUT.addWidget(self.MAX_MIN_TEMPERATURE)
     


          self.LEFT_RIGHT_LAYOUT.addLayout(self.LEFT_LAYOUT)
          self.LEFT_RIGHT_LAYOUT.addLayout(self.RIGHT_LAYOUT)

     #    self.LABEL = widgets.QLabel("Днепр", self)
     #    self.LABEL.setStyleSheet("background: transparent;")

     #    self.CARDS_LAYOUT.addWidget(self.LABEL)


        

