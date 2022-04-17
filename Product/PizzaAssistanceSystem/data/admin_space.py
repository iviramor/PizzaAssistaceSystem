from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QPushButton, QWidget, QTableWidgetItem
from PyQt5.QtCore import *
import PyQt5.uic as uic
import sys, time, numpy, datetime
import xlsxwriter

import DATABASE
import main_window
from more_window import *
from notification import *
from ThreadClass import *

formTableOrders = uic.loadUiType("Interface files/Orders of admin.ui")[0]
formInfProduct = uic.loadUiType("Interface files/inf_product_window.ui")[0]
formEditProduct = uic.loadUiType("Interface files/edit_product_window.ui")[0]
formAddToProduct = uic.loadUiType("Interface files/addItemWindow.ui")[0]
formAddNewToProduct = uic.loadUiType("Interface files/add_new_product_window.ui")[0]

class AdminTableClass(QMainWindow, formTableOrders):
	"""Рабочее место админа"""

	def __init__(self, data):
		QMainWindow.__init__(self, None)
		self.setupUi(self)
		self.__setWindowText()
		self.__navbar()
		self.__action()
		self.db = DATABASE.AdminDataTable()
		self.prodtabl = ProductsTableClass(self)
		self.orderTable = TableClass(self)
		self.searckOrdAdm = SearchOrderAdmin(self, self.orderTable)
		self.userData = [data[0][i] for i in range(len(data[0]))]
		self.setName()
		self.prodtabl.tableControl()
		self.orderTable.tableControl()
		self.__searchToOrd()
		self.analWin = AnalWindow(self)

	def __setWindowText(self):
		self.tabWidget.setTabText(0, 'Ассортимент')
		self.tabWidget.setTabText(1, 'Данные заказов')
		self.tabWidget.setTabText(2, 'Аналитика и отчет')

	def setName(self):
		self.nameLabel.setText(self.userData[1])

	def __navbar(self):
		self.setButton.clicked.connect(self.__showSettings)
		self.exitButton.clicked.connect(self.__showMainWindow)

	def __action(self):
		self.infoButton2.clicked.connect(self.__showInfOrders)
		self.infoProdButton.clicked.connect(self.__showInfProduct)
		self.udateProdButton.clicked.connect(self.__showEditProduct)
		self.addProdButton.clicked.connect(self.__showAddNewProgWindow)

	def __searchToOrd(self):
		self.searchButton.clicked.connect(self.searckOrdAdm.searchTable)
		self.falseButton.clicked.connect(self.searckOrdAdm.onTable)
		self.statusBox.activated.connect(self.searckOrdAdm.blockStatus)

	def __showMainWindow(self):
		self.mw = main_window.MainWindowClass()
		self.mw.show()
		self.close()

	def __showSettings(self):
		db = DATABASE.SettingDataAdmin()
		self.setwin = SettingsClass(self, self.userData, db)
		self.setwin.setWindowModality(Qt.ApplicationModal)
		self.setwin.show()

	def __showInfOrders(self):
		self.ewi = ErrorClass()
		idrow = self.tableWidgetOrders.currentRow()
		if idrow == -1:
			self.ewi.label.setText("Выберите заказ")
			self.ewi.show()
		else:
			self.iwb0 = InfoWindow(self, self.tableWidgetOrders.item(idrow, 0).text())
			self.iwb0.show()

	def __showAddNewProgWindow(self):
		self.anpw = AddNewProductWindow(self)
		self.anpw.show()

	def __showInfProduct(self):
		self.ewp = ErrorClass()
		idrow = self.tableProdWidget.currentRow()
		if idrow == -1:
			self.ewp.label.setText("Выберите заказ")
			self.ewp.show()
		else:
			self.iwp = InfProductWindow(self, self.tableProdWidget.item(idrow, 0).text())
			self.iwp.show()

	def __showEditProduct(self): 
		self.ewp = ErrorClass()
		idrow = self.tableProdWidget.currentRow()
		if idrow == -1:
			self.ewp.label.setText("Выберите заказ")
			self.ewp.show()
		else:
			self.iwp = EditProductWindow(self, self.tableProdWidget.item(idrow, 0).text())
			self.iwp.show()


