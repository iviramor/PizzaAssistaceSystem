import pymysql
import sys

#    pip install pymysql
#    pip install cryptography

class ConnectToDataBase:
    '''Присоединение к MySQL Server'''

    def __init__(self):
        self.__connect = None
        self.__cursor = None
        self.__arrDataSet = []
        self.__setSetting()
        self.__setConnect()

    def __setSetting(self):
        set = open('../settingDataBase.txt', 'r')
        for line in set:
            self.__arrDataSet.append(line[line.find('<')+1:line.find('>')])
        
    def __setConnect(self):
        try:
            self.__connect = pymysql.connect( 
                host=self.__arrDataSet[0],
                user=self.__arrDataSet[1],
                password=self.__arrDataSet[2], 
                db='basicpas'
                )
            self.__cursor = self.__connect.cursor()
            return True
        except Exception:
            return False

    def testServer(self):
        inquiry = '''SHOW TABLES'''
        self.__cursor.execute(inquiry)
        ansq = self.__cursor.fetchall()
        return ansq

    def giveCursor(self):
        return self.__cursor

    def commit(self):
        self.__connect.commit()


class SingInAdmin(ConnectToDataBase):
    '''Вход в уч. запись администратор'''

    def __init__(self):
        super().__init__()
        self.__cursor = self.giveCursor()
        
    def singInDbSearch(self, arrData):
        inquiry = '''SELECT * FROM admin
                      WHERE users_login = %s 
                        AND users_password = %s'''
        self.__cursor.execute(inquiry, arrData)
        ansq = self.__cursor.fetchall()
        if len(ansq) != 0:
            return ansq
        else:
            return False

class SingUpAdmin(ConnectToDataBase):
    '''Регистрация в уч.запись администратор'''

    def __init__(self):
        super().__init__()
        self.__cursor = self.giveCursor()
        
    def singUpDbAdmin(self, arrData):
        inquiry = '''SELECT * FROM admin
                      WHERE users_login = %s'''
        self.__cursor.execute(inquiry, arrData[1])
        ansq = self.__cursor.fetchall()
        if len(ansq) == 0:
            return self.__sendToDB(arrData)
        else:
            return False

    def __sendToDB(self, arrData):
        inquiry = '''INSERT INTO admin (users_name, users_login, users_password, status_to_system)
                     VALUES (%s, %s, %s, "Администратор")'''
        self.__cursor.execute(inquiry, arrData)
        self.commit()
        return True

class SingInWorker(ConnectToDataBase):
    '''Вход в уч. запись рабочий'''

    def __init__(self):
        super().__init__()
        self.__cursor = self.giveCursor()
        
    def singInDbWorker(self, arrData):
        inquiry = '''SELECT * FROM workers
                      WHERE users_login = %s 
                        AND users_password = %s'''
        self.__cursor.execute(inquiry, arrData)
        ansq = self.__cursor.fetchall()
        if len(ansq) != 0:
            return ansq
        else:
            return False

class SingUpWorker(ConnectToDataBase):
    '''Регистрация в уч.запись рабочий'''

    def __init__(self):
        super().__init__()
        self.__cursor = self.giveCursor()
        
    def singUpDbWorker(self, arrData):
        inquiry = '''SELECT * FROM workers
                      WHERE users_login = %s'''
        self.__cursor.execute(inquiry, arrData[1])
        ansq = self.__cursor.fetchall()
        if len(ansq) == 0:
            return self.__sendToDB(arrData)
        else:
            return False

    def __sendToDB(self, arrData):
        inquiry = '''INSERT INTO workers (users_name, users_login, users_password, status_to_system)
                     VALUES (%s, %s, %s, "Рабочий")'''
        self.__cursor.execute(inquiry, arrData)
        self.commit()
        return True

class SettingDataWorker(ConnectToDataBase):
    '''Настройки рабочего'''

    def __init__(self):
        super().__init__()
        self.__cursor = self.giveCursor()


    def editDataWorker(self, arrData):
        inquiry = '''SELECT * FROM workers
                      WHERE users_login = %s'''
        self.__cursor.execute(inquiry, arrData[2])
        ansq = self.__cursor.fetchall()
        if len(ansq) == 0:
            return self.updDataBase(arrData)
        else:
            return False

    def updDataBase(self, arrData):
        inquiry = '''UPDATE workers
                        SET users_name=%s, users_login=%s, users_password=%s
                      WHERE id = '''+str(arrData[0])
        self.__cursor.execute(inquiry, arrData[1:4])
        self.commit()

