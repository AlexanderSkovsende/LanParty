# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'turnering.ui'
#
# Created by: PyQt4 UI code generator 4.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(512, 339)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.txtName = QtGui.QLineEdit(Dialog)
        self.txtName.setObjectName(_fromUtf8("txtName"))
        self.gridLayout.addWidget(self.txtName, 0, 1, 1, 1)
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 3, 0, 1, 1)
        self.txtType = QtGui.QLineEdit(Dialog)
        self.txtType.setObjectName(_fromUtf8("txtType"))
        self.gridLayout.addWidget(self.txtType, 1, 1, 1, 1)
        self.btnSave = QtGui.QPushButton(Dialog)
        self.btnSave.setObjectName(_fromUtf8("btnSave"))
        self.gridLayout.addWidget(self.btnSave, 4, 2, 1, 1)
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.dateTurnering = QtGui.QDateTimeEdit(Dialog)
        self.dateTurnering.setObjectName(_fromUtf8("dateTurnering"))
        self.gridLayout.addWidget(self.dateTurnering, 2, 1, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Turnering", None))
        self.label.setText(_translate("Dialog", "Navn på turnering", None))
        self.label_2.setText(_translate("Dialog", "Turneringstype", None))
        self.btnSave.setText(_translate("Dialog", "Gem og luk", None))
        self.label_3.setText(_translate("Dialog", "Start-tidspunkt", None))