class ProductsTableClass():
	"""Таблица ассортимента"""

	def __init__(self, obj):
		self.obj = obj

	def __converter(self, data, obj):
		for x in range(len(data)):
			d = data[x]
			data[x] = list(map(obj, d))
		return data

	def __setRow(self, d):
		self.obj.tableProdWidget.setRowCount(len(d))

	def tableControl(self):
		db = DATABASE.AdminDataTable()
		data = list(db.getAllProduct())
		self.__setRow(data)
		data = self.__converter(data, str)
		data = self.__converter(data, QTableWidgetItem)
		for row in range(len(data)):
			for column in range(len(data[row])):
				self.obj.tableProdWidget.setItem(row, column, data[row][column])


class TableClass():
	"""Процессы с таблицой заказов Админ"""

	def __init__(self, obj):
		self.obj = obj
		self.currentdb = None
		self.thread = ProgressThread(self)
		self.timeStatus = True
		self.__timer()

	def __timer(self):
		self.timer = QTimer()
		self.timer.timeout.connect(self.startThread)
		self.timer.start(5000)

	def __converter(self, data, obj):
		for x in range(len(data)):
			d = data[x]
			data[x] = list(map(obj, d))
		return data

	def __saveCurrentdb(self):
		db = DATABASE.AdminDataTable()
		self.currentdb = list(db.getData())

	def tableControl(self):
		db = DATABASE.AdminDataTable()
		self.__saveCurrentdb()
		data = list(db.getData())
		self.__setRow(data)
		data = self.__converter(data, str)
		data = self.__converter(data, QTableWidgetItem)
		for row in range(len(data)):
			for column in range(len(data[row])):
				self.obj.tableWidgetOrders.setItem(row, column, data[row][column])

	def __cleaningTable(self, d):
		for i in range(1, len(d)+1):
			self.obj.tableWidgetOrders.removeRow(i)

	def __setRow(self, d):
		self.obj.tableWidgetOrders.setRowCount(len(d))

	def __getData(self):
		self.__saveCurrentdb()
		db = DATABASE.AdminDataTable()
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
				self.obj.tableWidgetOrders.setItem(row, column, data[row][column])

	def startUpdate(self):
		db = DATABASE.AdminDataTable()
		data = list(db.getData())
		if not(numpy.array_equal(data, self.currentdb)):
			self.__cleaningTable(self.currentdb)
			self.__getData()
			self.thread.quit()

	def startThread(self):
		if self.timeStatus:
			self.thread.getMethods(self.startUpdate)
			self.thread.start()


class SearchOrderAdmin():
	"""Меню поиска"""

	def __init__(self, obj, table):
		self.tableOrd = table
		self.obj = obj
		self.__addWorkersTobox()
		self.blockStatus()

	def __converter(self, data, obj):
		for x in range(len(data)):
			d = data[x]
			data[x] = list(map(obj, d))
		return data

	def __cleaningTable(self, d):
		for row in range(0, len(d)+1):
			self.obj.tableWidgetOrders.removeRow(row)

	def __setRow(self, d):
		self.obj.tableWidgetOrders.setRowCount(len(d))

	def __addWorkersTobox(self):
		db = DATABASE.AdminDataTable()
		data = db.getAllWorkers()
		for row in range(len(data)):
			self.obj.workerBox.addItem(data[row][1])

	def searchTable(self):
		self.tableOrd.timeStatus = False
		if self.obj.statusBox.currentIndex() == 0:
			self.__setDataSearchNew()
		else:
			self.__setDataSearch()

	def onTable(self):
		self.tableOrd.tableControl()
		self.tableOrd.timeStatus = True

	def __setDataSearchNew(self):
		db = DATABASE.AdminDataTable()
		dataRowS = self.obj.statusBox.currentText()
		data = db.searchDataNew(dataRowS)
		if len(data) != 0:
			self.__updateTableData(list(data))
		else:
			self.mbsn = MessBoxClass()
			self.mbsn.setWindowTitle('Пусто')
			self.mbsn.label.setText("Ничего не найдено")
			self.mbsn.show()
			self.onTable()

	def __updateTableData(self, data):
		self.__cleaningTable(data)
		self.__setRow(data)
		data = self.__convertData(data)
		for row in range(len(data)):
			for column in range(len(data[row])):
				self.obj.tableWidgetOrders.setItem(row, column, data[row][column])

	def __convertData(self, data):
		data = self.__converter(data, str)
		data = self.__converter(data, QTableWidgetItem)
		return data

	def __setDataSearch(self):
		db = DATABASE.AdminDataTable()
		dataRowS = self.obj.statusBox.currentText()
		dataRowW = self.obj.workerBox.currentText()
		data = [dataRowS, dataRowW]
		data = db.searchData(data)
		if len(data) != 0:
			self.__updateTableData(list(data))
		else:
			self.mbs = MessBoxClass()
			self.mbs.setWindowTitle('Пусто')
			self.mbs.label.setText("Ничего не найдено")
			self.mbs.show()
			self.onTable()

	def blockStatus(self):
		if self.obj.statusBox.currentIndex() == 0:
			self.obj.workerBox.setDisabled(True)
			return False
		else:
			self.obj.workerBox.setDisabled(False)
			return True