class SettingDataWorker(ConnectToDataBase):
    '''Настройки рабочего'''

    def __init__(self):
        super().__init__()
        self.__cursor = self.giveCursor()


    def editDataWorker(self, arrData):
        inquiry = '''SELECT * FROM workers
                      WHERE users_login = %s'''
        self.__cursor.execute(inquiry, arrData[2])
        ansq = self.__cursor.fetchall()
        if len(ansq) == 0:
            return self.updDataBase(arrData)
        else:
            return False

    def updDataBase(self, arrData):
        inquiry = '''UPDATE workers
                        SET users_name=%s, users_login=%s, users_password=%s
                      WHERE id = '''+str(arrData[0])
        self.__cursor.execute(inquiry, arrData[1:4])
        self.commit()

class SettingDataAdmin(ConnectToDataBase):
    '''Настройки рабочего'''

    def __init__(self):
        super().__init__()
        self.__cursor = self.giveCursor()


    def editDataWorker(self, arrData):
        inquiry = '''SELECT * FROM admin
                      WHERE users_login = %s'''
        self.__cursor.execute(inquiry, arrData[2])
        ansq = self.__cursor.fetchall()
        if len(ansq) == 0:
            return self.updDataBase(arrData)
        else:
            return False

    def updDataBase(self, arrData):
        inquiry = '''UPDATE admin
                        SET users_name=%s, users_login=%s, users_password=%s
                      WHERE id = '''+str(arrData[0])
        self.__cursor.execute(inquiry, arrData[1:4])
        self.commit()
     
class WorkerDataTable(ConnectToDataBase):
    '''Таблицы заказов'''

    def __init__(self):
        super().__init__()
        self.__cursor = self.giveCursor()


    def getData(self):
        inquiry = '''SELECT Orders.id, product.name_product, Orders.comment_orders, Orders.quantuty_orders, Status_order.step_status, workers.users_name
	                   FROM Orders
                 INNER JOIN status_order
                         ON Orders.id = status_order.id_order
                 INNER JOIN product
                         ON Orders.id_product_orders = product.id
                  LEFT JOIN workers
                         ON Status_order.worker = workers.id'''

        self.__cursor.execute(inquiry)
        ansq = self.__cursor.fetchall()
        return ansq
        
    def addStatus(self, orderID, worker):
        inquiry = '''SELECT Orders.id, Status_order.step_status
	                   FROM Orders
                       JOIN status_order
                         ON Orders.id = status_order.id_order
					  WHERE step_status = "Новый" and id = '''+str(orderID)
        self.__cursor.execute(inquiry)
        ansq = self.__cursor.fetchall()
        if len(ansq) != 0:
            self.__updateDataTable(0,  str(worker), orderID)
            return True
        else:
            return False

    def completStatus(self, orderID):
        inquiry = '''SELECT Orders.id, Status_order.step_status
	                   FROM Orders
                       JOIN status_order
                         ON Orders.id = status_order.id_order
					  WHERE step_status = "Завершен" and id = '''+str(orderID)
        self.__cursor.execute(inquiry)
        ansq = self.__cursor.fetchall()
        if len(ansq) == 0:
            self.__updateDataTable(1, orderID)
            return True
        else:
            return False

    def __updateDataTable(self, status, *arrData):
        inquiry = '''UPDATE Status_order
                        SET step_status = "В работе", worker = %s
                      WHERE id_order = %s'''
        inquiry2 ='''UPDATE Status_order
                        SET step_status = "Завершен"
                      WHERE id_order = %s'''
        if status == 0:
            self.__cursor.execute(inquiry, arrData)
            self.commit()
        elif status == 1:
            self.__cursor.execute(inquiry2, arrData)
            self.commit()
          
    def getMyOrdersData(self, workerID):
        inquiry = '''SELECT Orders.id, product.name_product, Orders.comment_orders, Orders.quantuty_orders, Status_order.step_status
	                   FROM Orders
                 INNER JOIN status_order
                         ON Orders.id = status_order.id_order
                 INNER JOIN product
                         ON Orders.id_product_orders = product.id
                      WHERE Status_order.worker = '''+str(workerID)
        self.__cursor.execute(inquiry)
        ansq = self.__cursor.fetchall()
        return ansq


class InoWindow(ConnectToDataBase):
    """Вывод информации продукта"""

    def __init__(self):
        super().__init__()
        self.__cursor = self.giveCursor()


    def getInfoProduct(self, orderID):
        inquiry = '''SELECT product.id, product.name_product, product.price_product, Orders.quantuty_orders, Orders.comment_orders
	                   FROM Orders
                 INNER JOIN status_order
                         ON Orders.id = status_order.id_order
                 INNER JOIN product
                         ON Orders.id_product_orders = product.id
					  WHERE Orders.id = ''' + str(orderID)
        self.__cursor.execute(inquiry)
        ansq = self.__cursor.fetchall()
        return ansq

    def getIfoToProduct(self, productID):
        inquiry = '''SELECT to_products.id_product, to_products.name_product, to_products.description_product
	                   FROM product
                 INNER JOIN to_products
                         ON product.id = to_products.id_product
				      WHERE product.id = ''' + str(productID)
        self.__cursor.execute(inquiry)
        ansq = self.__cursor.fetchall()
        return ansq


