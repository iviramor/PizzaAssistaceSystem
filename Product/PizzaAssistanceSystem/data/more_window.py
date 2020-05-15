from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QPushButton, QWidget, QTableWidgetItem
from PyQt5.QtCore import *

import DATABASE
from notification import *

formSettingsWin = uic.loadUiType("Interface files/Settings.ui")[0]
formInfoOrders = uic.loadUiType("Interface files/inf_window.ui")[0]

class SettingsClass(formSettingsWin, QWidget):
	'''Окно с настройками'''

	def __init__(self, obj, data, db):
		QWidget.__init__(self, None)
		self.setupUi(self)
		self.userData = data
		self.wt = obj
		self.db = db
		self.__fillData()
		self.__saveClick()
		self.__setModality()


	def __setModality(self):
		self.positionEdit.setDisabled(True)

	def __fillData(self):
		self.fioEdit.setText(self.userData[1])
		self.loginEdit.setText(self.userData[2])
		self.passwordEdit.setText(self.userData[3])
		self.positionEdit.setText(self.userData[4])

	def __saveClick(self):
		self.saveButton.clicked.connect(self.__ifNone)
		self.backButton.clicked.connect(self.close)
		
	def __getData(self):
		self.userNewData[1] = self.fioEdit.text()
		self.userNewData[2] = self.loginEdit.text()
		self.userNewData[3] = self.passwordEdit.text()

	def __saveData(self):
		self.userNewData = self.userData
		if self.userData[2] == self.loginEdit.text():
			self.__getData()
			self.db.updDataBase(self.userNewData)
			self.__completed()
			self.__setName(self.userNewData)
		else:
			self.__getData()
			self.__updDataBase(self.userNewData)

	def __setName(self, data):
		self.wt.userData = data
		self.wt.setName()

	def __updDataBase(self, data):
		data = self.db.editDataWorker(data)
		if data == False:
			self.ews = ErrorClass()
			self.ews.label.setText("Неверный логин, с таким логином человек уже есть")
			self.ews.show()
		else:
			self.__completed()
			self.__setName(self.userNewData)

	def __ifNone(self):
		if len(self.fioEdit.text()) == 0 or len(self.loginEdit.text()) == 0 or len(self.passwordEdit.text()) == 0:
			self.ew = ErrorClass()
			self.ew.label.setText("Заполните поля для ввода!")
			self.ew.show()
		else:
			self.__saveData()

	def __completed(self):
		self.mbc = MessBoxClass()
		self.mbc.label.setText("Данные успешно изменены")
		self.mbc.show()

class InfoWindow(formInfoOrders, QWidget):
	"""Информация о товаре"""

	def __init__(self, obj, idOrder):
		QWidget.__init__(self, None)
		self.setupUi(self)
		self.setWindowModality(Qt.ApplicationModal)
		self.idOrder = idOrder
		self.setWindowTitle("Информация заказа: "+str(idOrder))
		self.obj = obj
		self.__clBut()
		self.__getInfData()

	def __clBut(self):
		self.backButton.clicked.connect(self.close)
		self.listWidget.itemClicked.connect(self.__addDataToProduct)

	def __getInfData(self):
		self.db = DATABASE.InoWindow()
		self.arrDataProduct = list(list(self.db.getInfoProduct(self.idOrder)[0]))
		self.__setDataText()
		self.__getInfToProduct()

	def __getInfToProduct(self):
		self.arrDataToProduct = list(self.db.getIfoToProduct(self.arrDataProduct[0]))
		self.__addItemToList(self.arrDataToProduct)

	def __addItemToList(self, data):
		for row in range(len(data)):
			self.listWidget.insertItem(row, data[row][1])

	def __addDataToProduct(self):
		row = self.listWidget.currentRow()
		self.nameDesForm.setText(str(self.arrDataToProduct[row][1]))
		self.descriptionEdit.setText(str(self.arrDataToProduct[row][2]))

	def __setDataText(self):
		self.idForm.setText(str(self.arrDataProduct[0]))
		self.nameForm.setText(str(self.arrDataProduct[1]))
		self.priceForm.setText(str(self.arrDataProduct[2]))
		self.queEdit.setText(str(self.arrDataProduct[3]))
		self.comEdit.setText(str(self.arrDataProduct[4]))