from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import QDateTime
import numpy as np

class MiniTerminal(QLabel):
    """Small terminal to include in a window. Use a circular buffer to store the lines"""

    def __init__(self, nbLines=5):
        QLabel.__init__(self)
        self.numberOfLines = nbLines
        self.lines = np.empty(self.numberOfLines, dtype='U100')    # Array of 100 unicode characters per line
        self.lineIndex = 0   # Store the position of the circular buffer
        self.UpdateText()

    def AddLine(self, newLine):
        self.lines[self.lineIndex] = newLine
        self.lineIndex += 1
        if self.lineIndex >= self.numberOfLines:
            self.lineIndex = 0

        self.UpdateText()

    def AddLineWithTimestamp(self, newLine):
        self.AddLine(QDateTime.currentDateTime().toString() + ": " + newLine)

    def UpdateText(self):
        displayText = ""
        index = self.lineIndex
        for i in range(self.numberOfLines):
            displayText += self.lines[index]
            if i < self.numberOfLines - 1:
                displayText += "\r\n"
            
            index += 1
            if index >= self.numberOfLines:
                index = 0

        self.setText(displayText)
