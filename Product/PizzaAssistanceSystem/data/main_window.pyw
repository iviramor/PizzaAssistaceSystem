from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QWidget, QPushButton, QErrorMessage, QMessageBox
from PyQt5.QtCore import *
import PyQt5.uic as uic
import sys

import DATABASE
import admin_space
import worker_space
from notification import *

formMain = uic.loadUiType("Interface files/main.ui")[0]
formAdminSignIn = uic.loadUiType("Interface files/Admin Sign In.ui")[0]
formAdminReg = uic.loadUiType("Interface files/Admin reg.ui")[0]
formWorkSignIn = uic.loadUiType("Interface files/Work Sign In.ui")[0]
formWorkReg = uic.loadUiType("Interface files/Work reg.ui")[0]

class MainWindowClass(QMainWindow, formMain):
	'''Главное окно'''

	def __init__(self):
		QMainWindow.__init__(self, None)
		self.setupUi(self)
		self.setWindowTitle('PizzaAssistanceSystem')
		self.gotoWork()
		self.gotoAdmin()

	def gotoWork(self):
		self.workButton.clicked.connect(self.showWorkWindow)

	def showWorkWindow(self):
		self.wsi = WorkerSignIn()
		self.wsi.show()
		self.close()

	def gotoAdmin(self):
		self.adminButton.clicked.connect(self.showAdminWindow)

	def showAdminWindow(self):
		self.asi = AdminSignIn()
		self.asi.show()
		self.close()


class WorkerSignIn(QMainWindow, formWorkSignIn):
	'''Окно входа рабочего'''

	def __init__(self):
		QMainWindow.__init__(self, None)
		self.db = DATABASE.SingInWorker()
		self.setupUi(self)
		self.setWindowTitle('Окно входа')
		self.gotoReg()
		self.checking()
		self.gotoMain()

	def gotoMain(self):
		self.backButton.clicked.connect(self.showMain)

	def showMain(self):
		self.mw = MainWindowClass()
		self.mw.show()
		self.close()

	def gotoReg(self):
		self.signButton.clicked.connect(self.show_RegWindow)

	def show_RegWindow(self):
		self.wr = RegWorkWindow()
		self.wr.setWindowModality(Qt.ApplicationModal)
		self.wr.show()

	def checking(self):
		self.loginButton.clicked.connect(self.check)

	def getData(self):
		userLogin = self.loginLine.text()
		userPassword = self.passLine.text()
		return [userLogin, userPassword]

	def check(self):
		data = self.db.singInDbWorker(self.getData())
		if data != False:
			self.close()
			self.ws = worker_space.WorkerClass(data)
			self.ws.show()
		else:
			self.ew = ErrorClass()
			self.ew.show()


class AdminSignIn(QMainWindow, formAdminSignIn):
	'''Окно входа админа'''

	def __init__(self):
		QMainWindow.__init__(self, None)
		self.db = DATABASE.SingInAdmin()
		self.setupUi(self)
		self.setWindowTitle('Окно входа')
		self.gotoReg()
		self.checking()
		self.gotoMain()

	def gotoMain(self):
		self.backButton.clicked.connect(self.showMain)

	def showMain(self):
		self.mw = MainWindowClass()
		self.mw.show()
		self.close()

	def gotoReg(self):
		self.signButton.clicked.connect(self.show_RegWindow)

	def show_RegWindow(self):
		self.rw = RegAdminWindow()
		self.rw.setWindowModality(Qt.ApplicationModal)
		self.rw.show()

	def checking(self):
		self.loginButton.clicked.connect(self.check)

	def getData(self):
		userLogin = self.loginLine.text()
		userPassword = self.passLine.text()
		return [userLogin, userPassword]

	def check(self):
		data = self.db.singInDbSearch(self.getData())
		if data != False:
			self.close()
			self.adms = admin_space.AdminTableClass(data)
			self.adms.show()
		else:
			self.ew = ErrorClass()
			self.ew.show()


class RegWorkWindow(QDialog, formWorkReg):
	'''Окно регистрации рабочего'''

	def __init__(self):
		QWidget.__init__(self, None)
		self.db = DATABASE.SingUpWorker()
		self.setupUi(self)
		self.setWindowTitle('Окно регистрации')
		self.registration()
		self.backToMain()

	def registration(self):
		self.regButton.clicked.connect(self.ifZero)

	def showMessBox(self):
		self.mb = MessBoxClass()
		self.mb.show()

	def backToMain(self):
		self.backButton.clicked.connect(self.close)

	def showMainWin(self):
		self.wsi = WorkerSignIn()
		self.wsi.show()

	def ifZero(self):
		if len(self.nameLine.text()) == 0 or len(self.loginLine.text()) == 0 or len(self.passLine.text()) == 0:
			self.ew = ErrorClass()
			self.ew.label.setText("Заполните поля для ввода!")
			self.ew.show()
		else:
			self.getTextToDB()

	def getText(self):
		userName = self.nameLine.text()
		userLogin = self.loginLine.text()
		userPassword = self.passLine.text()
		return [userName, userLogin, userPassword]

	def getTextToDB(self):
		data = self.db.singUpDbWorker(self.getText())
		if data == False:
			self.ew = ErrorClass()
			self.ew.label.setText("Пользователь с таким логином уже есть в системе")
			self.ew.show()
		else:
			self.showMessBox()


class RegAdminWindow(QDialog, formAdminReg):
	'''Окно регистрации админа'''

	def __init__(self):
		QWidget.__init__(self, None)
		self.db = DATABASE.SingUpAdmin()
		self.setupUi(self)
		self.setWindowTitle('Окно регистрации')
		self.registration() 
		self.backToMain()

	def registration(self):
		self.regButton.clicked.connect(self.ifZero)

	def showMessBox(self):
		self.mb = MessBoxClass()
		self.mb.show()

	def backToMain(self):
		self.backButton.clicked.connect(self.close)

	def ifZero(self):
		if len(self.nameLine.text()) == 0 or len(self.loginLine.text()) == 0 or len(self.passLine.text()) == 0:
			self.ew = ErrorClass()
			self.ew.label.setText("Заполните поля для ввода!")
			self.ew.show()
		else:
			self.getTextToDB()

	def getText(self):
		userName = self.nameLine.text()
		userLogin = self.loginLine.text()
		userPassword = self.passLine.text()
		return [userName, userLogin, userPassword]

	def getTextToDB(self):
		data = self.db.singUpDbAdmin(self.getText())
		if data == False:
			self.ew = ErrorClass()
			self.ew.label.setText("Пользователь с таким логином уже есть в системе")
			self.ew.show()
		else:
			self.showMessBox()

def setting():
	e = QErrorMessage()
	db = DATABASE.ConnectToDataBase()
	try:
		countTable = len(db.testServer())
		if countTable >= 7:
			return True
		else:
			e.showMessage('Ошибка: нехватает таблиц. Проверьте наличие всех необходимых таблиц и попробуйте снова')
			e.exec_()
	except:
		e.showMessage('Ошибка: не подключена база данных иди неверные данные пользователя в "settingDataBase". Проверьте данные и попробуйте снова')
		e.exec_()
		return False


if __name__ == "__main__":
	app = QApplication(sys.argv)
	if setting():
		MainWindow = MainWindowClass()
		MainWindow.show()
		app.exec_()
