import sys
import sys

from win11toast import notify

from configure__main import Configuration, Applicator
from applicate_dialogs import AppConfigurator, EnumerateApps

from ui_gui import *

from PySide6.QtGui import QAction, QIcon, QPixmap
from PySide6.QtWidgets import QSystemTrayIcon, QMenu
from PySide6.QtCore import Qt
NoBrush = Qt.NoBrush

notificate = ["Miko!! Notificate", "Please reopen main app for the changes to take effect"]

class Application:
    def __init__(self):
        self.app = QApplication(sys.argv + ['-platform', 'windows:darkmode=0'])
        self.app.setStyle('Fusion')

        icon        = QIcon("ui/icon.png")
        self.window = MainWindow(Configuration, icon)
        self.tray   = Tray(self.window, icon)

        self.window.show()
        self.app.exec()

class MainWindow(QMainWindow):
    def __init__(self, configuration: Configuration, icon=None):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("Miko!!")
        self.setWindowIcon(icon)
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.dia = notify

        self.config = configuration

        self.pixmap = QPixmap.fromImage(QImage("ui/white.jpg"))

        self.ui.comboBoxType.activated.connect(self._get_comboBoxType_choice)
        self.ui.comboBoxVoice.activated.connect(self._get_comboBoxVoice_choice)
        self.ui.langModels.activated.connect(self._get_langMobels_choice)

        self.ui.comboBoxVoice.addItem("None") # List active weights models
        self.ui.comboBoxVoice.addItems(self.config._CONFIG()['settings']['models'])

        self.ui.langModels.addItem("None")
        self.ui.langModels.addItems(self.config._CONFIG()['settings']['lang_models'])

        self.ui.closeButton.clicked.connect(self.closeFROMTRAY)
        self.ui.hideButton.clicked.connect(self.hideNormal)
        self.ui.stopButton.clicked.connect(self.pause)
        self.ui.updateModelButton.clicked.connect(self._update_model_list_)
        self.ui.checkAppButton.clicked.connect(self.enumerating)
        self.ui.reloadAppButton.clicked.connect(self.appUpdate)
        self.ui.appConfigureButton.clicked.connect(self.configurating)

        self.ui.stopStatus.setText(f"Pause is: {self.config._PAUSE()}")

        self.ui.speedSlider.setMinimum(0)
        self.ui.speedSlider.setMaximum(12)
        self.ui.speedSlider.setSingleStep(1)
        self.ui.speedSlider.valueChanged.connect(self.speedChanged)

        self.ui.protectSlider.setMinimum(0)
        self.ui.protectSlider.setMaximum(100)
        self.ui.protectSlider.setSingleStep(10)
        self.ui.protectSlider.valueChanged.connect(self.protectChanged)

        self.ui.tempSlider.setMinimum(-12)
        self.ui.tempSlider.setMaximum(12)
        self.ui.tempSlider.setSingleStep(1)
        self.ui.tempSlider.valueChanged.connect(self.tempChanged)

        self.ui.speedSlider.setValue(self.config._CONFIG()['settings']['voice']['speed'])
        self.ui.protectSlider.setValue(int(self.config._CONFIG()['settings']['voice']['protect0']*100))
        self.ui.tempSlider.setValue(self.config._CONFIG()['settings']['voice']['f0_key_up'])

        self.ui.speedCount.setText(str(self.config._CONFIG()['settings']['voice']['speed']))
        self.ui.protectCount.setText(str(self.config._CONFIG()['settings']['voice']['protect0']))
        self.ui.tempCount.setText(str(self.config._CONFIG()['settings']['voice']['f0_key_up']))

        self.__updater()
        self.__appUpdater()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)

        qp.setBrush(NoBrush)
        qp.drawPixmap(0, 0, self.pixmap)

        qp.end()

    def showNormal(self): self.show()
    def hideNormal(self): self.hide()

    def closeEvent(self, event):
        self.hide()
        event.ignore() 
    def closeFROMTRAY(self):
        self.config.stop()
        Applicator._checkSave()
        self.close()

    def pause(self):
        self.config.pause()
        self.ui.stopStatus.setText(f"Pause is: {self.config._PAUSE()}")

    def __appUpdater(self):
        countAll = Applicator.getAppsCount()
        countReady = Applicator.getReadyAppsCount()
        countData = Applicator.getNeedDataAppsCount()
        countConfirm = Applicator.getNeedAcceptAppsCount()
        self.ui.appCount.setText(
            f"⚫️App found - {countAll}\n"\
            f"🟢Ready to use - {countReady}\n"\
            f"🔴Need enter path - {countData}"
            )
        self.ui.appConfirmCount.setText(f"🟡Need confirmation - {countConfirm} apps")
        self.ui.checkAppButton.setText(f"Check app configuration ({countConfirm})")

    def __updater(self):
        if self.config._CONFIG()['settings']['voiceActive']:
            self.ui.typeLabel.setText('Model is active')
            self.ui.modelLabel.setText(
                self.config._CONFIG()['settings']['models'][self.config._ACTIVE()])
            
            self.ui.comboBoxType.setCurrentIndex(1)
            self.ui.comboBoxVoice.setCurrentIndex(self.config._ACTIVE()+1)
            self.ui.langModels.setCurrentIndex(
                self.config._CONFIG()['settings']['lang_models'].index(
                self.config._CONFIG()['settings']['voice']['tts'])+1
                )

        else:
            self.ui.typeLabel.setText('Model is not active')
            self.ui.modelLabel.setText('Model is not active')

            self.ui.comboBoxType.setCurrentIndex(0)
            self.ui.comboBoxVoice.setCurrentIndex(0)
            self.ui.langModels.setCurrentIndex(0)

    def _update_model_list_(self):
        self.ui.comboBoxVoice.clear()
        self.ui.comboBoxVoice.addItem('None')
        self.ui.comboBoxVoice.addItems(self.config._CONFIG()['settings']['models'])
        if self.config._CONFIG()['settings']['voiceActive']:
            self.ui.comboBoxVoice.setCurrentIndex(
                self.config._ACTIVE()+1)
        else: self.ui.comboBoxVoice.setCurrentIndex(0)

    def _get_comboBoxVoice_choice(self):
        active = self.ui.comboBoxVoice.currentText()
        if active != "None":
            self.config.update_voice(active)
            if not self.config._CONFIG()['settings']['voiceActive']:
                self.config.reverse_active()
            self.config.loaderON()
        else:
            if self.config._CONFIG()['settings']['voiceActive']:
                self.config.reverse_active()
            self.dia(notificate[0], notificate[1])
        self.__updater()

    def _get_comboBoxType_choice(self):
        active = self.ui.comboBoxType.currentText()
        if "Prime" in active.split()[0]:
            if not self.config._CONFIG()['settings']['voiceActive']:
                self.config.reverse_active()
        else:
            if self.config._CONFIG()['settings']['voiceActive']:
                self.config.reverse_active()
            self.dia(notificate[0], notificate[1])
        self.__updater()

    def _get_langMobels_choice(self):
        active = self.ui.langModels.currentText()
        if active not in self.config._CONFIG()['settings']['lang_models']:
            if self.config._CONFIG()['settings']['voiceActive']:
                self.config.reverse_active()
            self.dia(notificate[0], notificate[1])
        else:
            index = self.config._CONFIG()['settings']['lang_models'].index(active)
            self.config.update_tts(index)
        self.__updater()

    def speedChanged(self, value):
        self.config.change_speed(value)
        self.ui.speedSlider.setValue(
            self.config._CONFIG()['settings']['voice']['speed'])
        self.ui.speedCount.setText(
            str(self.config._CONFIG()['settings']['voice']['speed']))

    def protectChanged(self, value):
        self.config.change_protect0(value/100)
        self.ui.protectSlider.setValue(
            int(self.config._CONFIG()['settings']['voice']['protect0']*100))
        self.ui.protectCount.setText(
            str(self.config._CONFIG()['settings']['voice']['protect0']))

    def tempChanged(self, value):
        self.config.change_f0_key_up(value)
        self.ui.tempSlider.setValue(
            self.config._CONFIG()['settings']['voice']['f0_key_up'])
        self.ui.tempCount.setText(
            str(self.config._CONFIG()['settings']['voice']['f0_key_up']))

    def enumerating(self):
        self.newWindow = EnumerateApps(self.__appUpdater)
        self.newWindow.show()

    def configurating(self):
        self.confWindow = AppConfigurator(self.__appUpdater)
        self.confWindow.show()

    def appUpdate(self):
        Applicator.reloadAppList()
        self.__appUpdater()


