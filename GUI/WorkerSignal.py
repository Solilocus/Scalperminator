import traceback, sys
from PyQt5.QtCore import QObject, pyqtSignal

class WorkerSignal(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)