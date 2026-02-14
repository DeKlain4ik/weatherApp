import PyQt6.QtCore as core
import PyQt6.QtWidgets as widgets

import sys

widgets.QApplication.setAttribute(core.Qt.ApplicationAttribute.AA_ShareOpenGLContexts)

app_obj = widgets.QApplication(sys.argv)