class Tray(QSystemTrayIcon):
    def __init__(self, window, icon=None) -> None:
        QSystemTrayIcon.__init__(self)
        self.setIcon(icon)
        self.setVisible(True)

        self.window = window

        self.showB = QAction("Show")
        self.hideB = QAction("Hide")
        self.stopB = QAction("Pause <> Continue")
        self.quitB = QAction("Quit")

        self.showB.triggered.connect(window.showNormal)
        self.hideB.triggered.connect(window.hideNormal)
        self.stopB.triggered.connect(self.pause)
        self.quitB.triggered.connect(window.closeFROMTRAY)

        self.mainMenu = Menu("Miko!!")

        self.mainMenu.newSection("Miko!! GUI")
        self.mainMenu.newSeparator()
        self.mainMenu.newAction(self.showB)
        self.mainMenu.newAction(self.hideB)
        self.mainMenu.newAction(self.stopB)
        self.mainMenu.newSeparator()
        self.mainMenu.newAction(self.quitB)

        self.setContextMenu(self.mainMenu)

    def pause(self):
        self.window.pause()
        self.stopB.setText(str(self.window.config._PAUSE()))

class Menu(QMenu):
    def __init__(self, title: str) -> None:
        QMenu.__init__(self)
        self.setTitle(title)
        
    def newAction(self, action):        self.addAction(action)
    def newDefaultAction(self, action): self.setDefaultAction(action)
    def newSeparator(self):             self.addSeparator()
    def newSection(self, text):         self.addSection(text)
    def newMenu(self, menu):            self.addMenu(menu)