class InfProductWindow(formInfProduct, QWidget):
	"""Окно с информацией о продукте"""

	def __init__(self, obj, idProduct):
		QWidget.__init__(self, None)
		self.setupUi(self)
		self.setWindowModality(Qt.ApplicationModal)
		self.idProduct = idProduct
		self.setWindowTitle("Информация о товаре")
		self.obj = obj
		self.__clBut()
		self.__getInfData()

	def __clBut(self):
		self.backButton.clicked.connect(self.close)
		self.listWidget.itemClicked.connect(self.__addDataToProduct)

	def __getInfData(self):
		self.db = DATABASE.InfProductWindow()
		self.arrDataProduct = list(list(self.db.getInfoProduct(self.idProduct)[0]))
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
		self.priceToProdEdit.setText(str(self.arrDataToProduct[row][3]))

	def __setDataText(self):
		self.idForm.setText(str(self.arrDataProduct[0]))
		self.nameForm.setText(str(self.arrDataProduct[1]))
		self.desProdEdit.setText(str(self.arrDataProduct[2]))
		self.priceProdEdit.setText(str(self.arrDataProduct[3]))
		self.arrDataProduct[4] = self.arrDataProduct[4].split('.')
		self.imgEdit.setText(str(self.arrDataProduct[4][0]))
		self.formatEdit.setText(str(self.arrDataProduct[4][1]))

class AddToProduct(formAddToProduct, QWidget):
	def __init__(self, obj):
		QWidget.__init__(self, None)
		self.setupUi(self)
		self.setWindowModality(Qt.ApplicationModal)
		self.obj = obj
		self.__clBut()

	def __clBut(self):
		self.backButton.clicked.connect(self.close)
		self.okButton.clicked.connect(self.__saveName)

	def __saveName(self):
		data = self.nameToProductEdit.text()
		if len(data) != 0:
			self.obj.addItemtolist(data)
			self.close()
		else: 
			self.ew = ErrorClass()
			self.ew.label.setText("Введите название")
			self.ew.show()

