import sys
import sqlite3
from PyQt5 import QtWidgets, uic
# from main import open_main
import my


class log_window(QtWidgets.QMainWindow):
    def __init__(self):
        super(log_window, self).__init__()
        uic.loadUi('login.ui', self)
        self.logBtn.clicked.connect(self.open_rating)
        # self.quitBtn.clicked.connect(self.bac_log)

    # def bac_log(self):
    #     self.hide()
    #     self.SignupWindow = SignupWindow()
    #     self.SignupWindow.show()

    def open_rating(self):
        # Get the entered username and password from the text fields
        username = self.username.text()
        password = self.password.text()

        # Connect to the SQLite database
        connection = sqlite3.connect('try.db')
        cursor = connection.cursor()

        # Execute a SELECT query to check if the username and password are correct
        cursor.execute("SELECT * FROM users WHERE Username = ? AND PassWord = ?", (username, password))
        result = cursor.fetchone()

        if result:
            # Open the next page
            self.open_main = open_main()
            self.open_main.show()
            self.hide()
        else:
            # Display an error message
            QtWidgets.QMessageBox.warning(self, "Authentication Failed", "Incorrect username or password")

        # Close the database connection
        connection.close()


class open_main(QtWidgets.QMainWindow):
    def __init__(self):
        super(open_main, self).__init__()
        uic.loadUi('water.ui', self)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = log_window()
    window.show()
    sys.exit(app.exec_())