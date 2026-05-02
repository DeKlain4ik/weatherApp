import PyQt6.QtWidgets as widgets
import PyQt6.QtCore as core
import PyQt6.QtGui as gui
from PyQt6.QtGui import QFont, QFontDatabase
import os
import json
import folium
from PyQt6.QtWebEngineWidgets import QWebEngineView
from utils import api_request_no_file
from utils import tr
import tempfile


class SearchPlace(widgets.QWidget):
    def __init__(self,main_window, parent=None):
        super().__init__(parent)

        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))


        self.main_window = main_window

        self.coord = None

        self.setAttribute(core.Qt.WidgetAttribute.WA_TranslucentBackground)

        self.setStyleSheet("background: transparent; border-radius: 16px;")

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        font_id = QFontDatabase.addApplicationFont(os.path.join(BASE_DIR, "..", "..", "media", "fonts", "Comfortaa-Regular.ttf"))
        font_family = QFontDatabase.applicationFontFamilies(font_id)

        self.font_family = QFontDatabase.applicationFontFamilies(font_id)


        self.CENTRAL_LAYOUT = widgets.QVBoxLayout(self)
        self.CENTRAL_LAYOUT.setContentsMargins(10, 30, 10, 10)
        self.CENTRAL_LAYOUT.setSpacing(20)

        self.label = widgets.QLabel()
        self.label.setFont(QFont(font_family[0], 18))
        self.label.setStyleSheet("background: transparent;")
        self.CENTRAL_LAYOUT.addWidget(self.label, alignment=core.Qt.AlignmentFlag.AlignTop | core.Qt.AlignmentFlag.AlignLeft)
        
        self.MapLayout = widgets.QHBoxLayout()

        self.CENTRAL_LAYOUT.addLayout(self.MapLayout)

        self.textLayout = widgets.QVBoxLayout()
        self.textLayout.setContentsMargins(0, 0, 0, 0)
        self.textLayout.setSpacing(15)
        self.textLayout.setAlignment(core.Qt.AlignmentFlag.AlignTop | core.Qt.AlignmentFlag.AlignLeft)

        self.MapLayout.addLayout(self.textLayout)

        self.CITIES = self.get_cities()

        
        self.COUNTRY_NAME = widgets.QLabel()
        self.COUNTRY_NAME.setFont(QFont(font_family[0], 12))
        self.COUNTRY_NAME.setStyleSheet("background: transparent;")

        self.textLayout.addWidget(self.COUNTRY_NAME)

        self.COUNTRY_BOX = widgets.QComboBox()
        self.COUNTRY_BOX.setFont(QFont(font_family[0], 12))
        self.COUNTRY_BOX.setFixedSize(200,50)
        self.COUNTRY_BOX.setStyleSheet("""
                            QComboBox {
                                        background-color: rgba(0, 0, 0, 46);
                                        border-radius: 16px;
                                        padding: 10px;
                                    }
                            QComboBox::drop-down {
                                        background:  transparent;
                                        }
                            QComboBox QAbstractItemView {
                                        background: rgba(0, 0, 0, 126);
                                        border-radius: 16px;
                                    }
                                    """)    

        self.textLayout.addWidget(self.COUNTRY_BOX)

        for country in self.CITIES:
            # print(country["country"])
            self.COUNTRY_BOX.addItem(country["country"])

        self.CITY_NAME = widgets.QLabel()
        self.CITY_NAME.setFont(QFont(font_family[0], 12))
        self.CITY_NAME.setStyleSheet("background: transparent;")
        
        self.textLayout.addWidget(self.CITY_NAME)
        
        

        self.CITY_BOX = widgets.QComboBox()
        self.CITY_BOX.setFont(QFont(font_family[0], 12))
        self.CITY_BOX.setFixedSize(200,50)
        self.CITY_BOX.setStyleSheet("""
                            QComboBox {
                                        background-color: rgba(0, 0, 0, 46);
                                        border-radius: 16px;
                                        padding: 10px;
                                    }
                            QComboBox::drop-down {
                                        background:  transparent;
                                        }
                            QComboBox QAbstractItemView {
                                        background: rgba(0, 0, 0, 46);
                                        border-radius: 16px;
                                    }
                                    """)    
        self.textLayout.addWidget(self.CITY_BOX)
        
        self.COUNTRY_BOX.currentTextChanged.connect(self.city_choice)
        
        self.CITY_BOX.currentTextChanged.connect(self.coordinates_finding)

        self.COORDIANTE_NAME = widgets.QLabel()
        self.COORDIANTE_NAME.setFont(QFont(font_family[0], 12))
        self.COORDIANTE_NAME.setStyleSheet("background: transparent;")
        
        self.textLayout.addWidget(self.COORDIANTE_NAME)

        self.coordinate_label = widgets.QLabel()
        self.coordinate_label.setFont(QFont(font_family[0], 12))
        self.coordinate_label.setFixedSize(200,50)
        
        self.coordinate_label.setStyleSheet("background-color: rgba(0, 0, 0, 46); padding: 10px; ")
        
        self.textLayout.addWidget(self.coordinate_label)


        self.button_save = widgets.QPushButton()
        self.button_save.setFont(QFont(font_family[0], 12))
        self.button_save.setFixedSize(120,50)
        self.button_save.setStyleSheet("background-color: rgba(0, 0, 0, 86); border-radius: 16px; padding: 10px;")
        self.button_save.clicked.connect(self.button_save_clicked)

        self.textLayout.addWidget(self.button_save)

        self.map_view = QWebEngineView()
        self.map_view.setFixedSize(300, 300)

        self.MapLayout.addWidget(self.map_view)

        self.show_city_on_map(50.4501, 30.5234)

        self.city_list = widgets.QListWidget()
        self.city_list.setFont(QFont(font_family[0], 16))
        self.city_list.setStyleSheet("background: transparent;")
        self.city_list.setStyleSheet("background: rgba(0, 0, 0, 86);")

        for card in self.main_window.cards_list:
            self.add_list_item(card.CITY_NAME)

        self.cities_label = widgets.QLabel()
        self.cities_label.setFont(QFont(font_family[0], 18))
        self.cities_label.setStyleSheet("background: transparent;")
        self.CENTRAL_LAYOUT.addWidget(self.cities_label, alignment=core.Qt.AlignmentFlag.AlignTop | core.Qt.AlignmentFlag.AlignLeft)

        self.CENTRAL_LAYOUT.addWidget(self.city_list)

        self.CENTRAL_LAYOUT.addStretch()
        self.retranslate_ui()

    def show_city_on_map(self, lat, lon):
        self.city_map = folium.Map(
            location=[lat, lon], 
            zoom_start=10, 
            tiles='OpenStreetMap', 
            control_scale=True
        )
        folium.Marker(location=[lat, lon]).add_to(self.city_map)
        
        html_content = self.city_map.get_root().render()
        
        self.map_view.setHtml(html_content, core.QUrl("https://cdn.jsdelivr.net/"))


    def button_save_clicked(self):
        if self.coord is not None:
            self.show_city_on_map(self.coord['lat'], self.coord['lon'])
            self.add_list_item(self.CITY_BOX.currentText())
            # print(self.main_window)
            if self.main_window:
                self.main_window.make_cards(self.CITY_BOX.currentText())

        else:
            print(tr("city_not_found"))

    def add_list_item(self, city_name):
        item = widgets.QListWidgetItem(self.city_list)

        row = widgets.QWidget()
        row.setStyleSheet("background: transparent;")
        layout = widgets.QHBoxLayout(row)
        layout.setContentsMargins(8, 4, 20, 4)

        label = widgets.QLabel(city_name)
        label.setFont(self.city_list.font())
        label.setStyleSheet("background: transparent;")

        layout.addWidget(label)
        layout.addStretch()


        is_first = self.city_list.count() == 1
        if not is_first:
            trash_icon = gui.QIcon(os.path.join(self.BASE_DIR, "..", "..", "media", "trash.svg"))


            btn = widgets.QPushButton()
            btn.setIcon(trash_icon)
            btn.setIconSize(core.QSize(20, 20))
            btn.setFixedSize(32, 32)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: rgba(255, 60, 60, 150);
                    border-radius: 8px;
                }
                QPushButton:hover {
                    background-color: rgba(255, 60, 60, 220);
                }
            """)

            def delete_item(i=item, name=city_name):
                row_index = self.city_list.row(i)   # находим номер строки
                self.city_list.takeItem(row_index)  # удаляем из списка
                
                if self.main_window:
                    self.main_window.remove_card(name)  # удаляем карточку и кэш

            btn.clicked.connect(lambda checked=False: delete_item())

            layout.addWidget(btn)

        item.setSizeHint(row.sizeHint())
        self.city_list.setItemWidget(item, row)

    def city_choice(self):
        self.CITY_BOX.clear()

        country = self.COUNTRY_BOX.currentText()
        for city in self.CITIES:
            if city["country"] == country:
                # print(city["city"])
                self.CITY_BOX.addItem(city["city"])
        
        
    def coordinates_finding(self):
        city = self.CITY_BOX.currentText()
        if not city:
            return
        self.CITY_DATA = api_request_no_file(city)
        if self.CITY_DATA.get("cod") == "404":
            self.coord = None
            self.coordinate_label.setText(tr("city_not_found"))
            return
        self.coord = self.CITY_DATA["city"]["coord"]
        self.coordinate_label.setText(f"{self.coord['lat'] }, {self.coord['lon']}")

    def get_cities(self):
        with open("static/json/cities.json", mode="r", encoding="utf-8") as file:
            data = json.load(file)
            return data["data"]

    def retranslate_ui(self):
        self.label.setText(tr("search_city"))
        self.COUNTRY_NAME.setText(tr("country"))
        self.CITY_NAME.setText(tr("city"))
        self.COORDIANTE_NAME.setText(tr("coordinates"))
        self.button_save.setText(tr("save"))
        self.cities_label.setText(tr("added_cities"))
        if self.coord is None and self.coordinate_label.text():
            self.coordinate_label.setText(tr("city_not_found"))
