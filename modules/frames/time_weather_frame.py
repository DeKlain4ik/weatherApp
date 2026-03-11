import os
from datetime import datetime, timezone, timedelta

from PyQt6 import QtCore, QtWidgets, QtGui
from PyQt6.QtGui import QFont, QFontDatabase


OWM_ICONS = {
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

OWM_ICONS_NIGHT = {800: "113", 801: "116", 802: "119 122", 803: "119 123", 804: "119 123"}


def get_icon(weather_id: int, icon_code: str) -> str:
    if icon_code.endswith("n") and weather_id in OWM_ICONS_NIGHT:
        return OWM_ICONS_NIGHT[weather_id]
    return OWM_ICONS.get(weather_id, "116")


class HourCard(QtWidgets.QWidget):
    WIDTH, HEIGHT = 64, 82

    def __init__(self, time, icon_path, temp, parent=None):
        super().__init__(parent)
        self.setFixedSize(self.WIDTH, self.HEIGHT)
        self.setStyleSheet("background: transparent;")

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 2, 0, 2)
        layout.setSpacing(2)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.time_label = QtWidgets.QLabel(time)
        self.time_label.setStyleSheet("font-size: 13px; color: white; background: transparent;")
        self.time_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.time_label)

        self.icon_label = QtWidgets.QLabel()
        self.icon_label.setFixedSize(28, 28)
        self.icon_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.icon_label.setStyleSheet("background: transparent;")
        pix = QtGui.QPixmap(icon_path)
        if not pix.isNull():
            self.icon_label.setPixmap(pix.scaled(24, 24, QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                                                 QtCore.Qt.TransformationMode.SmoothTransformation))
        layout.addWidget(self.icon_label, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        self.temp_label = QtWidgets.QLabel(temp)
        self.temp_label.setStyleSheet("font-size: 14px; color: white; background: transparent;")
        self.temp_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.temp_label)

    def update(self, icon_path, temp):
        pix = QtGui.QPixmap(icon_path)
        if not pix.isNull():
            self.icon_label.setPixmap(pix.scaled(24, 24, QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                                                 QtCore.Qt.TransformationMode.SmoothTransformation))
        self.temp_label.setText(temp)


class SunCard(QtWidgets.QWidget):
    WIDTH, HEIGHT = 64, 82

    def __init__(self, time, icon_path, label, parent=None):
        super().__init__(parent)
        self.setFixedSize(self.WIDTH, self.HEIGHT)
        self.setStyleSheet("background: transparent;")

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 2, 0, 2)
        layout.setSpacing(2)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.time_label = QtWidgets.QLabel(time)
        self.time_label.setStyleSheet("font-size: 13px; color: white; background: transparent;")
        self.time_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.time_label)

        self.icon_label = QtWidgets.QLabel()
        self.icon_label.setFixedSize(28, 28)
        self.icon_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.icon_label.setStyleSheet("background: transparent;")
        pix = QtGui.QPixmap(icon_path)
        if not pix.isNull():
            self.icon_label.setPixmap(pix.scaled(24, 24, QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                                                 QtCore.Qt.TransformationMode.SmoothTransformation))
        layout.addWidget(self.icon_label, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        self.text_label = QtWidgets.QLabel(label)
        self.text_label.setStyleSheet("font-size: 11px; color: rgba(255,255,200,220); background: transparent;")
        self.text_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.text_label)


