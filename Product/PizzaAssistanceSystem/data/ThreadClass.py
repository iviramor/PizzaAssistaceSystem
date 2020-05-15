from PyQt5.QtCore import *
import sys


class ProgressThread(QThread):
    """Процессы"""

    def __init__(self, parent=None):
        super().__init__()

    def getMethods(self, *arr):
        self.arrMeth = arr

    def run(self):
        for i in range(len(self.arrMeth)):
            self.arrMeth[i]()