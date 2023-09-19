from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import functions, User, ast



class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        import LoginPage, MainPage, ArtistSearchPage, CreatePage, UserProfilePage
        
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 720)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.main_frame = QtWidgets.QFrame(self.centralwidget)
        self.main_frame.setGeometry(QtCore.QRect(9, 9, 1260, 700))
        self.main_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.main_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.main_frame.setObjectName("main_frame")
        self.stackedWidget = QtWidgets.QStackedWidget(self.main_frame)
        self.stackedWidget.setGeometry(QtCore.QRect(0, 0, 1260, 700))
        self.stackedWidget.setObjectName("stackedWidget")
        
        self.stackedWidget.currentChanged.connect(self.checkCurrentWidget)

        MainWindow.setCentralWidget(self.centralwidget)

        # Set up Login Page:
        self.login_page_widget = QtWidgets.QWidget()
        self.login_page = LoginPage.Ui_Form()
        self.login_page.setupUi(self.login_page_widget)
        self.login_page.login_button.clicked.connect(self.attemptLogin)
        self.login_page.create_button.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.create_page_widget))

        # Set up Main Page:
        self.main_page_widget = QtWidgets.QWidget()
        self.main_page = MainPage.Ui_Form()
        self.main_page.setupUi(self.main_page_widget)
        self.main_page.add_artist_button.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.search_page_widget))
        self.main_page.profile_button.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.profile_page_widget))

        # Set up Search Page:
        self.search_page_widget = QtWidgets.QWidget()
        self.search_page = ArtistSearchPage.Ui_Form()
        self.search_page.setupUi(self.search_page_widget)
        self.search_page.search_button.clicked.connect(lambda: self.search_page.findArtist())
        self.search_page.artist_found_listWidget.itemDoubleClicked.connect(self.addItemClicked)
        self.search_page.home_button.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.main_page_widget))

        # Set up Create Page:
        self.create_page_widget = QtWidgets.QWidget()
        self.create_page = CreatePage.Ui_Form()
        self.create_page.setupUi(self.create_page_widget)
        self.create_page.back_button.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.login_page_widget))
        self.create_page.create_button.clicked.connect(self.attemptCreate)

        # Set up Profile Page:
        self.profile_page_widget = QtWidgets.QWidget()
        self.profile_page = UserProfilePage.Ui_Form()
        self.profile_page.setupUi(self.profile_page_widget)
        self.profile_page.artist_listWidget.itemDoubleClicked.connect(self.removeItemClicked)
        self.profile_page.back_button.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.main_page_widget))
        self.profile_page.update_button.clicked.connect(self.updateUser)


        self.stackedWidget.addWidget(self.login_page_widget) # Index: 0
        self.stackedWidget.addWidget(self.create_page_widget) # Index: 1
        self.stackedWidget.addWidget(self.main_page_widget) # Index: 2
        self.stackedWidget.addWidget(self.search_page_widget) # Index: 3
        self.stackedWidget.addWidget(self.profile_page_widget) # Index: 4
        self.stackedWidget.setCurrentWidget(self.login_page_widget)

        # self.user = User.User()
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

    def checkCurrentWidget(self):
        current_index = self.stackedWidget.currentIndex()

        if current_index == 0:
            print("Login Page")
        elif current_index == 1:
            print("Create Page")
        elif current_index == 2:
            print("Main Page")
            self.setupMainPage()
        elif current_index == 3:
            print("Search Page")
            self.setupSearchPage()
        elif current_index == 4:
            print("Profile Page")
            self.setupProfilePage()
        else:
            print("WTF is this index: {}".format(current_index))

    def attemptLogin(self):
        login_response = functions.login(self)
        if login_response != None:
            self.populateUser(login_response)
            self.stackedWidget.setCurrentWidget(self.main_page_widget)

    def attemptCreate(self):
        created_user = {"username": self.create_page.username_lineEdit.text(),
                        "favorites": [],
                        "pref": {
                            "state": self.create_page.state_comboBox.currentText()
                        }}
        create_response = functions.create_account(created_user)
        if create_response != None:
            self.create_page.error_label.setText("<html><head/><body><p><span style=\" font-size:14pt; color:#02f00e;\">User {} has been created!</span></p></body></html>".format(created_user["username"]))
            self.create_page.error_label.setVisible(True)
        else:
            self.create_page.error_label.setText("<html><head/><body><p><span style=\" font-size:14pt; color:#de0000;\">User {} already exists.</span></p></body></html>".format(created_user["username"]))
            self.create_page.error_label.setVisible(True)

    def populateUser(self, user_info):
        self.user = User.User(user_info)
        print("Hello, {}".format(self.user.username))

    def setupMainPage(self):
        self.main_page.welcome_label.setText("Welcome, {}".format(self.user.username))
        self.main_page.refreshEventList(functions.get_events(self.user.username)["events"])
    
    def setupSearchPage(self):
        self.search_page.artist_found_listWidget.clear()
        self.search_page.lineEdit.setText("")

    def setupProfilePage(self):
        self.profile_page.artist_listWidget.clear()
        self.profile_page.username_value_label.setText(self.user.username)
        index = self.profile_page.state_comboBox.findText(self.user.pref["state"])
        self.profile_page.state_comboBox.setCurrentIndex(index)

        for artist in self.user.favorites:
            print(artist)
            self.profile_page.addToList(artist)

        self.stackedWidget.setCurrentWidget(self.profile_page_widget)

    def searchArtists(self):
        print(self.search_page.lineEdit.text())
    
    def updateUser(self):
        state = self.profile_page.state_comboBox.currentText()
        self.user.pref["state"] = state
        functions.update_user_settings(state)
        self.stackedWidget.setCurrentWidget(self.main_page_widget)

    def removeItemClicked(self, item):
        widget_selected = self.profile_page.artist_listWidget.itemWidget(item)
        artist_info = ast.literal_eval(widget_selected.findChildren(QtWidgets.QLabel, "artist_id")[0].text())
        name = widget_selected.findChildren(QtWidgets.QLabel, "artist_name")[0].text()
        
        ret = QMessageBox.question(self.centralwidget, 'Add artist?', "Would you like to remove {} from your favorites list?".format(name), QMessageBox.Yes | QMessageBox.No)

        if ret == QMessageBox.Yes:
            resp = functions.remove_favorite_artist(self.user.username, artist_info)

            if resp:
                update = functions.refreshUser(self.user.username)
                self.user.favorites = update["favorites"]
                self.profile_page.artist_listWidget.takeItem(self.profile_page.artist_listWidget.indexFromItem(item).row())
            else:
                print("Artist not deleted.")

        elif ret == QMessageBox.No:
            print("Cancelled")

    def addItemClicked(self, item):
        widget_selected = self.search_page.artist_found_listWidget.itemWidget(item)
        artist_info = ast.literal_eval(widget_selected.findChildren(QtWidgets.QLabel, "artist_id")[0].text())
        name = widget_selected.findChildren(QtWidgets.QLabel, "artist_name")[0].text()
        
        ret = QMessageBox.question(self.centralwidget, 'Add artist?', "Would you like to add {} to your favorites list?".format(name), QMessageBox.Yes | QMessageBox.No)

        if ret == QMessageBox.Yes:
            functions.set_favorite_artist(self.user.username, artist_info)
            update = functions.refreshUser(self.user.username)
            self.user.favorites = update["favorites"]
        elif ret == QMessageBox.No:
            print("Cancelled")