class TimeWeatherFrame(QtWidgets.QFrame):
    CARDS_PER_PAGE = 9
    CARD_WIDTH = HourCard.WIDTH
    CARD_SPACING = 6
    ANIM_DURATION = 520

    def __init__(self, parent=None):
        super().__init__(parent)
        self.DATA = {"list": [], "city": {}}
        self.cards = []
        self.page = 0
        self.animating = False

        # font
        base_dir = os.path.dirname(os.path.abspath(__file__))
        font_id = QFontDatabase.addApplicationFont(os.path.join(base_dir, "..", "..", "media", "fonts", "Comfortaa-Regular.ttf"))
        fam = QFontDatabase.applicationFontFamilies(font_id)
        self.font = QFont(fam[0], 14) if fam else QFont()

        self.setStyleSheet("background-color: rgba(0, 0, 0, 46); border-radius: 16px;")
        self.setFixedSize(790, 157)

        root = QtWidgets.QVBoxLayout(self)
        root.setContentsMargins(10, 10, 10, 5)
        root.setSpacing(3)

        self.HEADER = QtWidgets.QLabel("Погода до кінця дня")
        self.HEADER.setFixedHeight(24)
        self.HEADER.setStyleSheet("background: transparent; color: white;")
        self.HEADER.setFont(self.font)
        root.addWidget(self.HEADER, alignment=QtCore.Qt.AlignmentFlag.AlignLeft)

        sep = QtWidgets.QFrame()
        sep.setStyleSheet("background-color: rgba(255,255,255,50);")
        sep.setFixedHeight(2)
        sep.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        root.addWidget(sep)

        row = QtWidgets.QHBoxLayout()
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(4)
        root.addLayout(row)

        btn_style = "background: transparent; color: white; font-size: 20px; border: none;"

        self.LEFT_BTN = QtWidgets.QPushButton("<")
        self.LEFT_BTN.setFixedSize(16, 82)
        self.LEFT_BTN.setStyleSheet(btn_style)
        self.LEFT_BTN.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.LEFT_BTN.clicked.connect(self.prev_page)
        row.addWidget(self.LEFT_BTN, alignment=QtCore.Qt.AlignmentFlag.AlignVCenter)

        self.viewport = QtWidgets.QScrollArea()
        self.viewport.setFixedHeight(82)
        self.viewport.setStyleSheet("background: transparent; border: none;")
        self.viewport.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.viewport.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.viewport.setWidgetResizable(False)
        row.addWidget(self.viewport, 1)

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
        self.RIGHT_BTN.setStyleSheet(btn_style)
        self.RIGHT_BTN.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.RIGHT_BTN.clicked.connect(self.next_page)
        row.addWidget(self.RIGHT_BTN, alignment=QtCore.Qt.AlignmentFlag.AlignVCenter)

        self.anim = QtCore.QPropertyAnimation(self.viewport.horizontalScrollBar(), b"value")
        self.anim.setDuration(self.ANIM_DURATION)
        self.anim.setEasingCurve(QtCore.QEasingCurve.Type.OutCubic)
        self.anim.finished.connect(self.anim_done)

        self.update_arrows()

    def page_width(self):
        vw = self.viewport.viewport().width()
        return vw if vw > 0 else self.CARDS_PER_PAGE * (self.CARD_WIDTH + self.CARD_SPACING) - self.CARD_SPACING

    def max_page(self):
        return 0 if not self.cards else (len(self.cards) - 1) // self.CARDS_PER_PAGE

    def update_arrows(self):
        self.LEFT_BTN.setEnabled(self.page > 0)
        self.LEFT_BTN.setStyleSheet(f"background: transparent; border: none; font-size: 20px; color: {'white' if self.page > 0 else 'rgba(255,255,255,60)'}")
        self.RIGHT_BTN.setEnabled(self.page < self.max_page())
        self.RIGHT_BTN.setStyleSheet(f"background: transparent; border: none; font-size: 20px; color: {'white' if self.page < self.max_page() else 'rgba(255,255,255,60)'}")

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
        bar = self.viewport.horizontalScrollBar()
        target = page * self.page_width()
        if bar.value() == target:
            return
        self.animating = True
        self.anim.stop()
        self.anim.setStartValue(bar.value())
        self.anim.setEndValue(target)
        self.anim.start()
        self.update_arrows()

    def anim_done(self):
        self.animating = False

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.viewport.horizontalScrollBar().setValue(self.page * self.page_width())

    def load_weather(self):
        self.page = 0
        for c in self.cards:
            c.setParent(None)
            c.deleteLater()
        self.cards.clear()

        while self.strip_layout.count():
            item = self.strip_layout.takeAt(0)
            if item.widget():
                item.widget().setParent(None)

        entries = self.DATA.get("list", [])
        city_info = self.DATA.get("city", {})
        tz = city_info.get("timezone", 0)
        sunrise = city_info.get("sunrise")
        sunset = city_info.get("sunset")

        def ts_to_dt(ts):
            if ts is None:
                return None
            return datetime.fromtimestamp(ts, tz=timezone.utc) + timedelta(seconds=tz)

        sunrise_dt, sunset_dt = ts_to_dt(sunrise), ts_to_dt(sunset)
        sunrise_inserted = sunset_inserted = False
        MAX_CARDS = self.CARDS_PER_PAGE * 2

        for i, e in enumerate(entries):
            if len(self.cards) >= MAX_CARDS:
                break

            dt_txt = e.get("dt_txt", "")
            try:
                dt = datetime.strptime(dt_txt, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc) + timedelta(seconds=tz)
            except Exception:
                dt = datetime.fromtimestamp(e["dt"], tz=timezone.utc) + timedelta(seconds=tz)

            prev_dt = None
            if i > 0:
                try:
                    prev_dt = datetime.strptime(entries[i-1]["dt_txt"], "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc) + timedelta(seconds=tz)
                except Exception:
                    pass

            if not sunrise_inserted and sunrise_dt and prev_dt and prev_dt <= sunrise_dt < dt and len(self.cards) < MAX_CARDS:
                card = SunCard(sunrise_dt.strftime("%H:%M"), "media/icons_12hours/sunrise.svg", "Схід")
                self.strip_layout.addWidget(card)
                self.cards.append(card)
                sunrise_inserted = True

            if not sunset_inserted and sunset_dt and prev_dt and prev_dt <= sunset_dt < dt and len(self.cards) < MAX_CARDS:
                card = SunCard(sunset_dt.strftime("%H:%M"), "media/icons_12hours/sunset.svg", "Захід")
                self.strip_layout.addWidget(card)
                self.cards.append(card)
                sunset_inserted = True

            if len(self.cards) >= MAX_CARDS:
                break

            temp = int(round(e["main"]["temp"]))
            w = e["weather"][0] if isinstance(e["weather"], list) else e["weather"]
            icon = get_icon(w.get("id", 800), w.get("icon", "01d"))
            icon_path = f"media/icons_12hours/{icon}.svg"
            time_str = "Зараз" if i == 0 else dt.strftime("%H:%M")

            card = HourCard(time_str, icon_path, f"{temp}°")
            self.strip_layout.addWidget(card)
            self.cards.append(card)

        n = len(self.cards)
        self.strip.setFixedWidth(n * self.CARD_WIDTH + max(0, n-1) * self.CARD_SPACING)
        self.viewport.horizontalScrollBar().setValue(0)
        self.update_arrows()

    def set_current_weather(self, icon, temp):
        if self.cards and isinstance(self.cards[0], HourCard):
            self.cards[0].update(f"media/icons_12hours/{icon}.svg", temp)