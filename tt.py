import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QLineEdit, QGroupBox, QGridLayout, QPushButton
from PyQt5.QtWidgets import QVBoxLayout, QTabWidget, QLabel, QFileDialog
import threading
import tab_posipic
import tab_chrome
import tab_strsearch

class TThread:
    def __init__(self, func, param):
        if func:
            self.state = 'armed'
            self.tthread = threading.Thread(target=func, args=(param,))
        else:
            self.state = 'disarmed'
            self.tthread = None

    def set_func(self, func, param):
        self.tthread = threading.Thread(target=func, args=(param,))
        self.state = 'armed'

    def start_thread(self):
        if self.state == 'armed':
            self.tthread.start()

    def stop_thread(self):
        self.tthread.stop()

class TabDialog(QDialog):
    def __init__(self):
        super().__init__()


        self.setWindowTitle("twik ToolKit")
        self.setWindowIcon(QIcon("icon.png"))

        tabwidget = QTabWidget()
        tabwidget.addTab(tab_posipic.PosiPic(), "PosiPic")
        tabwidget.addTab(tab_chrome.Chrome(), "UnChrome")
        tabwidget.addTab(tab_strsearch.StrSearch(), "StrSearch")
        vboxLayout = QVBoxLayout()
        vboxLayout.addWidget(tabwidget)
        self.setLayout(vboxLayout)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    tabdialog = TabDialog()
    tabdialog.show()
    app.exec()