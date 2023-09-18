from PyQt5 import QtCore, QtGui, QtWidgets
from functions import *
import functions, ArtistListWidget, TicketFinder

global ui

if __name__ == "__main__":
    import sys
    init_db()
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = TicketFinder.Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())