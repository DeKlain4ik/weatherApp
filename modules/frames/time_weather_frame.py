import os
from datetime import datetime, timezone, timedelta

from PyQt6 import QtCore, QtWidgets, QtGui
from PyQt6.QtGui import QFont, QFontDatabase
from utils import load_icon_pixmap, tr, weather_icon_path


WEATHER_ID_TO_ICON = {
    200: "200 386", 201: "200 386", 202: "200 386",
    210: "200 386", 211: "200 386", 212: "200 386",
    221: "200 386", 230: "200 386", 231: "200 386", 232: "200 386",
    300: "263 266", 301: "263 266", 302: "263 267",
    310: "263 266", 311: "263 266", 312: "263 267",
    313: "296 302", 314: "296 303", 321: "263 266",
    500: "296 302", 501: "305 356", 502: "305 357", 503: "305 357", 504: "305 357",
    511: "311 314",
    520: "296 302", 521: "296 303", 522: "305 357", 531: "296 303",
    600: "326 332", 601: "326 333", 602: "338",
    611: "317 320", 612: "317 321", 613: "317 320",
    615: "323 329 368", 616: "323 329 369",
    620: "326 332", 621: "326 333", 622: "338",
    701: "248", 711: "248", 721: "248",
    731: "248", 741: "248", 751: "248",
    761: "248", 762: "248", 771: "248", 781: "248",
    800: "113", 801: "116", 802: "119 122", 803: "119 123", 804: "119 123",
}

WEATHER_ID_TO_ICON_NIGHT = {
    800: "113", 801: "116", 802: "119 122", 803: "119 123", 804: "119 123"
}


def get_icon(weather_id: int, icon_code: str) -> str:
    is_night_icon = icon_code.endswith("n")

    if is_night_icon and weather_id in WEATHER_ID_TO_ICON_NIGHT:
        return WEATHER_ID_TO_ICON_NIGHT[weather_id]

    return WEATHER_ID_TO_ICON.get(weather_id, "116")


class HourCard(QtWidgets.QWidget):
    WIDTH = 64
    HEIGHT = 82

    def __init__(self, time_text, icon_path, temperature_text, parent=None):
        super().__init__(parent)
        self.setFixedSize(self.WIDTH, self.HEIGHT)
        self.setStyleSheet("background: transparent;")

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 2, 0, 2)
        layout.setSpacing(2)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.time_label = QtWidgets.QLabel(time_text)
        self.time_label.setStyleSheet("font-size: 13px; color: white; background: transparent;")
        self.time_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.time_label)

        self.icon_label = QtWidgets.QLabel()
        self.icon_label.setFixedSize(28, 28)
        self.icon_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.icon_label.setStyleSheet("background: transparent;")

        icon_pixmap = load_icon_pixmap(icon_path, 20, 20)
        if not icon_pixmap.isNull():
            self.icon_label.setPixmap(
                icon_pixmap
            )
        layout.addWidget(self.icon_label, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        self.temperature_label = QtWidgets.QLabel(temperature_text)
        self.temperature_label.setStyleSheet("font-size: 14px; color: white; background: transparent;")
        self.temperature_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.temperature_label)

    def update(self, icon_path, temperature_text):
        icon_pixmap = load_icon_pixmap(icon_path, 20, 20)
        if not icon_pixmap.isNull():
            self.icon_label.setPixmap(
                icon_pixmap
            )
        self.temperature_label.setText(temperature_text)


class SunCard(QtWidgets.QWidget):
    WIDTH = 64
    HEIGHT = 82

    def __init__(self, time_text, icon_path, label_text, parent=None):
        super().__init__(parent)
        self.setFixedSize(self.WIDTH, self.HEIGHT)
        self.setStyleSheet("background: transparent;")

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 2, 0, 2)
        layout.setSpacing(2)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.time_label = QtWidgets.QLabel(time_text)
        self.time_label.setStyleSheet("font-size: 13px; color: white; background: transparent;")
        self.time_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.time_label)

        self.icon_label = QtWidgets.QLabel()
        self.icon_label.setFixedSize(28, 28)
        self.icon_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.icon_label.setStyleSheet("background: transparent;")

        icon_pixmap = load_icon_pixmap(icon_path, 20, 20)
        if not icon_pixmap.isNull():
            self.icon_label.setPixmap(
                icon_pixmap
            )
        layout.addWidget(self.icon_label, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        self.text_label = QtWidgets.QLabel(label_text)
        self.text_label.setStyleSheet("font-size: 11px; color: rgba(255,255,200,220); background: transparent;")
        self.text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.text_label)


