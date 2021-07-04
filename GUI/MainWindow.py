import sys
import json
from typing import Text
sys.path.append('..')
from PyQt5.QtWidgets import QLineEdit, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QComboBox, QListWidget, QAbstractItemView
from PyQt5.QtCore import QTimer, QThreadPool
from PyQt5.QtGui import QIntValidator
from .Worker import Worker
from .MiniTerminal import MiniTerminal
from .Settings import Settings
from .SettingWebsite import SettingWebsite
from WebCrawler.Crawler import Crawler
from WebCrawler.ElementFind import ElementFind

class MainWindow(QMainWindow):

    SETTINGS_FILE = "Settings.json"
    MIN_REFRESH_RATE = 60000   # milli-seconds

    Started1 = False
    Started2 = False
    Started3 = False
    Started4 = False

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.Crawler1 = Crawler()
        self.Crawler2 = Crawler()
        self.Crawler3 = Crawler()
        self.Crawler4 = Crawler()

        self.threadpool = QThreadPool()

        # Keep the window in the memory. Otherwise it's garbage collected.
        self.window = QWidget()
        self.window.resize(1400, 400)
        self.window.move(50, 50)
        self.window.setWindowTitle('Scalperminator')

        mainLayout = QVBoxLayout()

        # Refresh rate
        refreshTimeLabel = QLabel("Refresh time in seconds:")
        mainLayout.addWidget(refreshTimeLabel)
        self.RefreshTime = QLineEdit()
        self.IntValidator = QIntValidator()
        self.RefreshTime.setValidator(self.IntValidator)
        self.RefreshTime.setText("60")
        mainLayout.addWidget(self.RefreshTime)

        # Horizontal separator
        hLine1 = QFrame()
        hLine1.setFrameShape(QFrame.HLine)
        hLine1.setFrameShadow(QFrame.Sunken)
        mainLayout.addWidget(hLine1)
        #mainLayout.addStretch()

        # Layout for websites
        websitesLayout = QHBoxLayout()

        # Website 1
        layout1 = QVBoxLayout()
        url1Label = QLabel("URL")
        layout1.addWidget(url1Label)
        self.Url1 = QLineEdit()
        # self.Url1.setText("https://www.manor.ch/fr/p/10000583778") # DEBUG
        layout1.addWidget(self.Url1)
        targetElement1Label = QLabel("Target Element")
        layout1.addWidget(targetElement1Label)
        self.TargetElement1 = QLineEdit()
        # self.TargetElement1.setText("js-scroll-to-accordion") # DEBUG
        layout1.addWidget(self.TargetElement1)
        targetValue1Label = QLabel("Target Value")
        layout1.addWidget(targetValue1Label)
        self.TargetValue1 = QLineEdit()
        # self.TargetValue1.setText("Indisponible en ligne") # DEBUG
        layout1.addWidget(self.TargetValue1)
        self.TargetType1 = QComboBox()
        self.TargetType1.addItems([e.name for e in ElementFind])
        layout1.addWidget(self.TargetType1)
        self.Start1Button = QPushButton("Start monitor")
        self.Start1Button.clicked.connect(self.StartMonitor1)
        layout1.addWidget(self.Start1Button)
        self.Timer1 = QTimer()
        self.Timer1.timeout.connect(self.Crawl1)
        self.Result1Label = QLabel("Not started")
        layout1.addWidget(self.Result1Label)
        self.terminal1 = MiniTerminal(10)
        layout1.addWidget(self.terminal1)

        layout1.addStretch()
        websitesLayout.addLayout(layout1)

        vLine1 = QFrame()
        vLine1.setFrameShape(QFrame.VLine)
        vLine1.setFrameShadow(QFrame.Sunken)
        websitesLayout.addWidget(vLine1)

        # Website 2
        layout2 = QVBoxLayout()
        url2Label = QLabel("URL")
        layout2.addWidget(url2Label)
        self.Url2 = QLineEdit()
        # self.Url2.setText("https://www.fr.fnac.ch/Console-Sony-PS5-Edition-Standard/a14119956") # DEBUG
        layout2.addWidget(self.Url2)
        targetElement2Label = QLabel("Target Element")
        layout2.addWidget(targetElement2Label)
        self.TargetElement2 = QLineEdit()
        # self.TargetElement2.setText("f-buyBox-availabilityStatus-unavailable") # DEBUG
        layout2.addWidget(self.TargetElement2)
        targetValue2Label = QLabel("Target Value")
        layout2.addWidget(targetValue2Label)
        self.TargetValue2 = QLineEdit()
        # self.TargetValue2.setText("Indisponible en ligne") # DEBUG
        layout2.addWidget(self.TargetValue2)
        self.TargetType2 = QComboBox()
        self.TargetType2.addItems([e.name for e in ElementFind])
        layout2.addWidget(self.TargetType2)
        self.Start2Button = QPushButton("Start monitor")
        self.Start2Button.clicked.connect(self.StartMonitor2)
        layout2.addWidget(self.Start2Button)
        self.Timer2 = QTimer()
        self.Timer2.timeout.connect(self.Crawl2)
        self.Result2Label = QLabel("Not started")
        layout2.addWidget(self.Result2Label)
        self.terminal2 = MiniTerminal(10)
        layout2.addWidget(self.terminal2)
        
        layout2.addStretch()
        websitesLayout.addLayout(layout2)

        vLine2 = QFrame()
        vLine2.setFrameShape(QFrame.VLine)
        vLine2.setFrameShadow(QFrame.Sunken)
        websitesLayout.addWidget(vLine2)

        # Website 3
        layout3 = QVBoxLayout()
        url3Label = QLabel("URL")
        layout3.addWidget(url3Label)
        self.Url3 = QLineEdit()
        # self.Url3.setText("https://www.digitec.ch/en/s1/product/sony-playstation-5-de-fr-it-en-game-consoles-12664145") # DEBUG
        layout3.addWidget(self.Url3)
        targetElement3Label = QLabel("Target Element")
        layout3.addWidget(targetElement3Label)
        self.TargetElement3 = QLineEdit()
        # self.TargetElement3.setText("extended_availability_availabilityText__1Mb57") # DEBUG
        layout3.addWidget(self.TargetElement3)
        targetValue3Label = QLabel("Target Value")
        layout3.addWidget(targetValue3Label)
        self.TargetValue3 = QLineEdit()
        # self.TargetValue3.setText("Currently out of stock and no delivery date available.") # DEBUG
        layout3.addWidget(self.TargetValue3)
        self.TargetType3 = QComboBox()
        self.TargetType3.addItems([e.name for e in ElementFind])
        layout3.addWidget(self.TargetType3)
        self.Start3Button = QPushButton("Start monitor")
        self.Start3Button.clicked.connect(self.StartMonitor3)
        layout3.addWidget(self.Start3Button)
        self.Timer3 = QTimer()
        self.Timer3.timeout.connect(self.Crawl3)
        self.Result3Label = QLabel("Not started")
        layout3.addWidget(self.Result3Label)
        self.terminal3 = MiniTerminal(10)
        layout3.addWidget(self.terminal3)
        
        layout3.addStretch()
        websitesLayout.addLayout(layout3)

        vLine3 = QFrame()
        vLine3.setFrameShape(QFrame.VLine)
        vLine3.setFrameShadow(QFrame.Sunken)
        websitesLayout.addWidget(vLine3)

        # Website 4
        layout4 = QVBoxLayout()
        url4Label = QLabel("URL")
        layout4.addWidget(url4Label)
        self.Url4 = QLineEdit()
        # self.Url4.setText("https://www.mediamarkt.ch/fr/product/_sony-ps-playstation-5-2018096.html") # DEBUG - https://www.mediamarkt.ch/fr/shop/ps5.html
        layout4.addWidget(self.Url4)
        targetElement4Label = QLabel("Target Element")
        layout4.addWidget(targetElement4Label)
        self.TargetElement4 = QLineEdit()
        # self.TargetElement4.setText("offline-text") # DEBUG - /html/body/div[@id='content']/div[1]/div[4]/div[1]/div[1]
        layout4.addWidget(self.TargetElement4)
        targetValue4Label = QLabel("Target Value")
        layout4.addWidget(targetValue4Label)
        self.TargetValue4 = QLineEdit()
        # self.TargetValue4.setText("ARTICLE TEMPORAIREMENT PAS EN STOCK") # DEBUG - La PlayStation 5 est actuellement en rupture de stock.\nInscris-toi sans tarder pour savoir quand la console pourra à nouveau être commandée.
        layout4.addWidget(self.TargetValue4)
        self.TargetType4 = QComboBox()
        self.TargetType4.addItems([e.name for e in ElementFind])
        layout4.addWidget(self.TargetType4)
        self.Start4Button = QPushButton("Start monitor")
        self.Start4Button.clicked.connect(self.StartMonitor4)
        layout4.addWidget(self.Start4Button)
        self.Timer4 = QTimer()
        self.Timer4.timeout.connect(self.Crawl4)
        self.Result4Label = QLabel("Not started")
        layout4.addWidget(self.Result4Label)
        self.terminal4 = MiniTerminal(10)
        layout4.addWidget(self.terminal4)
        
        layout4.addStretch()
        websitesLayout.addLayout(layout4)

        mainLayout.addLayout(websitesLayout)

        # Horizontal separator
        hLine2 = QFrame()
        hLine2.setFrameShape(QFrame.HLine)
        hLine2.setFrameShadow(QFrame.Sunken)
        mainLayout.addWidget(hLine2)

        self.SaveButton = QPushButton("Save")
        self.SaveButton.clicked.connect(self.Save)
        mainLayout.addWidget(self.SaveButton)

        self.mainTerminal = MiniTerminal(5)
        self.mainTerminal.AddLine("All elements of window started")
        mainLayout.addWidget(self.mainTerminal)

        self.Load()

        self.window.setLayout(mainLayout)
        self.window.show()

    # --------- 1 ---------
    def StartMonitor1(self):
        if self.Started1:
            self.terminal1.AddLineWithTimestamp("Stopping monitoring of website 1")
            self.Timer1.stop()
            self.Start1Button.setText("Start monitor")
            self.Started1 = False
        else:
            self.terminal1.AddLineWithTimestamp("Starting monitoring of website 1")
            refresh = int(self.RefreshTime.text()) * 1000
            if refresh < self.MIN_REFRESH_RATE:
                refresh = self.MIN_REFRESH_RATE
            self.Timer1.start(refresh)
            self.Start1Button.setText("Stop monitor")
            self.Started1 = True

    def Crawl1(self):
        if self.Crawler1.Running:
            self.terminal1.AddLineWithTimestamp("Crawler 1 still busy. Skipping check.")
        else:
            self.terminal1.AddLineWithTimestamp("Crawler 1 starting.")
            self.Crawler1.Configure(self.Url1.text(), self.TargetElement1.text(), self.TargetValue1.text(), self.TargetType1.currentText())
            worker = Worker(self.Crawler1.Run)
            worker.signals.result.connect(self.Crawler1ProcessResult)
            self.threadpool.start(worker)

    def Crawler1ProcessResult(self, result):
        if result.Found:
            self.Result1Label.setText(result.Message)
            self.terminal1.AddLineWithTimestamp("Found !")
        elif not result.Message:
            self.Result1Label.setText("Not available.")
            self.terminal1.AddLineWithTimestamp("Not found")
        else:
            self.Result1Label.setText(result.Message)
            self.terminal1.AddLineWithTimestamp("Not found: " + result.Message)

    # --------- 2 ---------
    def StartMonitor2(self):
        if self.Started2:
            self.terminal2.AddLineWithTimestamp("Stopping monitoring of website 2")
            self.Timer2.stop()
            self.Start2Button.setText("Start monitor")
            self.Started2 = False
        else:
            self.terminal2.AddLineWithTimestamp("Starting monitoring of website 2")
            refresh = int(self.RefreshTime.text()) * 1000
            if refresh < self.MIN_REFRESH_RATE:
                refresh = self.MIN_REFRESH_RATE
            self.Timer2.start(refresh)
            self.Start2Button.setText("Stop monitor")
            self.Started2 = True

    def Crawl2(self):
        if self.Crawler2.Running:
            self.terminal2.AddLineWithTimestamp("Crawler 2 still busy. Skipping check.")
        else:
            self.terminal2.AddLineWithTimestamp("Crawler 2 starting.")
            self.Crawler2.Configure(self.Url2.text(), self.TargetElement2.text(), self.TargetValue2.text(), self.TargetType2.currentText())
            worker = Worker(self.Crawler2.Run)
            worker.signals.result.connect(self.Crawler2ProcessResult)
            self.threadpool.start(worker)

    def Crawler2ProcessResult(self, result):
        if result.Found:
            self.Result2Label.setText(result.Message)
            self.terminal2.AddLineWithTimestamp("Found !")
        elif not result.Message:
            self.Result2Label.setText("Not available.")
            self.terminal2.AddLineWithTimestamp("Not found")
        else:
            self.Result2Label.setText(result.Message)
            self.terminal2.AddLineWithTimestamp("Not found: " + result.Message)

    # --------- 3 ---------
    def StartMonitor3(self):
        if self.Started3:
            self.terminal3.AddLineWithTimestamp("Stopping monitoring of website 3")
            self.Timer3.stop()
            self.Start3Button.setText("Start monitor")
            self.Started3 = False
        else:
            self.terminal3.AddLineWithTimestamp("Starting monitoring of website 3")
            refresh = int(self.RefreshTime.text()) * 1000
            if refresh < self.MIN_REFRESH_RATE:
                refresh = self.MIN_REFRESH_RATE
            self.Timer3.start(refresh)
            self.Start3Button.setText("Stop monitor")
            self.Started3 = True

    def Crawl3(self):
        if self.Crawler3.Running:
            self.terminal3.AddLineWithTimestamp("Crawler 3 still busy. Skipping check.")
        else:
            self.terminal3.AddLineWithTimestamp("Crawler 3 starting.")
            self.Crawler3.Configure(self.Url3.text(), self.TargetElement3.text(), self.TargetValue3.text(), self.TargetType3.currentText())
            worker = Worker(self.Crawler3.Run)
            worker.signals.result.connect(self.Crawler3ProcessResult)
            self.threadpool.start(worker)

    def Crawler3ProcessResult(self, result):
        if result.Found:
            self.Result3Label.setText(result.Message)
            self.terminal3.AddLineWithTimestamp("Found !")
        elif not result.Message:
            self.Result3Label.setText("Not available.")
            self.terminal3.AddLineWithTimestamp("Not found")
        else:
            self.Result3Label.setText(result.Message)
            self.terminal3.AddLineWithTimestamp("Not found: " + result.Message)

            
    # --------- 4 ---------
    def StartMonitor4(self):
        if self.Started4:
            self.terminal4.AddLineWithTimestamp("Stopping monitoring of website 4")
            self.Timer4.stop()
            self.Start4Button.setText("Start monitor")
            self.Started4 = False
        else:
            self.terminal4.AddLineWithTimestamp("Starting monitoring of website 4")
            refresh = int(self.RefreshTime.text()) * 1000
            if refresh < self.MIN_REFRESH_RATE:
                refresh = self.MIN_REFRESH_RATE
            self.Timer4.start(refresh)
            self.Start4Button.setText("Stop monitor")
            self.Started4 = True

    def Crawl4(self):
        if self.Crawler4.Running:
            self.terminal4.AddLineWithTimestamp("Crawler 4 still busy. Skipping check.")
        else:
            self.terminal4.AddLineWithTimestamp("Crawler 4 starting.")
            self.Crawler4.Configure(self.Url4.text(), self.TargetElement4.text(), self.TargetValue4.text(), self.TargetType4.currentText())
            worker = Worker(self.Crawler4.Run)
            worker.signals.result.connect(self.Crawler4ProcessResult)
            self.threadpool.start(worker)

    def Crawler4ProcessResult(self, result):
        if result.Found:
            self.Result4Label.setText(result.Message)
            self.terminal4.AddLineWithTimestamp("Found !")
        elif not result.Message:
            self.Result4Label.setText("Not available.")
            self.terminal4.AddLineWithTimestamp("Not found")
        else:
            self.Result4Label.setText(result.Message)
            self.terminal4.AddLineWithTimestamp("Not found: " + result.Message)

            
    # --------- Save / Load ---------
    def Save(self):
        settingWebsite = []
        settingWebsite.append( SettingWebsite(self.Url1.text(), self.TargetElement1.text(), self.TargetValue1.text(), self.TargetType1.currentText()))
        settingWebsite.append( SettingWebsite(self.Url2.text(), self.TargetElement2.text(), self.TargetValue2.text(), self.TargetType2.currentText()))
        settingWebsite.append( SettingWebsite(self.Url3.text(), self.TargetElement3.text(), self.TargetValue3.text(), self.TargetType3.currentText()))
        settingWebsite.append( SettingWebsite(self.Url4.text(), self.TargetElement4.text(), self.TargetValue4.text(), self.TargetType4.currentText()))
        settings = Settings(self.RefreshTime.text(), settingWebsite)

        file = open(self.SETTINGS_FILE, "w")
        jsonData = json.dumps(settings, default=lambda o: o.__dict__, indent=2)
        file.write(jsonData)
        file.close()

        self.mainTerminal.AddLine("Settings saved in : " + self.SETTINGS_FILE)

    def Load(self):
        try:
            file = open(self.SETTINGS_FILE, "r")
            jsonData = file.read()
            settings = Settings(**json.loads(jsonData))

            self.RefreshTime.setText(settings.RefreshTime)

            self.Url1.setText(settings.SettingWebsites[0]["Url"])
            self.TargetElement1.setText(settings.SettingWebsites[0]["Element"])
            self.TargetValue1.setText(settings.SettingWebsites[0]["ElementValue"])
            self.TargetType1.setCurrentText(settings.SettingWebsites[0]["ElementType"])
            
            self.Url2.setText(settings.SettingWebsites[1]["Url"])
            self.TargetElement2.setText(settings.SettingWebsites[1]["Element"])
            self.TargetValue2.setText(settings.SettingWebsites[1]["ElementValue"])
            self.TargetType2.setCurrentText(settings.SettingWebsites[1]["ElementType"])
            
            self.Url3.setText(settings.SettingWebsites[2]["Url"])
            self.TargetElement3.setText(settings.SettingWebsites[2]["Element"])
            self.TargetValue3.setText(settings.SettingWebsites[2]["ElementValue"])
            self.TargetType3.setCurrentText(settings.SettingWebsites[2]["ElementType"])
            
            self.Url4.setText(settings.SettingWebsites[3]["Url"])
            self.TargetElement4.setText(settings.SettingWebsites[3]["Element"])
            self.TargetValue4.setText(settings.SettingWebsites[3]["ElementValue"])
            self.TargetType4.setCurrentText(settings.SettingWebsites[3]["ElementType"])

            self.mainTerminal.AddLine("Settings loaded.")
        except:
            self.mainTerminal.AddLine("No setting file. Loading default values")