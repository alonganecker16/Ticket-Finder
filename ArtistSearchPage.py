from PyQt5 import QtCore, QtGui, QtWidgets
import functions, SearchListWidget, requests


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(800, 600)
        self.search_button = QtWidgets.QPushButton(Form)
        self.search_button.setGeometry(QtCore.QRect(550, 70, 161, 31))
        self.search_button.setObjectName("search_button")
        self.artist_found_listWidget = QtWidgets.QListWidget(Form)
        self.artist_found_listWidget.setGeometry(QtCore.QRect(50, 140, 681, 381))
        self.artist_found_listWidget.setObjectName("artist_found_listWidget")
        self.artist_found_listWidget.setResizeMode(QtWidgets.QListView.Adjust)
        self.artist_found_listWidget.setGridSize(QtCore.QSize(250, 250))
        self.artist_found_listWidget.setWrapping(True)
        self.artist_found_listWidget.setFlow(QtWidgets.QListView.LeftToRight)
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(190, 70, 351, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.artist_name_label = QtWidgets.QLabel(Form)
        self.artist_name_label.setGeometry(QtCore.QRect(60, 70, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.artist_name_label.setFont(font)
        self.artist_name_label.setObjectName("artist_name_label")
        self.home_button = QtWidgets.QPushButton(Form)
        self.home_button.setGeometry(QtCore.QRect(620, 530, 151, 51))
        self.home_button.setObjectName("home_button")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.search_button.setText(_translate("Form", "Search"))
        self.artist_name_label.setText(_translate("Form", "Artist Name:"))
        self.home_button.setText(_translate("Form", "Back to Home Page"))

    def findArtist(self):
        self.artist_found_listWidget.clear()
        artist_name = self.lineEdit.text()
        artists = functions.get_artists(artist_name)
        for x in artists:
            self.addToList(x)

    def addToList(self, artist):
        artist_name = artist["artist"]
        url = artist["image_url"]

        print("Name: {}, Url: {}".format(artist_name, url))

        new_item_widget = QtWidgets.QWidget()
        new_item = SearchListWidget.Ui_Form()
        new_item.setupUi(new_item_widget)

        if url == None:
            new_item.artist_picture.setText("No Picture")
        else:
            image = QtGui.QImage()
            image.loadFromData(requests.get(url).content)
            new_item.artist_picture.setPixmap(QtGui.QPixmap(image))

        # Input values:
        new_item.artist_name.setText(artist_name)
        new_item.artist_id.setText(str(artist))

        widget_item = QtWidgets.QListWidgetItem()
        widget_item.setSizeHint(QtCore.QSize(250, 250))
        
        self.artist_found_listWidget.addItem(widget_item)
        self.artist_found_listWidget.setItemWidget(widget_item, new_item_widget)


