#import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QLineEdit, QGroupBox, QGridLayout, QPushButton
from PyQt5.QtWidgets import QVBoxLayout, QTabWidget, QLabel, QFileDialog, QComboBox, QSpinBox
import threading
import posipic
import tt

class StrSearch(QWidget):
    def __init__(self):
        super().__init__()

        gpbx1 = QGroupBox('Config')
        # Labels
        lone = QLabel("Select directory/file to search for strings")
        ltwo = QLabel("Select result file")
        lthree = QLabel("Min and max string lenght to search for")
        l4  = QLabel("Encoding to search for")
        # editfields
        self.ldir = QLineEdit(self)
        self.sfile = QLineEdit(self)
        # qspinbox
        spbox1 = QSpinBox()
        spbox1.setRange(3, 30);
        spbox1.setSingleStep(1);
        spbox1.setValue(3);
        spbox2 = QSpinBox()
        #self.max = QLineEdit(self)
        #self.max.setFixedWidth(80)
        #self.min = QLineEdit(self)
        #self.min.setFixedWidth(80)
        # combobox
        self.comboBox = QComboBox()
        self.comboBox.addItem("UTF-8")
        self.comboBox.addItem("UTF-16")
        self.comboBox.addItem("Latin-1")
        #self.lfile = QLineEdit(self)
        # Buttons
        dirbutton = QPushButton('...', self)
        dirbutton.clicked.connect(self.select_dir)
        sfilebutton = QPushButton('...', self)
        sfilebutton.clicked.connect(self.select_save_file)
        #filebutton = QPushButton('...', self)
        #filebutton.clicked.connect(self.select_file)

        layout1 = QGridLayout()
        #layout.setColumnStretch(1, 4)
        #layout.setColumnStretch(2, 4)
        layout1.addWidget(lone, 0, 0)
        layout1.addWidget(self.ldir, 1, 0, 1, 1)
        layout1.addWidget(dirbutton, 1, 1, 1, 1)
        layout1.addWidget(l4, 2, 0)
        layout1.addWidget(self.comboBox, 3, 0)
        layout1.addWidget(lthree, 4, 0)
        #layout.setColumnStretch(5, 1)
        layout1.addWidget(spbox1, 5, 0, 1, 1)
        layout1.addWidget(spbox2, 5, 1, 1, 1)
        #layout.addWidget(filebutton, 5, 1)
        layout1.addWidget(ltwo, 6, 0)
        layout1.addWidget(self.sfile, 7, 0)
        layout1.addWidget(sfilebutton, 7, 1)
        gpbx1.setLayout(layout1)

        gpbx2 = QGroupBox('Status')
        self.label1 = QLabel("Status: Idle")
        self.label1.setStyleSheet("QLabel { color : blue; }")
        layout = QGridLayout()
        layout.setColumnStretch(1, 4)
        layout.setColumnStretch(2, 4)
        layout.addWidget(self.label1, 0, 0)
        gpbx2.setLayout(layout)

        gpbx3 = QGroupBox('Control')
        self.runbutton = QPushButton('Run', self)
        self.runbutton.clicked.connect(self.run_strsearch)
        self.stopbutton = QPushButton('Stop', self)
        self.stopbutton.clicked.connect(self.stop_strsearch)
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
        self.label1.setText('Status: Running...')
        self.label1.setStyleSheet("QLabel { color : blue; }");
        self.runbutton.setEnabled(False)
        self.stopbutton.setEnabled(True)
        QApplication.processEvents()
        retvalue = posipic.run_posipic(self.ldir.text(), self.sfile.text())
        if retvalue['result'] == 0:
            self.label1.setText('Status: Finished OK')
            self.label1.setStyleSheet("QLabel { color : green; }")
        elif retvalue['result'] == 1:
            self.label1.setText('Status: Directory to search for doesn\'t exist')
            self.label1.setStyleSheet("QLabel { color : red; }")
        else:
            self.label1.setText('Status: Unknown fault')
            self.label1.setStyleSheet("QLabel { color : red; }")
        self.runbutton.setEnabled(True)
        self.stopbutton.setEnabled(False)
        QApplication.processEvents()

    def run_strsearch(self):
        # Check to see that all field are filled in
        if not self.ldir.text() or not self.sfile.text():
            self.label1.setText('Status: Fill in all fields')
            self.label1.setStyleSheet("QLabel { color : red; }")
            return
        work = tt.TThread(self.run_wrapper(), "")
        work.start_thread()

    def select_save_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        tfile = QFileDialog.getSaveFileName(self, "Select File", options=options)
        self.sfile.setText(str(tfile[0]))
        return tfile

    def stop_strsearch(self):
        None

