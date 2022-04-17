from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QWidget, QPushButton
from PyQt5.QtCore import *
import PyQt5.uic as uic
import sys

formError = uic.loadUiType("Interface files/Error.ui")[0]
formMessBox = uic.loadUiType("Interface files/MessBox.ui")[0]
class ErrorClass(QWidget, formError):
	'''Окно ошибки'''

	def __init__(self):
		QWidget.__init__(self, None)
		self.setMode()
		self.setupUi(self)
		self.closing()

	def closing(self):
		self.okButton.clicked.connect(self.close)

	def setMode(self):
		self.setWindowModality(Qt.ApplicationModal)


class MessBoxClass(QWidget, formMessBox):
	'''Окно оповещения'''

	def __init__(self):
		QWidget.__init__(self, None)
		self.setupUi(self)
		self.label.setText("Вы успешно зарегистрированы в системе!")
		self.setWindowTitle('Успех!')
		self.setMode()
		self.closing()

	def closing(self):
		self.okButton.clicked.connect(self.close)

	def setMode(self):
		self.setWindowModality(Qt.ApplicationModal)

class MessBox1CClass(QWidget, formMessBox):
	'''Окно оповещения'''

	def __init__(self):
		QWidget.__init__(self, None)
		self.setupUi(self)
		self.label.setText("Произведен экспорт в 1С!")
		self.setWindowTitle('Успех!')
		self.setMode()
		self.closing()

	def closing(self):
		self.okButton.clicked.connect(self.close)

	def setMode(self):
		self.setWindowModality(Qt.ApplicationModal)