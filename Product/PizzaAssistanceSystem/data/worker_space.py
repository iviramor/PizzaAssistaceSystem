from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QPushButton, QWidget, QTableWidgetItem
from PyQt5.QtCore import *
import PyQt5.uic as uic
import sys, time, numpy

import DATABASE
import main_window
from more_window import *
from notification import *
from ThreadClass import *

formTableOrders = uic.loadUiType("Interface files/Orders of worker.ui")[0]

class WorkerClass(QMainWindow, formTableOrders):
	'''Рабочее место работника'''

	def __init__(self, data):
		QMainWindow.__init__(self, None)
		self.setupUi(self)
		self.__setWindowText()
		self.__navbar()
		self.__action()
		self.db = DATABASE.WorkerDataTable()
		self.tableObj = TableClass(self)
		self.tableObjMyOrder = TableMyOrdersClass(self)
		self.userData = [data[0][i] for i in range(len(data[0]))]
		self.setName()
		self.tableObj.tableControl()
		self.tableObjMyOrder.tableControl()

	def __setWindowText(self):
		self.setWindowTitle('Заказы работника')
		self.tabWidget.setTabText(0, 'Заказы')
		self.tabWidget.setTabText(1, 'Мои заказы')

	def setName(self):
		self.nameLabel.setText(self.userData[1])

	def __navbar(self):
		self.setButton.clicked.connect(self.__showSettings)
		self.exitButton.clicked.connect(self.__showMainWindow)

	def __action(self):
		self.startButton.clicked.connect(self.__addToMy)
		self.completeButton.clicked.connect(self.__endOrder)
		self.infoButton.clicked.connect(self.__showInfOrders)
		self.infoButton2.clicked.connect(self.__showInfMyOrders)


	def __showSettings(self):
		db = DATABASE.SettingDataWorker()
		self.setwin = SettingsClass(self, self.userData, db)
		self.setwin.setWindowModality(Qt.ApplicationModal)
		self.setwin.show()

	def __showMainWindow(self):
		self.mw = main_window.MainWindowClass()
		self.mw.show()
		self.close()

	def prepare_some_row_data(self, number_of_row):
		self.column_container = [] 
		for column in range(0, self.tableWidget.columnCount()):
			self.column_container.append(self.tableWidget.item(number_of_row, column).text())
		return self.column_container

	def __addToMy(self):
		self.ewao = ErrorClass()
		self.mbao = MessBoxClass()
		idrow = self.tableWidget.currentRow()
		if idrow == -1:
			self.ewao.label.setText("Выберите заказ")
			self.ewao.show()
		else:
			db = DATABASE.WorkerDataTable()
			ans = db.addStatus(self.tableWidget.item(idrow, 0).text(), self.userData[0])
			if ans:
				self.tableObjMyOrder.tableControl()
				self.mbao.label.setText("Заказ добавлен на выполнение")
				self.mbao.show()
			else:
				self.ewao.label.setText("Заказ занят или уже выполнен")
				self.ewao.show()

	def __endOrder(self):
		self.eweo = ErrorClass()
		self.mbeo = MessBoxClass()
		idrow = self.tableWidgetOrders.currentRow()
		if idrow == -1:
			self.eweo.label.setText("Выберите заказ")
			self.eweo.show()
		else:
			ans = self.db.completStatus(self.tableWidgetOrders.item(idrow, 0).text())
			if ans:
				self.tableObjMyOrder.tableControl()
				self.mbeo.label.setText("Статус заказа Выполнено")
				self.mbeo.show()
			else:
				self.mbeo.label.setText("Заказ уже выполнен")
				self.mbeo.show()

	def __showInfMyOrders(self):
		self.ewi = ErrorClass()
		idrow = self.tableWidgetOrders.currentRow()
		if idrow == -1:
			self.ewi.label.setText("Выберите заказ")
			self.ewi.show()
		else:
			self.iwb1 = InfoWindow(self, self.tableWidgetOrders.item(idrow, 0).text())
			self.iwb1.show()

	def __showInfOrders(self):
		self.ewi = ErrorClass()
		idrow = self.tableWidget.currentRow()
		if idrow == -1:
			self.ewi.label.setText("Выберите заказ")
			self.ewi.show()
		else:
			self.iwb0 = InfoWindow(self, self.tableWidget.item(idrow, 0).text())
			self.iwb0.show()


class TableClass():
	"""Процессы с таблицой"""

	def __init__(self, obj):
		self.obj = obj
		self.currentdb = None
		self.thread = ProgressThread(self)
		self.__timer(True)

	def __timer(self, bool):
		if bool:
			self.timer = QTimer()
			self.timer.timeout.connect(self.startThread)
			self.timer.start(5000)

	def __converter(self, data, obj):
		for x in range(len(data)):
			d = data[x]
			data[x] = list(map(obj, d))
		return data

	def __saveCurrentdb(self):
		db = DATABASE.WorkerDataTable()
		self.currentdb = list(db.getData())

	def tableControl(self):
		db = DATABASE.WorkerDataTable()
		self.__saveCurrentdb()
		data = list(db.getData())
		self.__setRow(data)
		data = self.__converter(data, str)
		data = self.__converter(data, QTableWidgetItem)
		for row in range(len(data)):
			for column in range(len(data[row])):
				self.obj.tableWidget.setItem(row, column, data[row][column])

	def __cleaningTable(self, d):
		for i in range(1, len(d)+1):
			self.obj.tableWidget.removeRow(i)

	def __setRow(self, d):
		self.obj.tableWidget.setRowCount(len(d))

	def __getData(self):
		self.__saveCurrentdb()
		db = DATABASE.WorkerDataTable()
		data = list(db.getData())
		self.__setRow(data)
		data = self.__convertData(data)
		self.__updateTableData(data)

	def __convertData(self, data):
		data = self.__converter(data, str)
		data = self.__converter(data, QTableWidgetItem)
		return data

	def __updateTableData(self, data):
		for row in range(len(data)):
			for column in range(len(data[row])):
				self.obj.tableWidget.setItem(row, column, data[row][column])

	def startUpdate(self):
		db = DATABASE.WorkerDataTable()
		data = list(db.getData())
		if not(numpy.array_equal(data, self.currentdb)):
			self.__cleaningTable(self.currentdb)
			self.__getData()
			self.thread.quit()

	def startThread(self):
		self.thread.getMethods(self.startUpdate)
		self.thread.start()


class TableMyOrdersClass():
	"""Таблица выполняемых заказов рабочего"""

	def __init__(self, obj):
		self.obj = obj

	def __converter(self, data, obj):
		for x in range(len(data)):
			d = data[x]
			data[x] = list(map(obj, d))
		return data

	def __setRow(self, d):
		self.obj.tableWidgetOrders.setRowCount(len(d))

	def tableControl(self):
		db = DATABASE.WorkerDataTable()
		data = list(db.getMyOrdersData(self.obj.userData[0]))
		self.__setRow(data)
		data = self.__converter(data, str)
		data = self.__converter(data, QTableWidgetItem)
		for row in range(len(data)):
			for column in range(len(data[row])):
				self.obj.tableWidgetOrders.setItem(row, column, data[row][column])
