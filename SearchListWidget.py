from PyQt5 import QtCore, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(250, 250)
        self.artist_picture = QtWidgets.QLabel(Form)
        self.artist_picture.setGeometry(QtCore.QRect(40, 10, 176, 149))
        self.artist_picture.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.artist_picture.setAlignment(QtCore.Qt.AlignCenter)
        self.artist_picture.setObjectName("artist_picture")
        self.artist_id = QtWidgets.QLabel(Form)
        self.artist_id.setGeometry(QtCore.QRect(0, 0, 0, 0))
        self.artist_id.setAlignment(QtCore.Qt.AlignCenter)
        self.artist_id.setObjectName("artist_id")
        self.artist_id.setHidden(True)
        self.artist_name = QtWidgets.QLabel(Form)
        self.artist_name.setGeometry(QtCore.QRect(30, 210, 181, 20))
        self.artist_name.setAlignment(QtCore.Qt.AlignCenter)
        self.artist_name.setObjectName("artist_name")
        
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.artist_picture.setText(_translate("Form", "TextLabel"))
        self.artist_name.setText(_translate("Form", "TextLabel"))