class TimeWeatherFrame(QtWidgets.QFrame):
    CARDS_PER_PAGE = 9
    CARD_WIDTH = HourCard.WIDTH
    CARD_SPACING = 6
    ANIMATION_DURATION = 1020

    def __init__(self, parent=None):
        super().__init__(parent)
        self.DATA = {"list": [], "city": {}}
        self.cards = []
        self.page = 0
        self.animating = False

        base_directory = os.path.dirname(os.path.abspath(__file__))
        font_id = QFontDatabase.addApplicationFont(
            os.path.join(base_directory, "..", "..", "media", "fonts", "Comfortaa-Regular.ttf")
        )
        font_families = QFontDatabase.applicationFontFamilies(font_id)
        self.font = QFont(font_families[0], 14) if font_families else QFont()

        self.setStyleSheet("background-color: rgba(0, 0, 0, 46); border-radius: 16px;")
        self.setFixedSize(790, 157)

        root_layout = QtWidgets.QVBoxLayout(self)
        root_layout.setContentsMargins(10, 10, 10, 5)
        root_layout.setSpacing(3)

        self.HEADER = QtWidgets.QLabel()
        self.HEADER.setFixedHeight(24)
        self.HEADER.setStyleSheet("background: transparent; color: white;")
        self.HEADER.setFont(self.font)
        root_layout.addWidget(self.HEADER, alignment=QtCore.Qt.AlignmentFlag.AlignLeft)

        separator = QtWidgets.QFrame()
        separator.setStyleSheet("background-color: rgba(255,255,255,50);")
        separator.setFixedHeight(2)
        separator.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        root_layout.addWidget(separator)

        row_layout = QtWidgets.QHBoxLayout()
        row_layout.setContentsMargins(0, 0, 0, 0)
        row_layout.setSpacing(4)
        root_layout.addLayout(row_layout)

        button_style = "background: transparent; color: white; font-size: 20px; border: none;"

        self.LEFT_BTN = QtWidgets.QPushButton("<")
        self.LEFT_BTN.setFixedSize(16, 82)
        self.LEFT_BTN.setStyleSheet(button_style)
        self.LEFT_BTN.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.LEFT_BTN.clicked.connect(self.prev_page)
        row_layout.addWidget(self.LEFT_BTN, alignment=QtCore.Qt.AlignmentFlag.AlignVCenter)

        self.viewport = QtWidgets.QScrollArea()
        self.viewport.setFixedHeight(82)
        self.viewport.setStyleSheet("background: transparent; border: none;")
        self.viewport.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.viewport.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.viewport.setWidgetResizable(False)
        row_layout.addWidget(self.viewport, 1)

        self.strip = QtWidgets.QWidget()
        self.strip.setFixedHeight(82)
        self.strip.setStyleSheet("background: transparent;")
        self.viewport.setWidget(self.strip)

        self.strip_layout = QtWidgets.QHBoxLayout(self.strip)
        self.strip_layout.setContentsMargins(0, 0, 0, 0)
        self.strip_layout.setSpacing(self.CARD_SPACING)
        self.strip_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)

        self.RIGHT_BTN = QtWidgets.QPushButton(">")
        self.RIGHT_BTN.setFixedSize(16, 82)
        self.RIGHT_BTN.setStyleSheet(button_style)
        self.RIGHT_BTN.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.RIGHT_BTN.clicked.connect(self.next_page)
        row_layout.addWidget(self.RIGHT_BTN, alignment=QtCore.Qt.AlignmentFlag.AlignVCenter)

        self.animation = QtCore.QPropertyAnimation(self.viewport.horizontalScrollBar(), b"value")
        self.animation.setDuration(self.ANIMATION_DURATION)
        self.animation.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.animation.finished.connect(self.anim_done)

        self.update_arrows()
        self.retranslate_ui()

    def page_width(self):
        viewport_width = self.viewport.viewport().width()
        return viewport_width if viewport_width > 0 else self.CARDS_PER_PAGE * (self.CARD_WIDTH + self.CARD_SPACING) - self.CARD_SPACING

    def max_page(self):
        return 0 if not self.cards else (len(self.cards) - 1) // self.CARDS_PER_PAGE

    def update_arrows(self):
        left_is_active = self.page > 0
        self.LEFT_BTN.setEnabled(left_is_active)
        self.LEFT_BTN.setStyleSheet(
            f"background: transparent; border: none; font-size: 20px; "
            f"color: {'white' if left_is_active else 'rgba(255,255,255,60)'}"
        )

        right_is_active = self.page < self.max_page()
        self.RIGHT_BTN.setEnabled(right_is_active)
        self.RIGHT_BTN.setStyleSheet(
            f"background: transparent; border: none; font-size: 20px; "
            f"color: {'white' if right_is_active else 'rgba(255,255,255,60)'}"
        )

    def prev_page(self):
        if self.animating or self.page <= 0:
            return
        self.page -= 1
        self.slide_to(self.page)

    def next_page(self):
        if self.animating or self.page >= self.max_page():
            return
        self.page += 1
        self.slide_to(self.page)

    def slide_to(self, page):
        scroll_bar = self.viewport.horizontalScrollBar()
        target_position = page * self.page_width()

        if scroll_bar.value() == target_position:
            return

        self.animating = True
        self.animation.stop()
        self.animation.setStartValue(scroll_bar.value())
        self.animation.setEndValue(target_position)
        self.animation.start()
        self.update_arrows()

    def anim_done(self):
        self.animating = False

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.viewport.horizontalScrollBar().setValue(self.page * self.page_width())

    def load_weather(self):
        self.page = 0

        for card in self.cards:
            card.setParent(None)
            card.deleteLater()
        self.cards.clear()

        while self.strip_layout.count():
            layout_item = self.strip_layout.takeAt(0)
            if layout_item.widget():
                layout_item.widget().setParent(None)

        weather_entries = self.DATA.get("list", [])
        city_info = self.DATA.get("city", {})
        timezone_offset = city_info.get("timezone", 0)
        sunrise_timestamp = city_info.get("sunrise")
        sunset_timestamp = city_info.get("sunset")

        def timestamp_to_local_datetime(timestamp):
            if timestamp is None:
                return None
            return datetime.fromtimestamp(timestamp, tz=timezone.utc) + timedelta(seconds=timezone_offset)

        sunrise_datetime = timestamp_to_local_datetime(sunrise_timestamp)
        sunset_datetime = timestamp_to_local_datetime(sunset_timestamp)
        sunrise_inserted = False
        sunset_inserted = False
        max_cards = self.CARDS_PER_PAGE * 2

        for index, entry in enumerate(weather_entries):
            if len(self.cards) >= max_cards:
                break
                
            date_text = entry.get("dt_txt", "")
            try:
                entry_datetime = datetime.strptime(date_text, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc) + timedelta(seconds=timezone_offset)
            except Exception:
                entry_datetime = datetime.fromtimestamp(entry["dt"], tz=timezone.utc) + timedelta(seconds=timezone_offset)

            previous_datetime = None
            if index > 0:
                try:
                    previous_datetime = datetime.strptime(
                        weather_entries[index - 1]["dt_txt"], "%Y-%m-%d %H:%M:%S"
                    ).replace(tzinfo=timezone.utc) + timedelta(seconds=timezone_offset)
                except Exception:
                    pass

            should_insert_sunrise = (
                not sunrise_inserted
                and sunrise_datetime is not None
                and previous_datetime is not None
                and previous_datetime <= sunrise_datetime < entry_datetime
                and len(self.cards) < max_cards
            )
            if should_insert_sunrise:
                sunrise_card = SunCard(
                    sunrise_datetime.strftime("%H:%M"),
                    "media/icons_12hours/sunrise.svg",
                    tr("sunrise")
                )
                self.strip_layout.addWidget(sunrise_card)
                self.cards.append(sunrise_card)
                sunrise_inserted = True

            should_insert_sunset = (
                not sunset_inserted
                and sunset_datetime is not None
                and previous_datetime is not None
                and previous_datetime <= sunset_datetime < entry_datetime
                and len(self.cards) < max_cards
            )
            if should_insert_sunset:
                sunset_card = SunCard(
                    sunset_datetime.strftime("%H:%M"),
                    "media/icons_12hours/sunset.svg",
                    tr("sunset")
                )
                self.strip_layout.addWidget(sunset_card)
                self.cards.append(sunset_card)
                sunset_inserted = True

            if len(self.cards) >= max_cards:
                break

            temperature = int(round(entry["main"]["temp"]))
            weather_data = entry["weather"][0] if isinstance(entry["weather"], list) else entry["weather"]
            icon_name = get_icon(weather_data.get("id", 800), weather_data.get("icon", "01d"))
            icon_path = weather_icon_path(f"media/icons_12hours/{icon_name}.svg", weather_data.get("id", 800))
            time_display = tr("now") if index == 0 else entry_datetime.strftime("%H:%M")

            hour_card = HourCard(time_display, icon_path, f"{temperature}°")
            self.strip_layout.addWidget(hour_card)
            self.cards.append(hour_card)

        total_cards = len(self.cards)
        self.strip.setFixedWidth(
            total_cards * self.CARD_WIDTH + max(0, total_cards - 1) * self.CARD_SPACING
        )
        self.viewport.horizontalScrollBar().setValue(0)
        self.update_arrows()

    def set_current_weather(self, icon, temp, weather_id=None):
        if self.cards and isinstance(self.cards[0], HourCard):
            self.cards[0].update(weather_icon_path(f"media/icons_12hours/{icon}.svg", weather_id), temp)

    def retranslate_ui(self):
        self.HEADER.setText(tr("weather_until_end_day"))
