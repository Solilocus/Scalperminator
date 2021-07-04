import sys
from PyQt5.QtWidgets import QApplication
from GUI.MainWindow import MainWindow

app = QApplication(sys.argv)

window = MainWindow()

sys.exit(app.exec_())