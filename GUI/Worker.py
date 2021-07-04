import traceback, sys
from PyQt5.QtCore import QRunnable, pyqtSlot
from .WorkerSignal import WorkerSignal

class Worker(QRunnable):
    """Used to start a thread and run a function in it. Pass it to the QT threadpool."""
    def __init__(self, function, *args, **kwargs):
        super(Worker, self).__init__()
        """Define the function that will be run with it's arguments."""
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignal()

    @pyqtSlot()
    def run(self):
        
        try:
            result = self.function(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)
        finally:
            self.signals.finished.emit()