class EditProductWindow(formEditProduct, QWidget):
	"""Окно с информацией о продукте"""

	def __init__(self, obj, idProduct):
		QWidget.__init__(self, None)
		self.setupUi(self)
		self.setWindowModality(Qt.ApplicationModal)
		self.idProduct = idProduct
		self.setWindowTitle("Редактор товара")
		self.imgFormat = ['png', 'jpg', 'jpeg', 'raw']
		self.newItemList = []
		self.obj = obj
		self.tableProd = ProductsTableClass(self.obj)
		self.__clBut()
		self.__getInfData()


	def __converter(self, data, obj): 
		for x in range(len(data)):
			d = data[x]
			data[x] = list(d)
		return data

	def __clBut(self): 
		self.backButton.clicked.connect(self.close)
		self.listWidget.itemClicked.connect(self.__addDataToProduct)
		self.saveButton.clicked.connect(self.__saveDataProduct)
		self.addListButton.clicked.connect(self.__addItemtolistWindow)
		self.saveListButton.clicked.connect(self.__saveDataToList)
		self.delToListButton.clicked.connect(self.__dropRowToTable)

	def __getInfData(self): 
		self.db = DATABASE.EditProduct()
		self.arrDataProduct = list(list(self.db.getInfoProduct(self.idProduct)[0]))
		self.__addFormatTobox()
		self.__setDataText()
		self.__getInfToProduct()

	def __getInfToProduct(self): 
		self.db = DATABASE.EditProduct()
		self.arrDataToProduct = list(self.db.getIfoToProduct(self.arrDataProduct[0]))
		self.arrDataToProduct = self.__converter(self.arrDataToProduct, list)
		self.listWidget.clear()
		self.__addItemToList(self.arrDataToProduct)

	def __addItemToList(self, data): 
		for row in range(len(data)): 
			self.listWidget.insertItem(row, data[row][2])

	def __addFormatTobox(self): 
		data = self.imgFormat
		for row in range(len(data)):
			self.formatBox.addItem(data[row])

	def __addDataToProduct(self):
		row = self.listWidget.currentRow()
		self.nameDesForm.setText(str(self.arrDataToProduct[row][2]))
		self.descriptionEdit.setText(str(self.arrDataToProduct[row][3]))
		self.priceToProdEdit.setText(str(self.arrDataToProduct[row][4]))

	def __setDataText(self): 
		self.idForm.setText(str(self.arrDataProduct[0]))
		self.nameForm.setText(str(self.arrDataProduct[1]))
		self.desProdEdit.setText(str(self.arrDataProduct[2]))
		self.priceProdEdit.setText(str(self.arrDataProduct[3]))
		self.arrDataProduct[4] = self.arrDataProduct[4].split('.')
		self.imgEdit.setText(str(self.arrDataProduct[4][0]))
		index = self.formatBox.findText(self.arrDataProduct[4][1])
		if index >= 0: 
			self.formatBox.setCurrentIndex(index)

	def __addItemtolistWindow(self):
		self.dtp = AddToProduct(self)
		self.dtp.show()

	def addItemtolist(self, data):
		arrData = [self.arrDataProduct[0], data]
		self.db.addToProduct(arrData)
		self.arrDataToProduct = list(self.db.getIfoToProduct(self.arrDataProduct[0]))
		self.arrDataToProduct = self.__converter(self.arrDataToProduct, list)
		self.listWidget.clear()
		self.__addItemToList(self.arrDataToProduct)

	def __saveDataToList(self):
		self.ewl = ErrorClass()
		idrow = self.listWidget.currentRow()
		if idrow == -1:
			self.ewl.label.setText("Выберите пункт")
			self.ewl.show()
		else:
			toProductName = self.nameDesForm.text()
			toProductDes = self.descriptionEdit.toPlainText()
			toProductPrice = self.priceToProdEdit.text()
			try:
				int(toProductPrice)
				arrData = [toProductName, toProductDes, toProductPrice]
				for item in range(2, len(self.arrDataToProduct[idrow])):
					self.arrDataToProduct[idrow][item] = arrData[item-2]
				self.__upDateToProd(self.arrDataToProduct[idrow])
			except:
				self.ewl.label.setText("Цена в цифрах!")
				self.ewl.show()

	def __upDateToProd(self, d):
		self.db.upDateToProduct(d)
		self.__getInfToProduct()
		self.mbc = MessBoxClass()
		self.mbc.label.setText("Данные успешно изменены")
		self.mbc.show()

	def __dropRowToTable(self):
		self.ewdl = ErrorClass()
		idrow = self.listWidget.currentRow()
		if idrow == -1:
			self.ewdl.label.setText("Выберите пункт")
			self.ewdl.show()
		else:
			self.db.dropRowToTable(self.arrDataToProduct[idrow])
			self.__getInfToProduct()
			self.mbc = MessBoxClass()
			self.mbc.label.setText("Успешно удалено")
			self.mbc.show()

	def __saveDataProduct(self):
		idProd = self.idForm.text()
		nameProd = self.nameForm.text()
		priceProd = self.priceProdEdit.text()
		desProd = self.desProdEdit.toPlainText()
		imgProd = self.imgEdit.text()
		formatProg = self.formatBox.currentText()
		try:
			int(priceProd)
			arrData = [idProd, nameProd, desProd, priceProd, imgProd + '.'+ formatProg]
			self.db.savedataProduct(arrData)
			self.tableProd.tableControl()
			self.mbc = MessBoxClass()
			self.mbc.label.setText("Успешно изменено")
			self.mbc.show()
		except:
			self.ewl.label.setText("Цена в цифрах!")
			self.ewl.show()
			self.formatBox.setCurrentIndex(index) 

