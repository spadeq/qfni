import os
import random
import sys
import PySide6
import matplotlib
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import QSize
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QMainWindow, QApplication, QWidget
from qt_material import apply_stylesheet, QtStyleTools
from multiprocessing import freeze_support

dirname = os.path.dirname(PySide6.__file__)
plugin_path = os.path.join(dirname, "plugins", "platforms")
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path

app = QApplication([])
freeze_support()
app.processEvents()
app.setQuitOnLastWindowClosed(False)
app.lastWindowClosed.connect(app.quit)


class MainWidget(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        main_widget = QtWidgets.QWidget()
        main_layout = QtWidgets.QHBoxLayout()
        main_widget.setLayout(main_layout)

        self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир", "你好"]

        self.button = QtWidgets.QPushButton("Click me!")
        self.button.setProperty("class", "danger")
        self.text = QtWidgets.QLabel("Hello World", alignment=QtCore.Qt.AlignCenter)
        self.nav = QtWidgets.QListWidget()
        nav_list = ["Dicom", "Labeling", "Train", "Verify"]
        for item in nav_list:
            self.nav_item = QtWidgets.QListWidgetItem(item, self.nav)
            self.nav_item.setSizeHint(QSize(30, 60))
            self.nav_item.setTextAlignment(Qt.AlignCenter)

        self.tabWidget = QtWidgets.QTabWidget()

        main_layout.addWidget(self.nav)
        main_layout.addWidget(self.text)
        main_layout.addWidget(self.button)

        self.setCentralWidget(main_widget)

        self.button.clicked.connect(self.magic)

    @QtCore.Slot()
    def magic(self):
        self.text.setText(random.choice(self.hello))


class RuntimeStylesheets(QMainWindow, QtStyleTools):
    def __init__(self):
        super().__init__()

        self.main = QUiLoader().load("mainform.ui", self)

        logo = QIcon("qt_material:/logo/logo.svg")
        logo_frame = QIcon("qt_material:/logo/logo_frame.svg")

        self.main.setWindowIcon(logo)


if __name__ == "__main__":
    extra = {
        "danger": "#dc3545",
        "warning": "#ffc107",
        "success": "#17a2b8"
    }

    apply_stylesheet(app, theme="dark_pink.xml", extra=extra)
    frame = RuntimeStylesheets()

    frame.main.show()
    app.exec()