class AdminDataTable(ConnectToDataBase):
    '''Таблицы админа'''

    def __init__(self):
        super().__init__()
        self.__cursor = self.giveCursor()

    def getAllProduct(self):
        inquiry = '''SELECT * FROM product'''
        self.__cursor.execute(inquiry)
        ansq = self.__cursor.fetchall()
        return ansq

    def getData(self):
        inquiry = '''SELECT Orders.id, product.name_product, Orders.comment_orders, Orders.quantuty_orders, Status_order.step_status, workers.users_name
	                   FROM Orders
                 INNER JOIN status_order
                         ON Orders.id = status_order.id_order
                 INNER JOIN product
                         ON Orders.id_product_orders = product.id
                  LEFT JOIN workers
                         ON Status_order.worker = workers.id'''
        self.__cursor.execute(inquiry)
        ansq = self.__cursor.fetchall()
        return ansq

    def getAllWorkers(self):
        inquiry = '''SELECT id, users_name FROM workers'''
        self.__cursor.execute(inquiry)
        ansq = self.__cursor.fetchall()
        return ansq

    def searchDataNew(self, d):
        inquiry = '''SELECT Orders.id, product.name_product, Orders.comment_orders, Orders.quantuty_orders, Status_order.step_status, workers.users_name
	                   FROM Orders
                 INNER JOIN status_order
                         ON Orders.id = status_order.id_order
                 INNER JOIN product
                         ON Orders.id_product_orders = product.id
                  LEFT JOIN workers
                         ON Status_order.worker = workers.id
                      WHERE Status_order.step_status = %s'''
        self.__cursor.execute(inquiry, [d])
        ansq = self.__cursor.fetchall()
        return ansq

    def searchData(self, d):
        inquiry = '''SELECT Orders.id, product.name_product, Orders.comment_orders, Orders.quantuty_orders, Status_order.step_status, workers.users_name
	                   FROM Orders
                 INNER JOIN status_order
                         ON Orders.id = status_order.id_order
                 INNER JOIN product
                         ON Orders.id_product_orders = product.id
                  LEFT JOIN workers
                         ON Status_order.worker = workers.id
                      WHERE Status_order.step_status = %s AND workers.users_name = %s'''
        self.__cursor.execute(inquiry, d)
        ansq = self.__cursor.fetchall()
        return ansq


class InfProductWindow(ConnectToDataBase):
    """Информация окна продуктов"""

    def __init__(self):
        super().__init__()
        self.__cursor = self.giveCursor()


    def getInfoProduct(self, idProduct):
        inquiry = '''SELECT * FROM product
                      WHERE id = '''+str(idProduct)
        self.__cursor.execute(inquiry)
        ansq = self.__cursor.fetchall()
        return ansq

    def getIfoToProduct(self, productID):
        inquiry = '''SELECT to_products.id_product, to_products.name_product, to_products.description_product, to_products.consumption_product
	                   FROM product
                 INNER JOIN to_products
                         ON product.id = to_products.id_product
				      WHERE product.id = ''' + str(productID)
        self.__cursor.execute(inquiry)
        ansq = self.__cursor.fetchall()
        return ansq

class EditProduct(ConnectToDataBase):
    """Редактировать товары"""

    def __init__(self):
        super().__init__()
        self.__cursor = self.giveCursor()


    def getInfoProduct(self, idProduct):
        inquiry = '''SELECT * FROM product
                      WHERE id = '''+str(idProduct)
        self.__cursor.execute(inquiry)
        ansq = self.__cursor.fetchall()
        return ansq

    def getIfoToProduct(self, productID):
        inquiry = '''SELECT to_products.id, to_products.id_product, to_products.name_product, to_products.description_product, to_products.consumption_product
	                   FROM product
                 INNER JOIN to_products
                         ON product.id = to_products.id_product
				      WHERE product.id = ''' + str(productID)
        self.__cursor.execute(inquiry)
        ansq = self.__cursor.fetchall()
        return ansq

    def addToProduct(self, d):
        inquiry = '''INSERT To_products (id_product, name_product) 
                     VALUES (%s, %s)'''
        self.__cursor.execute(inquiry, d)
        self.commit()

    def upDateToProduct(self, d):
        inquiry = '''UPDATE to_products
                        SET name_product = %s, description_product = %s, consumption_product = %s
                      WHERE id = '''+str(d[0])
        self.__cursor.execute(inquiry, d[2:])
        self.commit()

    def dropRowToTable(self, d):
        inquiry = '''DELETE from To_products
                      WHERE id = '''+str(d[0])
        self.__cursor.execute(inquiry)
        self.commit()

    def savedataProduct(self, d):
        inquiry = '''UPDATE Product
                        SET name_product = %s, description_product = %s, price_product = %s, image_product = %s
                      WHERE id = '''+str(d[0])
        self.__cursor.execute(inquiry, d[1:])
        self.commit()