class AddNewProductWindow(formAddNewToProduct, QWidget):
	"""Окно с добавлением продукта"""

	def __init__(self, obj):
		QWidget.__init__(self, None)
		self.setupUi(self)
		self.setWindowModality(Qt.ApplicationModal)
		self.idNewProduct = None
		self.setWindowTitle("Добавить товар")
		self.imgFormat = ['png', 'jpg', 'jpeg', 'raw']
		self.newItemProd = []
		self.newItemList = []
		self.obj = obj
		self.tableProd = ProductsTableClass(self.obj)
		self.__addFormatTobox()
		self.__setIdNewProd()
		self.__clBut()

	def __setIdNewProd(self):
		db = DATABASE.AddNewProduct()
		self.idNewProduct = db.countRowProd()[0][0]+1

	def __addFormatTobox(self):
		data = self.imgFormat
		for row in range(len(data)):
			self.formatBox.addItem(data[row])

	def __clBut(self):
		self.backButton.clicked.connect(self.close)
		self.listWidget.itemClicked.connect(self.__addDataToProduct)
		self.saveButton.clicked.connect(self.__saveDataProduct)
		self.addListButton.clicked.connect(self.__addItemtolistWindow)
		self.saveListButton.clicked.connect(self.__saveDataToList)
		self.delToListButton.clicked.connect(self.__dropRowToTable)

	def __addItemToList(self, data):
		for row in range(len(data)): 
			self.listWidget.insertItem(row, data[row][1])

	def __addItemtolistWindow(self):
		self.atp = AddToProduct(self)
		self.atp.show()

	def addItemtolist(self, data):
		arrData = [self.idNewProduct, data, None, None]
		self.newItemList.append(arrData)
		self.listWidget.clear()
		self.__addItemToList(self.newItemList)

	def __addDataToProduct(self):
		row = self.listWidget.currentRow()
		self.nameDesForm.setText(str(self.newItemList[row][1]))
		self.descriptionEdit.setText(str(self.newItemList[row][2]))
		self.priceToProdEdit.setText(str(self.newItemList[row][3]))

	def __saveDataToList(self):
		self.ewl = ErrorClass()
		idrow = self.listWidget.currentRow()
		if idrow == -1:
			self.ewl.label.setText("Выберите пункт")
			self.ewl.show()
		else:
			toProductName = self.nameDesForm.text()
			toProductDes = self.descriptionEdit.toPlainText()
			toProductPrice = self.priceToProdEdit.text()
			try:
				int(toProductPrice)
				arrData = [toProductName, toProductDes, toProductPrice]
				for item in range(1, len(self.newItemList[idrow])):
					self.newItemList[idrow][item] = arrData[item-1]
			except:
				self.ewl.label.setText("Цена в цифрах!")
				self.ewl.show()

	def __dropRowToTable(self):
		self.ewdl = ErrorClass()
		idrow = self.listWidget.currentRow()
		if idrow == -1:
			self.ewdl.label.setText("Выберите пункт")
			self.ewdl.show()
		else:
			del self.newItemList[idrow]
			self.listWidget.clear()
			self.__addItemToList(self.newItemList)
			self.mbc = MessBoxClass()
			self.mbc.label.setText("Успешно удалено")
			self.mbc.show()

	def __saveDataProduct(self):
		self.ewls = ErrorClass()
		nameProd = self.nameForm.text()
		priceProd = self.priceProdEdit.text()
		desProd = self.desProdEdit.toPlainText()
		imgProd = self.imgEdit.text()
		formatProg = self.formatBox.currentText()
		try:
			int(priceProd)
			self.newItemProd = [nameProd, desProd, priceProd, imgProd + '.'+ formatProg]
			self.addToDbNewProduct()
			self.addToDbNewToProduct()
			self.tableProd.tableControl()
			self.mbc = MessBoxClass()
			self.mbc.label.setText("Товар добавлен")
			self.close()
			self.mbc.show()
		except:
			self.ewls.label.setText("Цена в цифрах!")
			self.ewls.show()

	def addToDbNewProduct(self):
		db = DATABASE.AddNewProduct()
		db.addProduct(self.newItemProd)

	def addToDbNewToProduct(self):
		db = DATABASE.AddNewProduct()
		for row in range(len(self.newItemList)):
			db.addToProduct(self.newItemList[row])


