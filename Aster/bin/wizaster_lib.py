# coding:utf-8
import os
import subprocess as sp
import ConfigParser

from PySide import QtCore, QtGui

from write_export import *
from write_comm import *


def get_model_type(ui):
    return ui.md_combo.currentText()


def ms_ref(ui):
    mesh_name = QtGui.QFileDialog.getOpenFileName()
    ui.ms_edit.setText(mesh_name[0])


def fw_ref(ui):
    comm_name = QtGui.QFileDialog.getSaveFileName()
    ui.fw_edit.setText(comm_name[0])


def output_export(ui, path):
    param = {
            'comm_name':ui.fw_edit.text().replace('/', '\\'),
            'mesh_name':ui.ms_edit.text().replace('/', '\\')
            }
    write_export(param=param,output_name=path)


def output_comm(ui):
    param = {
            'comm_name':ui.fw_edit.text(),
            'E':ui.mp_edit1.text(),
            'nu':ui.mp_edit2.text(),
            'bc1':ui.bc1_data,
            'bc2':ui.bc2_data
            }
    comm = ui.fw_edit.text()
    write_comm(param=param)


def run_aster(folder_path, command):
    pwd = os.getcwd()
    os.chdir(folder_path)
    run_com = [command, 'export']
    cmd = ' '.join(run_com)
    try:
        sp.check_call(cmd)
    except:
        QtGui.QMessageBox.information(
            None,
            "Error!",
            "Calculation is not ended!",
            QtGui.QMessageBox.Close
            )
    else:
        QtGui.QMessageBox.information(
            None,
            "Successful!",
            "Calculation ended usually!",
            QtGui.QMessageBox.Close
            )
    os.chdir(pwd)


def run_button(ui):
    comm = ui.fw_edit.text().replace('/', '\\')
    folder_path = comm[:comm.rfind('\\')]
    def _get(inifile, section, name):
        try:
            return inifile.get(section, name)
        except Exception, e:
            return "error: could not read " + name
    inifile = ConfigParser.SafeConfigParser()
    inifile.read("config.ini")
    command = _get(inifile, 'solver', 'command') 
    output_export(ui, os.path.join(folder_path, 'export'))
    output_comm(ui)
    run_aster(folder_path, command)


def run_paraview(ui):
    comm = ui.fw_edit.text().replace('/', '\\')
    folder_path = comm[:comm.rfind('\\')]
    def _get(inifile, section, name):
        try:
            return inifile.get(section, name)
        except Exception, e:
            return "error: could not read " + name
    inifile = ConfigParser.SafeConfigParser()
    inifile.read("config.ini")
    command = _get(inifile, 'paraview', 'command')
    pwd = os.getcwd()
    os.chdir(folder_path)
    try:
        sp.check_call(command)
    except:
        pass
    os.chdir(pwd)
