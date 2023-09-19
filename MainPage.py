from PyQt5 import QtCore, QtGui, QtWidgets
from datetime import datetime
import ArtistListWidget, requests



class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(800, 600)
        self.add_artist_button = QtWidgets.QPushButton(Form)
        self.add_artist_button.setGeometry(QtCore.QRect(550, 50, 161, 51))
        self.add_artist_button.setObjectName("add_artist_button")
        self.profile_button = QtWidgets.QPushButton(Form)
        self.profile_button.setGeometry(QtCore.QRect(350, 50, 161, 51))
        self.profile_button.setObjectName("profile_button")
        self.welcome_label = QtWidgets.QLabel(Form)
        self.welcome_label.setGeometry(QtCore.QRect(50, 20, 211, 51))
        self.welcome_label.setObjectName("welcome_label")
        self.artist_listWidget = QtWidgets.QListWidget(Form)
        self.artist_listWidget.setGeometry(QtCore.QRect(50, 140, 850, 450))
        self.artist_listWidget.setObjectName("artist_listWidget")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.add_artist_button.setText(_translate("Form", "Add an Artist"))
        self.profile_button.setText(_translate("Form", "Update Profile"))
        self.welcome_label.setText(_translate("Form", "Hello, [USERNAME]"))
        __sortingEnabled = self.artist_listWidget.isSortingEnabled()
        self.artist_listWidget.setSortingEnabled(False)
        self.artist_listWidget.setSortingEnabled(__sortingEnabled)
    
    def refreshEventList(self, events):
        self.artist_listWidget.clear()
        
        for event in events:
            self.addItem(event)

    def addItem(self, event):
        # Set up widget:
        new_item_widget = QtWidgets.QWidget()
        new_item = ArtistListWidget.Ui_Form()
        new_item.setupUi(new_item_widget)

        # Set variables from event JSON:
        artist_name = event["artist_name"]
        event_name = event["title"]
        location = event["venue"]["name_v2"]
        time = datetime.strptime(event["datetime_local"], "%Y-%m-%dT%H:%M:%S").strftime("%m/%d/%Y\n%H:%M %p")
        best_price = event["stats"]["lowest_price_good_deals"]
        lowest_price = event["stats"]["lowest_price"]

        # If prices are None value:
        if lowest_price == None: lowest_price = "N/a"
        else: lowest_price = "${}".format(lowest_price)
        if best_price == None: best_price = "N/a"
        else: best_price = "${}".format(best_price)

        # Set text of the labels in the widget:
        new_item.artist_label.setText(artist_name)
        new_item.location_label.setText(location)
        new_item.date_label.setText(time)
        new_item.event_label.setText(event_name)
        new_item.best_price_label.setText("Best Value Price: {}".format(best_price))
        new_item.lowest_price_label.setText("Lowest Price: {}".format(lowest_price))

        # Set up the image in widget:
        url = event["image_url"]
        image = QtGui.QImage()
        image.loadFromData(requests.get(url).content)
        new_item.artist_picture.setPixmap(QtGui.QPixmap(image))

        new_item.url = event["url"]

        widget_item = QtWidgets.QListWidgetItem()
        widget_item.setSizeHint(QtCore.QSize(589, 128))
        
        self.artist_listWidget.addItem(widget_item)
        self.artist_listWidget.setItemWidget(widget_item, new_item_widget)
