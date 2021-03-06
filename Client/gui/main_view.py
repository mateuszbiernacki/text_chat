# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Client\gui\qt_des\main_view.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 572)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.list_of_friends = QtWidgets.QListWidget(self.centralwidget)
        self.list_of_friends.setGeometry(QtCore.QRect(10, 40, 171, 361))
        self.list_of_friends.setObjectName("list_of_friends")
        item = QtWidgets.QListWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.list_of_friends.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.list_of_friends.addItem(item)
        self.real_chat_area = QtWidgets.QTextBrowser(self.centralwidget)
        self.real_chat_area.setGeometry(QtCore.QRect(320, 40, 461, 431))
        self.real_chat_area.setObjectName("real_chat_area")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(320, 480, 361, 71))
        self.textEdit.setObjectName("textEdit")
        self.send_message_button = QtWidgets.QPushButton(self.centralwidget)
        self.send_message_button.setGeometry(QtCore.QRect(690, 480, 91, 71))
        self.send_message_button.setObjectName("send_message_button")
        self.line_friend_to_invite = QtWidgets.QLineEdit(self.centralwidget)
        self.line_friend_to_invite.setGeometry(QtCore.QRect(10, 440, 171, 20))
        self.line_friend_to_invite.setObjectName("line_friend_to_invite")
        self.send_invite_button = QtWidgets.QPushButton(self.centralwidget)
        self.send_invite_button.setGeometry(QtCore.QRect(190, 440, 75, 23))
        self.send_invite_button.setObjectName("send_invite_button")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 20, 47, 13))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 420, 151, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(310, 20, 131, 16))
        self.label_3.setObjectName("label_3")
        self.log_out_button = QtWidgets.QPushButton(self.centralwidget)
        self.log_out_button.setGeometry(QtCore.QRect(710, 10, 75, 23))
        self.log_out_button.setObjectName("log_out_button")
        self.delete_friend_list_buton = QtWidgets.QPushButton(self.centralwidget)
        self.delete_friend_list_buton.setGeometry(QtCore.QRect(190, 40, 75, 23))
        self.delete_friend_list_buton.setObjectName("delete_friend_list_buton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        __sortingEnabled = self.list_of_friends.isSortingEnabled()
        self.list_of_friends.setSortingEnabled(False)
        item = self.list_of_friends.item(0)
        item.setText(_translate("MainWindow", "test"))
        item = self.list_of_friends.item(1)
        item.setText(_translate("MainWindow", "test2"))
        self.list_of_friends.setSortingEnabled(__sortingEnabled)
        self.send_message_button.setText(_translate("MainWindow", "Send"))
        self.send_invite_button.setText(_translate("MainWindow", "Send Invite"))
        self.label.setText(_translate("MainWindow", "Friends:"))
        self.label_2.setText(_translate("MainWindow", "Invite friend by login:"))
        self.label_3.setText(_translate("MainWindow", "Real Chat:"))
        self.log_out_button.setText(_translate("MainWindow", "Log out"))
        self.delete_friend_list_buton.setText(_translate("MainWindow", "Delete"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