class AnalWindow():
	"""Окно анализа и статистики"""

	def __init__(self, obj):
		self.obj = obj
		self.__addWorkersToBox()
		self.updateStat()
		self.__clBut()
		self.excel = Excel(obj, self.idWorker)

	def __clBut(self):
		self.obj.updButton.clicked.connect(self.updateStat)
		self.obj.expButton.clicked.connect(self.__expToEX)
		self.obj.expButtonTo1C.clicked.connect(self.__ExpToOneC)
		self.obj.workerBoxAnal.activated.connect(self.setWork)

	def updateStat(self):
		self.setStat()
		self.setWork()

	def setStat(self):
		self.__setSumOrder()
		self.__setSumNewOrder()
		self.__setSumWorkOrder()
		self.__setSumСomplOrder()
		self.__setCostOrder()
		self.__setIncomelOrder()
		self.__setSummOrder()

	def setWork(self):
		db = DATABASE.StatAnalClass()
		name = self.obj.workerBoxAnal.currentText()
		self.idWorker = db.getIdWorker(name)
		self.__setSumWorkTotalOrder(self.idWorker[0][0])
		self.__setSumWorkComplOrder(self.idWorker[0][0])
		self.__setSumWorkIncome(self.idWorker[0][0])
		
	def __setSumOrder(self):
		self.db = DATABASE.StatAnalClass()
		self.obj.com_total.setText(str(self.db.countRowOrders()[0][0]))

	def __setSumNewOrder(self):
		self.obj.com_new.setText(str(self.db.countRowNewOrders()[0][0]))

	def __setSumWorkOrder(self):
		self.obj.com_work.setText(str(self.db.countRowWorkOrders()[0][0]))

	def __setSumСomplOrder(self):
		self.obj.com_completed.setText(str(self.db.countRowСomplOrders()[0][0]))

	def __setCostOrder(self):
		self.cost = self.db.sumCostOrders()[0][0]
		self.obj.com_cost.setText(str(self.cost))

	def __setIncomelOrder(self):
		self.income = self.db.sumIncomeOrders()[0][0]
		self.obj.com_income.setText(str(self.income))

	def __setSummOrder(self):
		self.obj.com_summ.setText(str(self.income - self.cost))

	def __addWorkersToBox(self):
		db = DATABASE.AdminDataTable()
		d = db.getAllWorkers()
		for row in range(len(d)):
			self.obj.workerBoxAnal.addItem(d[row][1])

	def __setSumWorkTotalOrder(self, id):
		self.workTotal = self.db.sumWorkTotalOrders(id)[0][0]
		self.obj.work_total.setText(str(self.workTotal))

	def __setSumWorkComplOrder(self, id):
		self.workcompleted = self.db.getSumWorkComplOrder(id)[0][0]
		self.obj.work_completed.setText(str(self.workcompleted))

	def __setSumWorkIncome(self, id):
		self.workIncom = self.db.getSumWorkIncome(id)[0][0]
		if self.workIncom == None:
			self.workIncom = 0
		self.obj.work_income.setText(str(self.workIncom))

	def __expToEX(self):
		self.excel.createXlsx()

	def __ExpToOneC(self):
		self.inf = MessBox1CClass()
		self.inf.show()

class Excel():

	def __init__(self, obj, idWorker):
		self.obj = obj
		self.idWorker = idWorker

	def createXlsx(self):
		data = str(datetime.datetime.now())
		data = data.replace(':', '-')
		self.data = '../Отчеты/' + data + '.xlsx'
		self.workbook = xlsxwriter.Workbook(self.data)
		self.worksheet = self.workbook.add_worksheet()
		self.__setDataExel()
		self.__showMB()

	def __showMB(self):
		self.mbsn = MessBoxClass()
		self.mbsn.label.setText(f'Экспортирован в папку "Отчеты"\n {self.data}')
		self.mbsn.show()

	def __setDataExel(self):
		db = DATABASE.StatAnalClass()
		data = [
			['Количество заказов всего', 
				'Количество новых заказов', 
				'Количество заказов в работе', 
				'Количество выполненных заказов', 
				'Затраты', 
				'Доход', 
				'Прибыль'],
			[db.countRowOrders()[0][0], 
				db.countRowNewOrders()[0][0], 
				db.countRowWorkOrders()[0][0], 
				db.countRowСomplOrders()[0][0], 
				db.sumCostOrders()[0][0], 
				db.sumIncomeOrders()[0][0], 
				db.sumIncomeOrders()[0][0] - db.sumCostOrders()[0][0]],
			['Работник', 
				'Количество заказов в целом', 
				'Количество выполненных заказов', 
				'Доход работника'],
			[self.obj.workerBoxAnal.currentText(),
				int(self.obj.work_total.text()),
				int(self.obj.work_completed.text()),
				int(self.obj.work_income.text())]
				]

		self.worksheet.write_column('A1', data[0])
		self.worksheet.write_column('B1', data[1])
		self.worksheet.write_column('D1', data[2])
		self.worksheet.write_column('E1', data[3])
		self.worksheet.set_column(0, 0, 35)
		self.worksheet.set_column(1, 1, 15)
		self.worksheet.set_column(3, 3, 35)
		self.worksheet.set_column(4, 5, 15)
		self.workbook.close()