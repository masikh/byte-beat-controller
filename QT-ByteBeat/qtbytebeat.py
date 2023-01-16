# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qtbytebeat.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1280, 719)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        Form.setFont(font)
        Form.setCursor(QtGui.QCursor(QtCore.Qt.BlankCursor))
        Form.setAcceptDrops(False)
        Form.setAutoFillBackground(False)
        self.frequency_plot = QtWidgets.QGraphicsView(Form)
        self.frequency_plot.setGeometry(QtCore.QRect(180, 80, 920, 181))
        self.frequency_plot.setMouseTracking(True)
        self.frequency_plot.setTabletTracking(True)
        self.frequency_plot.setObjectName("frequency_plot")
        self.title = QtWidgets.QLabel(Form)
        self.title.setGeometry(QtCore.QRect(180, 10, 920, 61))
        font = QtGui.QFont()
        font.setFamily("Marker Felt")
        font.setPointSize(48)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.title.setFont(font)
        self.title.setMouseTracking(True)
        self.title.setTabletTracking(True)
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setObjectName("title")
        self.formula_selector = QtWidgets.QListView(Form)
        self.formula_selector.setGeometry(QtCore.QRect(180, 400, 921, 221))
        self.formula_selector.setMouseTracking(True)
        self.formula_selector.setTabletTracking(True)
        self.formula_selector.setObjectName("formula_selector")
        self.formula_editor = QtWidgets.QLineEdit(Form)
        self.formula_editor.setGeometry(QtCore.QRect(180, 640, 920, 61))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.formula_editor.setFont(font)
        self.formula_editor.setTabletTracking(True)
        self.formula_editor.setObjectName("formula_editor")
        self.potmeter_1 = QtWidgets.QDial(Form)
        self.potmeter_1.setGeometry(QtCore.QRect(181, 284, 100, 100))
        self.potmeter_1.setCursor(QtGui.QCursor(QtCore.Qt.BlankCursor))
        self.potmeter_1.setMouseTracking(True)
        self.potmeter_1.setTabletTracking(True)
        self.potmeter_1.setMaximum(4095)
        self.potmeter_1.setWrapping(False)
        self.potmeter_1.setNotchesVisible(True)
        self.potmeter_1.setObjectName("potmeter_1")
        self.potmeter_2 = QtWidgets.QDial(Form)
        self.potmeter_2.setGeometry(QtCore.QRect(427, 284, 100, 100))
        self.potmeter_2.setCursor(QtGui.QCursor(QtCore.Qt.BlankCursor))
        self.potmeter_2.setMouseTracking(True)
        self.potmeter_2.setTabletTracking(True)
        self.potmeter_2.setMaximum(4095)
        self.potmeter_2.setWrapping(False)
        self.potmeter_2.setNotchesVisible(True)
        self.potmeter_2.setObjectName("potmeter_2")
        self.potmeter_3 = QtWidgets.QDial(Form)
        self.potmeter_3.setGeometry(QtCore.QRect(674, 284, 100, 100))
        self.potmeter_3.setCursor(QtGui.QCursor(QtCore.Qt.BlankCursor))
        self.potmeter_3.setMouseTracking(True)
        self.potmeter_3.setTabletTracking(True)
        self.potmeter_3.setMaximum(4095)
        self.potmeter_3.setWrapping(False)
        self.potmeter_3.setNotchesVisible(True)
        self.potmeter_3.setObjectName("potmeter_3")
        self.potmeter_4 = QtWidgets.QDial(Form)
        self.potmeter_4.setGeometry(QtCore.QRect(920, 284, 100, 100))
        self.potmeter_4.setCursor(QtGui.QCursor(QtCore.Qt.BlankCursor))
        self.potmeter_4.setMouseTracking(True)
        self.potmeter_4.setTabletTracking(True)
        self.potmeter_4.setMaximum(4095)
        self.potmeter_4.setWrapping(False)
        self.potmeter_4.setNotchesVisible(True)
        self.potmeter_4.setObjectName("potmeter_4")
        self.button_left = QtWidgets.QPushButton(Form)
        self.button_left.setGeometry(QtCore.QRect(30, 110, 110, 110))
        self.button_left.setMouseTracking(True)
        self.button_left.setTabletTracking(True)
        self.button_left.setText("")
        self.button_left.setObjectName("button_left")
        self.button_right = QtWidgets.QPushButton(Form)
        self.button_right.setGeometry(QtCore.QRect(1140, 110, 110, 110))
        self.button_right.setMouseTracking(True)
        self.button_right.setTabletTracking(True)
        self.button_right.setText("")
        self.button_right.setObjectName("button_right")
        self.button_1 = QtWidgets.QPushButton(Form)
        self.button_1.setGeometry(QtCore.QRect(290, 300, 70, 70))
        self.button_1.setMouseTracking(True)
        self.button_1.setTabletTracking(True)
        self.button_1.setText("")
        self.button_1.setObjectName("button_1")
        self.button_2 = QtWidgets.QPushButton(Form)
        self.button_2.setGeometry(QtCore.QRect(537, 300, 70, 70))
        self.button_2.setMouseTracking(True)
        self.button_2.setTabletTracking(True)
        self.button_2.setText("")
        self.button_2.setObjectName("button_2")
        self.button_3 = QtWidgets.QPushButton(Form)
        self.button_3.setGeometry(QtCore.QRect(784, 300, 70, 70))
        self.button_3.setMouseTracking(True)
        self.button_3.setTabletTracking(True)
        self.button_3.setText("")
        self.button_3.setObjectName("button_3")
        self.button_4 = QtWidgets.QPushButton(Form)
        self.button_4.setGeometry(QtCore.QRect(1030, 300, 70, 70))
        self.button_4.setMouseTracking(True)
        self.button_4.setTabletTracking(True)
        self.button_4.setText("")
        self.button_4.setObjectName("button_4")
        self.background = QtWidgets.QGraphicsView(Form)
        self.background.setGeometry(QtCore.QRect(0, 0, 1280, 720))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.background.sizePolicy().hasHeightForWidth())
        self.background.setSizePolicy(sizePolicy)
        self.background.setMouseTracking(True)
        self.background.setTabletTracking(True)
        self.background.setObjectName("background")
        self.play_status = QtWidgets.QLabel(Form)
        self.play_status.setGeometry(QtCore.QRect(1140, 135, 110, 60))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(36)
        font.setBold(True)
        font.setWeight(75)
        self.play_status.setFont(font)
        self.play_status.setAlignment(QtCore.Qt.AlignCenter)
        self.play_status.setObjectName("play_status")
        self.background.raise_()
        self.frequency_plot.raise_()
        self.title.raise_()
        self.formula_selector.raise_()
        self.formula_editor.raise_()
        self.potmeter_1.raise_()
        self.potmeter_2.raise_()
        self.potmeter_3.raise_()
        self.potmeter_4.raise_()
        self.button_left.raise_()
        self.button_right.raise_()
        self.button_1.raise_()
        self.button_2.raise_()
        self.button_3.raise_()
        self.button_4.raise_()
        self.play_status.raise_()

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "bytebeat"))
        self.title.setText(_translate("Form", "Bytebeat"))
        self.formula_editor.setText(_translate("Form", "Formula editor"))
        self.play_status.setText(_translate("Form", "||"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
