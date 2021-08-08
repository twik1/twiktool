#import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QLineEdit, QGroupBox, QGridLayout, QPushButton
from PyQt5.QtWidgets import QVBoxLayout, QTabWidget, QLabel, QFileDialog
import threading
import chrome
import tt

class Chrome(QWidget):
    def __init__(self):
        super().__init__()

        gpbx1 = QGroupBox('Config')
        lone = QLabel("SID as a string")
        ltwo = QLabel("Password")
        lthree = QLabel("Select directory with master keyfiles")
        lfour = QLabel("Select chrome db file")
        lfive = QLabel("Select result file")
        self.sid = QLineEdit(self)
        self.ldir = QLineEdit(self)
        self.lfile = QLineEdit(self)
        self.password = QLineEdit(self)
        self.sfile = QLineEdit(self)
        dirbutton = QPushButton('...', self)
        dirbutton.clicked.connect(self.select_dir)
        filebutton = QPushButton('...', self)
        filebutton.clicked.connect(self.select_file)
        sfilebutton = QPushButton('...', self)
        sfilebutton.clicked.connect(self.select_save_file)
        layout = QGridLayout()
        layout.setColumnStretch(1, 4)
        layout.setColumnStretch(2, 4)
        layout.addWidget(lone, 0, 0)
        layout.addWidget(self.sid, 1, 0)
        layout.addWidget(ltwo, 2, 0)
        layout.addWidget(self.password, 3, 0)
        layout.addWidget(lthree, 4, 0)
        layout.addWidget(self.ldir, 5, 0)
        layout.addWidget(dirbutton, 5, 1)
        layout.addWidget(lfour, 6, 0)
        layout.addWidget(self.lfile, 7, 0)
        layout.addWidget(filebutton, 7, 1)
        layout.addWidget(lfive, 8, 0)
        layout.addWidget(self.sfile, 9, 0)
        layout.addWidget(sfilebutton, 9, 1)
        gpbx1.setLayout(layout)

        gpbx2 = QGroupBox('Status')
        self.label1 = QLabel("Status : Idle")
        self.label1.setStyleSheet("QLabel { color : blue; }")
        layout = QGridLayout()
        layout.setColumnStretch(1, 4)
        layout.setColumnStretch(2, 4)
        layout.addWidget(self.label1, 0, 0)
        gpbx2.setLayout(layout)

        gpbx3 = QGroupBox('Control')
        self.runbutton = QPushButton('Run', self)
        self.runbutton.clicked.connect(self.run_unchrome)
        self.stopbutton = QPushButton('Stop', self)
        self.stopbutton.clicked.connect(self.stop_unchrome)
        self.stopbutton.setEnabled(False)
        layout = QGridLayout()
        layout.setColumnStretch(1, 4)
        layout.setColumnStretch(2, 4)
        layout = QGridLayout()
        layout.setColumnStretch(1, 4)
        layout.setColumnStretch(2, 4)
        layout.addWidget(self.runbutton, 0, 0)
        layout.addWidget(self.stopbutton, 0, 1)
        gpbx3.setLayout(layout)

        second_layout = QVBoxLayout()
        second_layout.addWidget(gpbx1)
        second_layout.addWidget(gpbx2)
        second_layout.addWidget(gpbx3)
        self.setLayout(second_layout)

    def select_dir(self):
        tdir = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.ldir.setText(tdir)
        return tdir

    def select_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        tfile = QFileDialog.getOpenFileName(self, "Select File", options=options)
        self.lfile.setText(str(tfile[0]))
        return tfile

    def select_save_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        tfile = QFileDialog.getSaveFileName(self, "Select File", options=options)
        self.sfile.setText(str(tfile[0]))
        return tfile

    def run_wrapper(self):
        self.label1.setText('Status: Running...')
        self.label1.setStyleSheet("QLabel { color : blue; }")
        self.runbutton.setEnabled(False)
        self.stopbutton.setEnabled(True)
        QApplication.processEvents()
        retvalue = chrome.run_unchrome(self.sid.text(), self.password.text(), self.ldir.text(),
                                       self.lfile.text(), self.sfile.text())
        if retvalue['result'] == 0:
            self.label1.setText('Status: Finished OK')
            self.label1.setStyleSheet("QLabel { color : green; }")
        elif retvalue['result'] == 1:
            self.label1.setText('Status: No masterkeys decoded')
            self.label1.setStyleSheet("QLabel { color : red; }")
        elif retvalue['result'] == 2:
            self.label1.setText('Status: Unable to save output file')
            self.label1.setStyleSheet("QLabel { color : red; }")
        else:
            self.label1.setText('Status: Unknown fault')
            self.label1.setStyleSheet("QLabel { color : red; }")
        self.runbutton.setEnabled(True)
        self.stopbutton.setEnabled(False)
        QApplication.processEvents()


    def run_unchrome(self):
        # Check to see that all field are filled in
        if not self.sid.text() or not self.lfile.text() or not self.ldir.text() \
                or not self.password.text() or not self.sfile.text():
            self.label1.setText('Status: Fill in all fields')
            self.label1.setStyleSheet("QLabel { color : red; }")
            return
        work = tt.TThread(self.run_wrapper(), "")
        work.start_thread()

    def stop_unchrome(self):
        None