class AddNewProduct(ConnectToDataBase): 
    """Добавление новых товаров"""

    def __init__(self):
        super().__init__()
        self.__cursor = self.giveCursor()

    def countRowProd(self):
        inquiry = '''SELECT MAX(id) FROM product'''
        self.__cursor.execute(inquiry)
        ansq = self.__cursor.fetchall()
        return ansq

    def addProduct(self, d):
        inquiry = '''INSERT Product (name_product, description_product, price_product, image_product) 
                     VALUES (%s, %s, %s, %s)'''
        self.__cursor.execute(inquiry, d)
        self.commit()

    def addToProduct(self, d):
        inquiry = '''INSERT To_products (id_product, name_product, description_product, consumption_product)
                     VALUES (%s, %s, %s, %s)'''
        self.__cursor.execute(inquiry, d)
        self.commit()


class StatAnalClass(ConnectToDataBase):
    """Сбор информации"""

    def __init__(self):
        super().__init__()
        self.__cursor = self.giveCursor()

    def countRowOrders(self):
        inquiry = '''SELECT COUNT(*) FROM orders'''
        self.__cursor.execute(inquiry)
        ansq = self.__cursor.fetchall()
        return ansq
    
    def countRowNewOrders(self):
        inquiry = '''SELECT COUNT(*)
                       FROM status_order
                      WHERE status_order.step_status = "Новый"'''
        self.__cursor.execute(inquiry)
        ansq = self.__cursor.fetchall()
        return ansq

    def countRowWorkOrders(self):
        inquiry = '''SELECT COUNT(*)
                       FROM status_order
                      WHERE status_order.step_status = "В работе"'''
        self.__cursor.execute(inquiry)
        ansq = self.__cursor.fetchall()
        return ansq

    def countRowСomplOrders(self):
        inquiry = '''SELECT COUNT(*)
                       FROM status_order
                      WHERE status_order.step_status = "Завершен"'''
        self.__cursor.execute(inquiry)
        ansq = self.__cursor.fetchall()
        return ansq

    def sumCostOrders(self):
        inquiry = '''SELECT SUM(To_products.consumption_product)
	                   FROM orders
                      INNER JOIN Product
                         ON orders.id_product_orders = Product.id
                      INNER JOIN To_products
                         ON Product.id = To_products.id_product'''
        self.__cursor.execute(inquiry)
        ansq = self.__cursor.fetchall()
        return ansq

    def sumIncomeOrders(self):
        inquiry = '''SELECT SUM(product.price_product)
	                   FROM orders
                      INNER JOIN Product
                         ON orders.id_product_orders = Product.id'''
        self.__cursor.execute(inquiry)
        ansq = self.__cursor.fetchall()
        return ansq

    def getIdWorker(self, worker):
        inquiry = '''SELECT id
                       FROM Workers
                      WHERE Workers.users_name = '''+ '"' + str(worker) + '"'
        self.__cursor.execute(inquiry)
        ansq = self.__cursor.fetchall()
        return ansq

    def sumWorkTotalOrders(self, idWorker):
        inquiry = '''SELECT COUNT(Status_order.worker)
                       FROM Status_order
                      WHERE Status_order.worker = '''+str(idWorker)
        self.__cursor.execute(inquiry)
        ansq = self.__cursor.fetchall()
        return ansq

    def getSumWorkComplOrder(self, idWorker):
        inquiry = '''SELECT COUNT(Status_order.step_status)
                       FROM Status_order
                      WHERE Status_order.step_status = "Завершен" AND Status_order.worker = '''+str(idWorker)
        self.__cursor.execute(inquiry)
        ansq = self.__cursor.fetchall()
        return ansq

    def getSumWorkIncome(self, idWorker):
        inquiry = '''SELECT SUM(Product.price_product)
                       FROM Orders
                 INNER JOIN Status_order
                         On Orders.id = Status_order.id_order
                 INNER JOIN Product
                         ON Orders.id_product_orders = Product.id
                      WHERE Status_order.worker = '''+str(idWorker)
        self.__cursor.execute(inquiry)
        ansq = self.__cursor.fetchall()
        return ansq

if __name__ == "__main__":
    ConnectToDataBase()
    