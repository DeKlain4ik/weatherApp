import PyQt6.QtCore as core
import PyQt6.QtWidgets as widgets
import PyQt6.QtGui as gui

from .app import app_obj
from .title_bar import Title_bar
from utils import api_request, city_request, get_weather
from .scrollarea import ScrollArea
from .cards import Cards_widget
from .frames import WeatherFrame, TimeFrame, TimeWeatherFrame, WeatherFor12HoursFrame
from .head_bar import HeadBar

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


class MainWindow(widgets.QMainWindow):
    def __init__(self, window_width: int, window_height: int):
        widgets.QMainWindow.__init__(self)
        
        self.DARK = True

        self.WEATHER = None
        self.CITY = None
        self.POSITION = None

        self.setWindowFlags(core.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(core.Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.WINDOW_WIDTH = window_width
        self.WINDOW_HEIGHT = window_height
        
        self.SCREEN = app_obj.primaryScreen()
        self.SCREEN_SIZE = self.SCREEN.size()
        
        self.SCREEN_WIDTH = self.SCREEN_SIZE.width()
        self.SCREEN_HEIGHT = self.SCREEN_SIZE.height()
        
        self.CENTER_X = (self.SCREEN_WIDTH // 2) - (self.WINDOW_WIDTH // 2)
        self.CENTER_Y = (self.SCREEN_HEIGHT // 2) - (self.WINDOW_HEIGHT // 2)
        
        self.setGeometry(self.CENTER_X, self.CENTER_Y, self.WINDOW_WIDTH, self.WINDOW_HEIGHT)

        self.WINDOW_CONTAINER = widgets.QFrame()
        self.setCentralWidget(self.WINDOW_CONTAINER)
        self.WINDOW_CONTAINER.setObjectName("window_container")


        self.WINDOW_CONTAINER.setStyleSheet("""
        #window_container {
            background: qlineargradient(
                x1:0, y1:1, x2:1, y2:0,
                stop:0 #5DADE2,
                stop:1 #808080
            );
            border-radius:16px;
        }
        """)
        
        
        
        self.CENTRAL_WIDGET = widgets.QWidget()

        self.CENTRAL_WIDGET_LAYOUT = widgets.QVBoxLayout(self.CENTRAL_WIDGET)
        self.CENTRAL_WIDGET_LAYOUT.setContentsMargins(0,0,0,0)
        self.CENTRAL_WIDGET_LAYOUT.setSpacing(0)
        self.CENTRAL_WIDGET.setLayout(self.CENTRAL_WIDGET_LAYOUT)

        
        container_layout = widgets.QVBoxLayout(self.WINDOW_CONTAINER)
        container_layout.setContentsMargins(0,0,0,0)

        container_layout.addWidget(self.CENTRAL_WIDGET)




        
        self.TITLE_BAR = Title_bar(self.CENTRAL_WIDGET, width = self.WINDOW_WIDTH)
        self.CENTRAL_WIDGET_LAYOUT.addWidget(self.TITLE_BAR)
        
        self.CONTENT_FRAME = widgets.QFrame()
        self.CONTENT_FRAME_LAYOUT = widgets.QHBoxLayout(self.CONTENT_FRAME)

        self.CONTENT_FRAME_LAYOUT.setContentsMargins(0,0,0,0)
        self.CONTENT_FRAME_LAYOUT.setSpacing(0)

        self.CENTRAL_WIDGET_LAYOUT.addWidget(self.CONTENT_FRAME)

        self.LEFT_AREA = widgets.QFrame(parent=self.CONTENT_FRAME)
        self.LEFT_AREA.setMinimumWidth(320)
        self.LEFT_AREA.setMaximumWidth(400)

        

        self.LEFT_AREA.setSizePolicy(
            widgets.QSizePolicy.Policy.Preferred,
            widgets.QSizePolicy.Policy.Expanding
        )

        self.LEFT_AREA.setStyleSheet("background-color: rgba(0, 0, 0, 46);")

        
        
        self.RIGHT_AREA = widgets.QFrame()

        self.RIGHT_AREA.setSizePolicy(
            widgets.QSizePolicy.Policy.Expanding,
            widgets.QSizePolicy.Policy.Expanding
        )

        self.HEAD_BAR = HeadBar(parent = self.RIGHT_AREA)

        

        self.FIRST_WIDGETS_LAYOUT = widgets.QHBoxLayout()
        self.FIRST_WIDGETS_LAYOUT.setSpacing(10)
    

        self.WEATHER_FRAME = WeatherFrame(parent = self.RIGHT_AREA, weather=self.WEATHER, city = self.CITY, position=self.POSITION)

        self.FIRST_WIDGETS_LAYOUT.addWidget(self.WEATHER_FRAME)
        
        self.TIME_FRAME = TimeFrame(parent = self.RIGHT_AREA)

        self.FIRST_WIDGETS_LAYOUT.addWidget(self.TIME_FRAME)


        self.TIME_WEATHER_FRAME = TimeWeatherFrame(parent = self.RIGHT_AREA)
        
        self.WEATHER_FOR_12_HOURS_FRAME = WeatherFor12HoursFrame(parent = self.RIGHT_AREA)
        

        self.LEFT_AREA_LAYOUT = widgets.QVBoxLayout()
        self.RIGHT_AREA_LAYOUT = widgets.QVBoxLayout()
        self.RIGHT_AREA_LAYOUT.setContentsMargins(10, 30, 20, 10)
        self.RIGHT_AREA_LAYOUT.setSpacing(15)
        self.RIGHT_AREA_LAYOUT.setAlignment(core.Qt.AlignmentFlag.AlignCenter)

        self.RIGHT_AREA_LAYOUT.addWidget(self.HEAD_BAR)

        self.RIGHT_AREA_LAYOUT.addLayout(self.FIRST_WIDGETS_LAYOUT)
        
        self.RIGHT_AREA_LAYOUT.addWidget(self.TIME_WEATHER_FRAME)
        self.RIGHT_AREA_LAYOUT.addWidget(self.WEATHER_FOR_12_HOURS_FRAME)

        self.LEFT_AREA.setLayout(self.LEFT_AREA_LAYOUT)
        self.RIGHT_AREA.setLayout(self.RIGHT_AREA_LAYOUT)

        self.THEME_BUTTON = widgets.QPushButton(parent = self.LEFT_AREA)
        self.THEME_BUTTON.setStyleSheet("background: transparent; border: none")
        

        self.THEME_BUTTON.setIcon(gui.QIcon("media/SwitchDark.svg"))
            
    

        self.THEME_BUTTON.setIconSize(core.QSize(52, 24))        

        self.TOP_LAYOUT = widgets.QHBoxLayout()
        self.TOP_LAYOUT.setContentsMargins(0, 10, 10, 0)

        self.TOP_LAYOUT.addStretch() # додає відстань між кнопкою та правим краєм

        self.TOP_LAYOUT.addWidget(self.THEME_BUTTON)

        self.LEFT_AREA_LAYOUT.addLayout(self.TOP_LAYOUT)
        
        self.SCROLL_AREA = ScrollArea(parent = self.LEFT_AREA)

        
     
     
        self.LEFT_AREA_LAYOUT.addWidget(self.SCROLL_AREA)

        self.CONTENT_FRAME_LAYOUT.addWidget(self.LEFT_AREA, 0)
        self.CONTENT_FRAME_LAYOUT.addWidget(self.RIGHT_AREA, 1)
        

        self.cards_list = []
        


        self.position = Cards_widget(parent=self.SCROLL_AREA,
                                id = 0,
                                city_name = "Ettlingen",
                                is_first = True)
        
        self.position.frame_clicked.connect(self.clicked)
        self.cards_list.append(self.position)
        self.SCROLL_AREA.SCROLL_LAYOUT.addWidget(self.position)

        self.clicked(self.position)
        
                
        self.card2 = Cards_widget(parent=self.SCROLL_AREA,
                                id = 2,
                                city_name = "Ettlingen")
        
        self.card2.frame_clicked.connect(self.clicked)
        self.cards_list.append(self.card2)
        self.SCROLL_AREA.SCROLL_LAYOUT.addWidget(self.card2)

        self.card3 = Cards_widget(parent=self.SCROLL_AREA,
                                id = 3,
                                city_name = "New York")
        
        self.card3.frame_clicked.connect(self.clicked)
        self.cards_list.append(self.card3)
        self.SCROLL_AREA.SCROLL_LAYOUT.addWidget(self.card3)

        
        self.card4 = Cards_widget(parent=self.SCROLL_AREA,
                                id = 4,
                                city_name = "Tokyo")
        
        self.card4.frame_clicked.connect(self.clicked)
        self.cards_list.append(self.card4)
        self.SCROLL_AREA.SCROLL_LAYOUT.addWidget(self.card4)

        self.card5 = Cards_widget(parent=self.SCROLL_AREA,
                                id = 5,
                                city_name = "Paris")
        
        self.card5.frame_clicked.connect(self.clicked)
        self.cards_list.append(self.card5)
        self.SCROLL_AREA.SCROLL_LAYOUT.addWidget(self.card5)

        

        
        self.THEME_BUTTON.clicked.connect(self.switch_theme)

        self.SCROLL_AREA.SCROLL_LAYOUT.addStretch()   


    def clicked(self, clicked_frame):
        for i in self.cards_list:
            i.normalColor()

        clicked_frame.clcikedColor()


        if clicked_frame.ID == 0:
            self.POSITION = "Поточна позицiя"
            self.WEATHER_FRAME.CURENT_POSITON_CHECK = True
            self.WEATHER_FRAME.curent_position()
        else:
            self.WEATHER_FRAME.CURENT_POSITON_CHECK = False
            self.WEATHER_FRAME.curent_position()
            self.POSITION = None

        
        
        self.CITY = clicked_frame.CITY_NAME
        self.WEATHER = f"{clicked_frame.TEMP}°"
        self.DESCRIPTION = clicked_frame.weather_description
        self.MAX_TEMP = clicked_frame.max_temp
        self.MIN_TEMP = clicked_frame.min_temp

        self.TIME_FRAME.CITY = self.CITY

        data_dict = get_weather(self.CITY)
        self.TIME_WEATHER_FRAME.DATA = data_dict
        self.WEATHER_FOR_12_HOURS_FRAME.DATA = data_dict
        self.TIME_WEATHER_FRAME.load_weather()
        self.WEATHER_FOR_12_HOURS_FRAME.set_images()

        icon_code = data_dict["list"][0]["weather"][0]["icon"]

        
        self.WEATHER_FRAME.set_text(position = self.POSITION,
                                    city = self.CITY,
                                    weather = self.WEATHER,
                                    icon=f"media/weather_icons/{icon_code}.svg",
                                    description=self.DESCRIPTION,
                                    max_temp = self.MAX_TEMP,
                                    min_temp = self.MIN_TEMP                                
                                    )
        


        img_name = get_icon_name(data_dict["list"][0]["weather"][0]["id"], data_dict["list"][0]["weather"][0]["icon"])


        self.TIME_WEATHER_FRAME.set_current_weather(icon = img_name,
                                        temp=self.WEATHER)


        print(self.WEATHER)
        


    def switch_theme(self):
        self.DARK = not self.DARK

        if self.DARK:
            self.THEME_BUTTON.setIcon(gui.QIcon("media/SwitchDark.svg"))
            self.WINDOW_CONTAINER.setStyleSheet("""
                #window_container {
                    background: qlineargradient(
                        x1:0, y1:1, x2:1, y2:0,
                        stop:0 #5DADE2,
                        stop:1 #808080
                    );
                    border-radius:16px;
                }
                """)
        else:
            self.WINDOW_CONTAINER.setStyleSheet("""
            #window_container {
                background: qlineargradient(
                    x1:0, y1:1, x2:1, y2:0,
                    stop:0 #87CEFA,
                    stop:1 #FFDF56
                );
                border-radius:16px;
            }
            """)
            self.THEME_BUTTON.setIcon(gui.QIcon("media/SwitchLight.svg"))

main_window = MainWindow(window_width = 1200, window_height = 800)