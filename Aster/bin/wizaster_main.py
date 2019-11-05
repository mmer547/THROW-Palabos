## -*- coding: utf-8 -*-
import sys
import subprocess as sp
from PySide import QtCore, QtGui

from wizaster_ui import *
from wizaster_lib import *


class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self,parent=None):
        super(MainWindow, self).__init__(parent) 
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Menu
        self.ui.actionEdit_config_ini.triggered.connect(self.open_config)

        self.ui.actionExit.triggered.connect(sys.exit)

        # Model difinition

        # Mesh selection
        self.ui.ms_refer.clicked.connect(lambda:ms_ref(self.ui))
        
        # Material properties
        self.ui.mp_edit1.setText('2e+11')
        self.ui.mp_edit2.setText('0.3')
        
        # Boundaries conditions
        self.bc1_model = QtGui.QStandardItemModel()
        self.ui.bc1_table.setModel(self.bc1_model)
        self.initial_bc1(self.bc1_model)
        self.ui.bc1_button.clicked.connect(lambda:self.add_bc1(self.bc1_model))
        self.ui.bc1_button_2.clicked.connect(lambda:self.del_bc(self.bc1_model))

        
        # Boundaries conditions
        self.bc2_model = QtGui.QStandardItemModel()
        self.ui.bc2_table.setModel(self.bc2_model)
        self.initial_bc2(self.bc2_model)
        self.ui.bc2_button.clicked.connect(lambda:self.add_bc2(self.bc2_model))
        self.ui.bc2_button_2.clicked.connect(lambda:self.del_bc(self.bc2_model))
        
        # Filename for writting command file
        self.ui.fw_refer.clicked.connect(lambda:fw_ref(self.ui))

        # Run Button
        self.ui.run_button.clicked.connect(lambda:self.run_func(self.ui))
        
        # Paraview Button
        self.ui.pv_button.clicked.connect(lambda:run_paraview(self.ui))

        # Close Button
        self.ui.close_button.clicked.connect(sys.exit)

    def open_config(self):
        def _get(inifile, section, name):
            try:
                return inifile.get(section, name)
            except Exception, e:
                return "error: could not read " + name
        inifile = ConfigParser.SafeConfigParser()
        inifile.read("config.ini")
        command = _get(inifile, 'other', 'editer')
        cmd = ' '.join([command, 'config.ini'])
        sp.call(cmd)


    def initial_bc1(self, model_name):
        buf = []        
        buf.append(QtGui.QStandardItem(''))
        buf.append(QtGui.QStandardItem('0.0'))
        buf.append(QtGui.QStandardItem('0.0'))
        buf.append(QtGui.QStandardItem('0.0'))
        buf = [buf]
        for i in range(len(buf)):
            for j in range(len(buf[i])):
                model_name.setItem(i, j, buf[i][j])


    def initial_bc2(self, model_name):
        buf = []
        buf.append(QtGui.QStandardItem(''))
        buf.append(QtGui.QStandardItem('0.0'))
        buf = [buf]
        for i in range(len(buf)):
            for j in range(len(buf[i])):
                model_name.setItem(i, j, buf[i][j])


    def add_bc1(self, model_name):
        buf = []        
        buf.append(QtGui.QStandardItem(''))
        buf.append(QtGui.QStandardItem('0.0'))
        buf.append(QtGui.QStandardItem('0.0'))
        buf.append(QtGui.QStandardItem('0.0'))
        i = model_name.rowCount()
        for j in range(len(buf)):
            model_name.setItem(i, j, buf[j])


    def add_bc2(self, model_name):
        buf = []
        buf.append(QtGui.QStandardItem(''))
        buf.append(QtGui.QStandardItem('0.0'))
        i = model_name.rowCount()
        for j in range(len(buf)):
            model_name.setItem(i, j, buf[j])


    def del_bc(self, model_name):
        i = model_name.rowCount()
        model_name.removeRows(i-1, 1)


    def del_bc2(self, model_name):
        buf = []
        buf.append(QtGui.QStandardItem(''))
        buf.append(QtGui.QStandardItem('0.0'))
        i = model_name.rowCount()
        for j in range(len(buf)):
            model_name.setItem(i, j, buf[j])


    def get_item(self, model_name):
        data=[]
        for row in range(model_name.rowCount()):
            data.append([])
            for column in range(model_name.columnCount()):
                index = model_name.index(row, column)
                data[row].append(str(model_name.data(index)))
        return data


    def run_func(self, ui):
        ui.bc1_data = self.get_item(self.bc1_model)
        ui.bc2_data = self.get_item(self.bc2_model)  
        run_button(ui)
        
#------------------------------------------------------------------------------ 
## GUIの起動
def main():
    app = QtGui.QApplication(sys.argv)
    app.setStyle('plastique')    # ← ここでスタイルを指定
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
