import base64
import re

from PyQt6 import QtCore, QtGui


def load_icon_pixmap(path, width, height):
    if path.lower().endswith(".svg"):
        try:
            with open(path, "r", encoding="utf-8") as file:
                svg_text = file.read()
        except OSError:
            return QtGui.QPixmap()

        match = re.search(r'data:image/[^;]+;base64,([^"]+)', svg_text)
        if match:
            image_data = base64.b64decode(match.group(1))
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(image_data)
            return pixmap.scaled(
                width,
                height,
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )

    pixmap = QtGui.QPixmap(path)
    if pixmap.isNull():
        return pixmap
    return pixmap.scaled(
        width,
        height,
        QtCore.Qt.AspectRatioMode.KeepAspectRatio,
        QtCore.Qt.TransformationMode.SmoothTransformation,
    )
