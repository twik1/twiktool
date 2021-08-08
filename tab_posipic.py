#import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QLineEdit, QGroupBox, QGridLayout, QPushButton
from PyQt5.QtWidgets import QVBoxLayout, QTabWidget, QLabel, QFileDialog
import threading
import posipic
import tt

class PosiPic(QWidget):
    def __init__(self):
        super().__init__()
        gpbx1 = QGroupBox('Config')
        lone = QLabel("Select directory to search for pics")
        ltwo = QLabel("Select output file for KML")
        self.ldir = QLineEdit(self)
        self.lfile = QLineEdit(self)
        #self.sfile = QLineEdit(self)
        dirbutton = QPushButton('...', self)
        dirbutton.clicked.connect(self.select_dir)
        filebutton = QPushButton('...', self)
        filebutton.clicked.connect(self.select_file)
        layout = QGridLayout()
        layout.setColumnStretch(1, 4)
        layout.setColumnStretch(2, 4)
        layout.addWidget(lone, 0, 0)
        layout.addWidget(self.ldir, 1, 0)
        layout.addWidget(dirbutton, 1, 1)
        layout.addWidget(ltwo, 2, 0)
        layout.addWidget(self.lfile, 3, 0)
        layout.addWidget(filebutton, 3, 1)
        gpbx1.setLayout(layout)

        gpbx2 = QGroupBox('Status')
        self.label1 = QLabel("Number of files scanned :")
        self.label2 = QLabel("Number of images :")
        self.label3 = QLabel("Number of images with exifdata :")
        self.label5 = QLabel("Number of images with exifdata with gps :")
        self.label4 = QLabel("Status: Idle")
        self.label4.setStyleSheet("QLabel { color : blue; }")
        layout = QGridLayout()
        layout.setColumnStretch(1, 4)
        layout.setColumnStretch(2, 4)
        layout.addWidget(self.label1, 0, 0)
        layout.addWidget(self.label2, 1, 0)
        layout.addWidget(self.label3, 2, 0)
        layout.addWidget(self.label5, 3, 0)
        layout.addWidget(self.label4, 4, 0)
        gpbx2.setLayout(layout)

        gpbx3 = QGroupBox('Control')
        self.runbutton = QPushButton('Run', self)
        self.runbutton.clicked.connect(self.run_posipic)
        self.stopbutton = QPushButton('Stop', self)
        self.stopbutton.clicked.connect(self.stop_posipic)
        self.stopbutton.setEnabled(False)
        layout = QGridLayout()
        layout.setColumnStretch(1, 4)
        layout.setColumnStretch(2, 4)
        layout.addWidget(self.runbutton, 0, 0)
        layout.addWidget(self.stopbutton, 0, 1)
        gpbx3.setLayout(layout)

        first_layout = QVBoxLayout()
        first_layout.addWidget(gpbx1)
        first_layout.addWidget(gpbx2)
        first_layout.addWidget(gpbx3)
        self.setLayout(first_layout)

    def select_dir(self):
        tdir = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.ldir.setText(tdir)
        return tdir

    def select_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        tfile = QFileDialog.getSaveFileName(self, "Select File", options=options)
        self.lfile.setText(str(tfile[0]))
        return tfile

    def run_wrapper(self):
        self.label4.setText('Status: Running...')
        self.label4.setStyleSheet("QLabel { color : blue; }");
        self.runbutton.setEnabled(False)
        self.stopbutton.setEnabled(True)
        QApplication.processEvents()
        retvalue = posipic.run_posipic(self.ldir.text(), self.lfile.text())
        if retvalue['result'] == 0:
            self.label4.setText('Status: Finished OK')
            self.label4.setStyleSheet("QLabel { color : green; }")
        elif retvalue['result'] == 1:
            self.label4.setText('Status: Directory to search for doesn\'t exist')
            self.label4.setStyleSheet("QLabel { color : red; }")
        else:
            self.label4.setText('Status: Unable to save KML file')
            self.label4.setStyleSheet("QLabel { color : red; }")
        self.label1.setText("Number of files scanned : {}".format(retvalue['numfiles']))
        self.label2.setText("Number of images : {}".format(retvalue['numimg']))
        self.label3.setText("Number of images with exifdata : {}".format(retvalue['numexif']))
        self.label5.setText("Number of images with exifdata with gps : {}".format(retvalue['numgps']))
        self.runbutton.setEnabled(True)
        self.stopbutton.setEnabled(False)
        QApplication.processEvents()

    def run_posipic(self):
        # Check to see that all field are filled in
        if not self.ldir.text() or not self.lfile.text():
            self.label4.setText('Status: Fill in all fields')
            self.label4.setStyleSheet("QLabel { color : red; }")
            return
        work = tt.TThread(self.run_wrapper(), "")
        work.start_thread()

    def stop_posipic(self):
        None

