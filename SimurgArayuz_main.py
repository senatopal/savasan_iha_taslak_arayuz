from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDateTime 
from PyQt5.QtGui import QPixmap
import time
import sys
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout
from SimurgArayuz import Ui_Form
from radar import MatplotlibWidget


class SimurgArayuz(QMainWindow):
        def __init__(self):
                super(SimurgArayuz, self).__init__()
                self.new2arayuz = Ui_Form()
                self.new2arayuz.setupUi(self)
                self.setMinimumSize(1024, 768)
                
                self.matplotlib_widget=MatplotlibWidget(self)
                layout = QVBoxLayout()
                layout.addWidget(self.matplotlib_widget)
                self.new2arayuz.widget_radar.setLayout(layout)



def app():
        if __name__ == "__main__":
                app = QtWidgets.QApplication(sys.argv)
                win = SimurgArayuz()
                win.show()
                sys.exit(app.exec_())
app()

    