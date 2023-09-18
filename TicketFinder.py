from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import functions, User, ast



class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        import LoginPage, MainPage, ArtistSearchPage
        
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
        self.login_page.create_button.clicked.connect(self.attemptCreate)

        # Set up Main Page:
        self.main_page_widget = QtWidgets.QWidget()
        self.main_page = MainPage.Ui_Form()
        self.main_page.setupUi(self.main_page_widget)
        self.main_page.add_artist_button.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.search_page_widget))

        # Set up Search Page:
        self.search_page_widget = QtWidgets.QWidget()
        self.search_page = ArtistSearchPage.Ui_Form()
        self.search_page.setupUi(self.search_page_widget)
        self.search_page.search_button.clicked.connect(lambda: self.search_page.findArtist())
        self.search_page.artist_found_listWidget.itemDoubleClicked.connect(self.itemClicked)
        self.search_page.home_button.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.main_page_widget))


        self.stackedWidget.addWidget(self.login_page_widget) # Index: 0
        self.stackedWidget.addWidget(self.main_page_widget) # Index: 1
        self.stackedWidget.addWidget(self.search_page_widget) # Index: 2
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
            self.setupMainPage()
            print("Main Page")
        elif current_index == 2:
            print("Search Page")
        else:
            print("WTF is this index: ".format(current_index))

    def attemptLogin(self):
        login_response = functions.login(self)
        if login_response != None:
            # print(login_response)
            self.populateUser(login_response)
            # self.setupMainPage()
            self.stackedWidget.setCurrentWidget(self.main_page_widget)

    def attemptCreate(self):
        create_response = functions.create_account(self)
        if create_response != None:
            print(create_response)
            self.stackedWidget.setCurrentWidget(self.main_page_widget)

    def populateUser(self, user_info):
        self.user = User.User(user_info)
        print("Hello, {}".format(self.user.username))

    def setupMainPage(self):
        self.main_page.welcome_label.setText("Welcome, {}".format(self.user.username))
        self.main_page.refreshEventList(functions.get_events(self.user.username)["events"])

    def searchArtists(self):
        print(self.search_page.lineEdit.text())

    def itemClicked(self, item):
        widget_selected = self.search_page.artist_found_listWidget.itemWidget(item)
        artist_info = ast.literal_eval(widget_selected.findChildren(QtWidgets.QLabel, "artist_id")[0].text())
        name = widget_selected.findChildren(QtWidgets.QLabel, "artist_name")[0].text()
        
        ret = QMessageBox.question(self.centralwidget, 'Add artist?', "Would you like to add {} to your favorites list?".format(name), QMessageBox.Yes | QMessageBox.No)

        if ret == QMessageBox.Yes:
            # TODO: Add to favorites:
            functions.set_favorite_artist(self.user.username, artist_info)
        elif ret == QMessageBox.No:
            print("Cancelled")

