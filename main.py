from PyQt5 import QtWidgets
from functions import *
import TicketFinder

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