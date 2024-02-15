# import cv2
import  sys
from PyQt5.QtWidgets import QApplication, QTextEdit
from PyQt5.QtWidgets import QApplication,QMainWindow
import smtplib
from email.mime.text import MIMEText
import traceback
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl
from PyQt5 import QtWidgets, uic
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon,QPixmap,QImage
from PyQt5.QtWidgets import QMessageBox,QTableWidgetItem,QFileDialog,QLabel
import icon
import my
import sqlite3
import openpyxl
from PyQt5.QtWidgets import QTextEdit, QPushButton
from PyQt5.QtCore import pyqtSlot
from PyQt5.uic import loadUi

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# app = QApplication(sys.argv)
# import sys
# from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QMessageBox, QTableWidgetItem, QFileDialog, QLabel
# from PyQt5 import QtWidgets, uic
# from PyQt5.QtGui import QDesktopServices
# from PyQt5.QtGui import QIcon, QPixmap, QImage
# from PyQt5.QtCore import QUrl, pyqtSlot
# from PyQt5.uic import loadUi
# import smtplib
# from email.mime.text import MIMEText
# import sqlite3
# import traceback
# import icon

class open_main(QMainWindow):
    def __init__(self):
        super(open_main, self).__init__()
        self.imgPath = None
        loadUi('water.ui', self)
        self.Return = ()
        self.btnHome.clicked.connect(lambda : self.stackedWidget.setCurrentWidget(self.RevBuz))
        self.btnContact.clicked.connect(lambda : self.stackedWidget.setCurrentWidget(self.About))
        self.btnRateUs.clicked.connect(lambda : self.stackedWidget.setCurrentWidget(self.Comment))
        self.btnAddBuz.clicked.connect(lambda : self.stackedWidget.setCurrentWidget(self.AddBuz))
        self.btnReply.clicked.connect(lambda : self.stackedWidget.setCurrentWidget(self.AddReply))
        self.tblBusiness_2.itemClicked.connect(lambda : self.stackedWidget.setCurrentWidget(self.Comment))
        self.tblBusiness_3.itemClicked.connect(lambda : self.stackedWidget.setCurrentWidget(self.Reply))
        self.pushButton_3.clicked.connect(self.save_information)
        self.pushButton_18.clicked.connect(self.exitApplication)
        # self.pushButton_12.clicked.connect(self. save_infos)
        self.insert.clicked.connect(self.open_file_dialog)
        self.btnReset.clicked.connect(self.resetData)
        self.btnAdd.clicked.connect(self.addData)
        self.btnUpdate.clicked.connect(self.updateData)
        self.btnDelete.clicked.connect(self.deleteData)
        self.tblBusiness.itemClicked.connect(self.on_table_clicked)
        self.pushButton.clicked.connect(self.searchLocation)
        self.load_2.clicked.connect(self.searchLocation1)
        self.load_3.clicked.connect(self.searchLocation2)
        self.pushButton.clicked.connect(self.searchLocation)
        self.pushButton.clicked.connect(self.apply_filter)
        self.pushButton_2.clicked.connect(self.send_email)
        self.btnContact_2.clicked.connect(self.exportToSheet)
        self.pushButton_3.clicked.connect(self.save_data)
        self.pushButton_12.clicked.connect(self.data)
        self.tblBusiness.setColumnHidden(4, True)
        self.loadData()
        # pushButton_2 = QPushButton("Send Email")``
        # pushButton_2.clicked.connect(lambda: send_email(None))

    def save_data(self):
        # Assuming self.lineEdit_4 and self.lineEdit_2 are QLineEdit widgets
        water_Id = self.lineEdit_4.text()
        Reply = self.lineEdit_2.text()

        # Create a connection to the database
        self.connection = sqlite3.connect('jj.db')
        self.cursor = self.connection.cursor()

        # Create the table if it doesn't exist
        self.create_table()

        # Insert the information into the database
        query = '''
        INSERT INTO ratings (water_Id, Reply)
        VALUES (?, ?)
        '''
        self.cursor.execute(query, (water_Id, Reply))
        self.connection.commit()

        # Show a message box indicating successful addition and rating
        message = f"Water '{water_Id}' successfully sent: {Reply}"
        QMessageBox.information(self, "Success", message)

    def create_table(self):
        query = '''
        CREATE TABLE IF NOT EXISTS ratings (
            water_Id TEXT,
            Reply TEXT
        )
        '''
        self.cursor.execute(query)
        self.connection.commit()

    

    def send_email(self):
        # Get the contents of textEdit_2 and textEdit_5
        subject = self.textEdit_2.toPlainText()
        body = self.textEdit_5.toPlainText()

        # Get the sender and recipient email addresses
        sender_email = self.textEdit.toPlainText()
        recipient_emails = [self.textEdit_3.toPlainText()]  # Assuming only one recipient for simplicity

        # Change accordingly
        username = "guiddel016@gmail.com"
        password = "dgoq ycmx poli uups"


        # Setup email message
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = ", ".join(recipient_emails)
        message['Subject'] = subject

        # Attach body
        message.attach(MIMEText(body, 'plain'))

        # Attach attachment
        ##attachment_path = 'path_to_your_attachment'  # Provide the path to your attachment file
       # attachment = open(attachment_path, "rb")
        #part = MIMEBase('application', 'octet-stream')
       # part.set_payload((attachment).read())
        #encoders.encode_base64(part)
       # part.add_header('Content-Disposition', "attachment; filename= %s" % attachment_path)
        #message.attach(part)hfnmewrokfpl,werfijomkwep,lf

        # Connect to SMTP server and send email
        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(username, password)
            server.sendmail(sender_email, recipient_emails, message.as_string())
            server.quit()
            print("Email sent successfully!")
        except Exception as e:
            print("An error occurred while sending the email:", str(e))

    def exportToSheet(self):
        workbook = openpyxl.Workbook()
        sheet = workbook.active

        for row in range(self.tblBusiness.rowCount()):
            rowData = []
            for column in range(self.tblBusiness.columnCount()):
                item = self.tblBusiness.item(row, column)
                if item is not None:
                    rowData.append(item.text())
                else:
                    rowData.append("")

            sheet.append(rowData)

        workbook.save("output.xlsx")

    def exitApplication(self):
        QtWidgets.QApplication.quit()  

    def data(self):
        # Assuming self.lineEdit_4 and self.lineEdit_2 are QLineEdit widgets
        water_Id = self.lineEdit_9.text()
        Comment= self.lineEdit_7.text()
        Reply = self.lineEdit_8.text()

        # Create a connection to the database
        self.connection = sqlite3.connect('ratings.db')
        self.cursor = self.connection.cursor()

        # Create the table if it doesn't exist
        self.create_table()

        # Insert the information into the database
        query = '''
        INSERT INTO ratings (water_Id, Comment,Reply)
        VALUES (?, ?,?)
        '''
        self.cursor.execute(query, (water_Id, Comment,Reply))
        self.connection.commit()

        # Show a message box indicating successful addition and rating
        message = f"Water '{water_Id}' successfully sent: {Reply}"
        QMessageBox.information(self, "Success", message)

    def create_table(self):
        query = '''
        CREATE TABLE IF NOT EXISTS ratings (
            water_Id TEXT,
            Comment TEXT
            Reply TEXT
        )
        '''
        self.cursor.execute(query)
        self.connection.commit()

    def create_table(self):
        # Execute a query to create the table if it doesn't exist
        query = '''
        CREATE TABLE IF NOT EXISTS ratings (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            BUSINESS_NAME TEXT,
            DESCRIPTION TEXT,
            RATE_US INTEGER,
            LIKE_DISLIKE TEXT,
            COMMENT TEXT
        )
        '''

    def save_information(self):
        button = self.sender()
        button.setStyleSheet("background-color: yellow;")

        # Create a connection to the database
        self.connection = sqlite3.connect('ratings.db')
        self.cursor = self.connection.cursor()

        # Create the table if it doesn't exist
        self.create_table()

        # Get the information from the UI
        business_name = self.lineEdit_3.text()
        description = self.lineEdit_2.text()
        rate_us = self.comboBox.currentIndex()
        like_dislike = "LIKE" if self.radioButton.isChecked() else "DISLIKE"
        comment = self.lineEdit.text()

        # Insert the information into the database
        query = '''
        INSERT INTO ratings (BUSINESS_NAME, DESCRIPTION, RATE_US, LIKE_DISLIKE, COMMENT)
        VALUES (?, ?, ?, ?, ?)
        '''
        self.cursor.execute(query, (business_name, description, rate_us, like_dislike, comment))
        self.connection.commit()

        # Show a message box indicating successful addition and rating
        message = f"Business '{business_name}' successfully added with rating: {rate_us}"
        QMessageBox.information(self, "Success", message)

        

    # def save_infos(self):
    #     button = self.sender()
    #     button.setStyleSheet("background-color: yellow;")

    #     # Create a connection to the database
    #     self.connection = sqlite3.connect('ratings.db')
    #     self.cursor = self.connection.cursor()

    #     # Create the table if it doesn't exist
    #     self.create_table()

    #     # Get the information from the UI
    #     business_name = self.lineEdit_3.text()
    #     description = self.lineEdit_2.text()
    #     rate_us = self.comboBox.currentIndex()
    #     like_dislike = "LIKE" if self.radioButton.isChecked() else "DISLIKE"
    #     comment = self.lineEdit.text()

    #     # Insert the information into the database
    #     query = '''
    #     INSERT INTO ratings (BUSINESS_NAME, DESCRIPTION, RATE_US, LIKE_DISLIKE, COMMENT)
    #     VALUES (?, ?, ?, ?, ?)
    #     '''
    #     self.cursor.execute(query, (business_name, description, rate_us, like_dislike, comment))
    #     self.connection.commit()

    #     # Retrieve the business name and comment from the database
    #     query = '''
    #     SELECT BUSINESS_NAME, COMMENT
    #     FROM ratings
    #     WHERE BUSINESS_NAME = ?
    #     '''
    #     self.cursor.execute(query, (business_name,))
    #     result = self.cursor.fetchone()

    #     # Display the retrieved information in the UI
    #     if result:
    #         self.lineEdit_9.setText(result[0])  # Set the text of lineEdit_9 with the retrieved business name
    #         self.lineEdit_7.setText(result[1])  # Set the text of lineEdit_7 with the retrieved comment
    #     else:
    #         self.lineEdit_9.setText("")  # Clear the text of lineEdit_9 if no result found
    #         self.lineEdit_7.setText("")  # Clear the text of lineEdit_7 if no result found

    #     # Show a message box indicating successful addition and rating
    #     message = f"Business '{business_name}' successfully added with rating: {rate_us}"
    #     QMessageBox.information(self, "Success", message)
    def searchLocation(self):
        # Search for the location entered in lineEdit
        location_name = self.lineEdit.text()
        if location_name:
            # Construct the Google Maps URL for the location
            map_url = "https://www.google.com/maps/search/?api=1&query=" + location_name
            QDesktopServices.openUrl(QUrl(map_url))
    def searchLocation1(self):
        # Search for the location entered in lineEdit
        location_name = self.lineEdit_5.text()
        if location_name:
            # Construct the Google Maps URL for the location
            map_url = "https://www.google.com/maps/search/?api=1&query=" + location_name
            QDesktopServices.openUrl(QUrl(map_url))
    def searchLocation2(self):
        # Search for the location entered in lineEdit
        location_name = self.lineEdit_6.text()
        if location_name:
            # Construct the Google Maps URL for the location
            map_url = "https://www.google.com/maps/search/?api=1&query=" + location_name
            QDesktopServices.openUrl(QUrl(map_url))

    def loadData(self):
        self.connection = sqlite3.connect("ratings.db")
        self.cursor = self.connection.cursor()
        sqlQuery = "SELECT * FROM ratings ";
        self.tblBusiness.setRowCount(50);
        self.tblBusiness_2.setRowCount(50);
        self.tblBusiness_3.setRowCount(50);
        tablerow = 0
        for row in self.cursor.execute(sqlQuery):
            self.image_label = QLabel();
            self.image_label2 = QLabel();
            self.image_label3 = QLabel()

            pixmap = QPixmap(QTableWidgetItem(row[1]).text())
            pixmap = pixmap.scaledToWidth(100)
            pixmap = pixmap.scaledToHeight(50)
            self.image_label.setPixmap(pixmap)
            self.image_label2.setPixmap(pixmap)
            self.image_label3.setPixmap(pixmap)
            self.tblBusiness.setItem(tablerow, 1, QTableWidgetItem(row[2]))
            self.tblBusiness.setItem(tablerow, 2, QTableWidgetItem(row[3]))
            self.tblBusiness.setItem(tablerow, 3, QTableWidgetItem(row[4]))
            self.tblBusiness.setCellWidget(tablerow, 0, self.image_label)
            self.tblBusiness.setItem(tablerow, 4, QTableWidgetItem(row[1]))

            self.tblBusiness_2.setItem(tablerow, 1, QTableWidgetItem(row[2]))
            self.tblBusiness_2.setItem(tablerow, 2, QTableWidgetItem(row[3]))
            self.tblBusiness_2.setItem(tablerow, 3, QTableWidgetItem(row[4]))
            self.tblBusiness_2.setItem(tablerow, 4, QTableWidgetItem(row[5]))
            self.tblBusiness_2.setItem(tablerow, 5, QTableWidgetItem(row[7]))
            self.tblBusiness_2.setItem(tablerow, 6, QTableWidgetItem(row[8]))
            self.tblBusiness_2.setCellWidget(tablerow, 0, self.image_label2)

            self.tblBusiness_3.setItem(tablerow, 1, QTableWidgetItem(row[2]))
            self.tblBusiness_3.setItem(tablerow, 2, QTableWidgetItem(row[3]))
            self.tblBusiness_3.setItem(tablerow, 3, QTableWidgetItem(row[4]))
            self.tblBusiness_3.setItem(tablerow, 4, QTableWidgetItem(row[5]))
            self.tblBusiness_3.setItem(tablerow, 5, QTableWidgetItem(row[7]))
            self.tblBusiness_3.setItem(tablerow, 6, QTableWidgetItem(row[8]))
            self.tblBusiness_3.setCellWidget(tablerow, 0, self.image_label3)
            tablerow +=1
    def resetData(self):
        self.txtName.setText("")
        self.txtAbout.setText("")
        self.txtAddress.setText("")

        self.profile.setIcon(QIcon())

    def open_file_dialog(self):
        options = QFileDialog.Options()
        file_dialog = QFileDialog()
        file_dialog.setOptions(options)
        file_dialog.setNameFilter("Images (*.png *.jpg *.jpeg *.bmp *.gif)")

        # Get the selected file path
        file_path, _ = file_dialog.getOpenFileName(self, "Select Image", "",
                                                   "Images (*.png *.jpg *.jpeg *.bmp *.gif)")

        if file_path:
            # Update the button's icon with the selected image file
            icon = QIcon(file_path)
            self.profile.setIcon(icon)
            self.imgPath = file_path;

    def addData(self):
        try:
            name = self.txtName.text()
            about = self.txtAbout.text()
            address = self.txtAddress.text()
            if self.txtName.text() == "" or self.txtAbout.text() == "" or self.txtAddress.text() == "":
                QMessageBox.critical(self, "Error", "Please fill in empty fields")
                return

            connection = sqlite3.connect("ratings.db")
            cur = connection.cursor()
            cur.execute("SELECT * FROM ratings WHERE WATER_ID = ?", (name,))
            existingData = cur.fetchone()
            if existingData:
                QMessageBox.critical(self, 'Duplicated Entry ', 'Data already exist in database.')
            else:
                cur.execute("INSERT INTO ratings (BUSINESS_IMAGE,WATER_ID, DESCRIPTION, ADDRESS)VALUES (?, ?, ?, ?)",
                            (self.imgPath, name, about, address))
                connection.commit()
                QMessageBox.information(self, "Success", "Data inserted successfully.")
                self.loadData()
        except Exception as e:
            traceback.print_exc()

    def updateData(self):
        try:
            name = self.txtName.text()
            about = self.txtAbout.text()
            address = self.txtAddress.text()
            if self.txtName.text() == "" or self.txtAbout.text() == "" or self.txtAddress.text() == "":
                QMessageBox.critical(self, "Error", "Please fill in empty fields")
                return

            connection = sqlite3.connect("ratings.db")
            cur = connection.cursor()
            cur.execute("SELECT * FROM ratings WHERE BUSINESS_NAME = ?", (name,))
            existingData = cur.fetchone()
            if existingData:
                cur.execute("UPDATE ratings SET BUSINESS_IMAGE = ?, DESCRIPTION = ?, ADDRESS = ? WHERE WATER_ID = ?",
                            (self.imgPath, about, address, name))
                connection.commit()
                self.loadData()
                QMessageBox.information(self, "Success", "Data Updated successfully!")

            else:
                QMessageBox.information(self, "Error", "Data not found for Updating")
        except Exception as e:
            traceback.print_exc()

    def deleteData(self):
        try:
            name = self.txtName.text()
            about = self.txtAbout.text()
            address = self.txtAddress.text()
            if self.txtName.text() == "" or self.txtAbout.text() == "" or self.txtAddress.text() == "":
                QMessageBox.critical(self, "Error", "Please fill in empty fields")
                return

            self.connection = sqlite3.connect("ratings.db")
            self.cursor = self.connection.cursor()
            self.cursor.execute("SELECT * FROM ratings WHERE WATER_ID = ?", (name,))
            existingData = self.cursor.fetchone()
            if existingData:
                self.cursor.execute("DELETE FROM ratings WHERE WATER_ID= ?",
                            (name,))
                self.connection.commit()
                QMessageBox.information(self, "Success", "Data deleted successfully!")
                self.loadData
            else:
                QMessageBox.information(self, "Error", "Data not found for deleting")
            self.loadData()
        except Exception as e:
            traceback.print_exc()

    def on_table_clicked(self, item):
        try:
            row = item.row()
            self.txtName.setText(self.tblBusiness.item(row, 1).text())
            self.txtAbout.setText(self.tblBusiness.item(row, 2).text())
            self.txtAddress.setText(self.tblBusiness.item(row, 3).text())
            imagePath = self.tblBusiness.item(row, 4).text()
            self.imgPath = imagePath
            icon = QIcon(self.imgPath)
            self.profile.setIcon(icon)
        except:
            traceback.print_exc()
    def apply_filter(self):
        try:
            filter_text = self.lineEdit.text()
            for row in range(self.tblBusiness.rowCount()):
                row_text = " ".join(
                    self.tblBusiness.item(row, col).text().lower()

                    for col in range(self.tblBusiness.columnCount())
                )
                if filter_text in row_text:
                    self.tblBusiness.setRowHidden(row, False)
                else:
                    self.tblBusiness.setRowHidden(row, True)
        except Exception as e:
            traceback.print_exc()

app = QApplication(sys.argv)
window = open_main()
window.show()
try:
    sys.exit(app.exec())
except:
    print('exiting')
