from PyQt5 import QtCore, QtGui, QtWidgets
import functions, TicketFinder


class Ui_Form(TicketFinder.Ui_MainWindow):
    def __init__(self):
        super(Ui_Form, self).__init__()

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(799, 600)
        self.login_button = QtWidgets.QPushButton(Form)
        self.login_button.setGeometry(QtCore.QRect(330, 410, 121, 41))
        self.login_button.setObjectName("login_button")
        self.create_button = QtWidgets.QPushButton(Form)
        self.create_button.setGeometry(QtCore.QRect(330, 460, 121, 41))
        self.create_button.setObjectName("create_button")
        self.prompt_label = QtWidgets.QLabel(Form)
        self.prompt_label.setGeometry(QtCore.QRect(210, 160, 351, 171))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.prompt_label.setFont(font)
        self.prompt_label.setAlignment(QtCore.Qt.AlignCenter)
        self.prompt_label.setObjectName("prompt_label")
        self.error_label = QtWidgets.QLabel(Form)
        self.error_label.setEnabled(False)
        self.error_label.setGeometry(QtCore.QRect(130, 300, 531, 41))
        self.error_label.setAlignment(QtCore.Qt.AlignCenter)
        self.error_label.setObjectName("error_label")
        self.error_label.setVisible(False)
        self.username_line = QtWidgets.QLineEdit(Form)
        self.username_line.setGeometry(QtCore.QRect(290, 350, 201, 31))
        self.username_line.setText("")
        self.username_line.setFrame(True)
        self.username_line.setObjectName("username_line")
        self.title_label = QtWidgets.QLabel(Form)
        self.title_label.setGeometry(QtCore.QRect(180, 70, 421, 111))
        font = QtGui.QFont()
        font.setPointSize(19)
        self.title_label.setFont(font)
        self.title_label.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.title_label.setObjectName("title_label")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.login_button.setText(_translate("Form", "Login"))
        self.create_button.setText(_translate("Form", "Create Account"))
        self.prompt_label.setText(_translate("Form", "Enter your username below\n"
"Click \"Login\" if you have an account\n"
"Click \"Create Account\" if you are a new user"))
        self.error_label.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:14pt; color:#de0000;\">[error_message]</span></p></body></html>"))
        self.username_line.setPlaceholderText(_translate("Form", "Username"))
        self.title_label.setText(_translate("Form", "Welcome to Ticket Finder!"))

    def loginClicked(self):
        if functions.login(self):
            super().switchToMainPage()
        

