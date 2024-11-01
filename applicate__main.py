import sys

from configure_localization import Localization
from configure__main import Configuration, Applicator
from applicate_dialogs import AppConfigurator, NotifyDialog

from ui_gui import *

from PySide6.QtGui import QAction, QMouseEvent, QPixmap
from PySide6.QtWidgets import QSystemTrayIcon, QMenu
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

class Application:
    def __init__(self):
        self.app = QApplication(sys.argv + ['-platform', 'windows:darkmode=0'])
        self.app.setStyle('Fusion')

        self.window = MainWindow()
        self.tray   = Tray(self.window)

        self.window.show()
        self.app.exec()

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.dia = NotifyDialog()
        self.dia.setText(key="voiceWarn")

        self.setWindowTitle("Miko!!")
        self.setWindowIcon(QIcon("ui/icon.png"))
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.oldpos = None

        self.pixmap = QPixmap.fromImage(QImage("ui/white.jpg"))

        self.loadLang()

        self.ui.comboBoxType.activated.connect(self._get_comboBoxType_choice)
        self.ui.comboBoxLang.activated.connect(self._changeLang)
        self.ui.comboBoxVoice.activated.connect(self._get_comboBoxVoice_choice)
        self.ui.langModels.activated.connect(self._get_langMobels_choice)

        self.ui.comboBoxVoice.addItem("None") # List active weights models
        self.ui.comboBoxVoice.addItems(Configuration._CONFIG()['settings']['models'])

        self.ui.langModels.addItem("None")
        self.ui.langModels.addItems(Configuration._CONFIG()['settings']['lang_models'])

        self.ui.closeButton.clicked.connect(self.closeFROMTRAY)
        self.ui.hideButton.clicked.connect(self.hideNormal)
        self.ui.stopButton.clicked.connect(self.pause)
        self.ui.updateModelButton.clicked.connect(self._update_model_list_)
        self.ui.checkAppButton.clicked.connect(self.enumerating)
        self.ui.reloadAppButton.clicked.connect(self.appUpdate)
        self.ui.appConfigureButton.clicked.connect(self.configurating)

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

        self.ui.speedSlider.setValue(Configuration._CONFIG()['settings']['voice']['speed'])
        self.ui.protectSlider.setValue(int(Configuration._CONFIG()['settings']['voice']['protect0']*100))
        self.ui.tempSlider.setValue(Configuration._CONFIG()['settings']['voice']['f0_key_up'])

        self.ui.speedCount.setText(str(Configuration._CONFIG()['settings']['voice']['speed']))
        self.ui.protectCount.setText(str(Configuration._CONFIG()['settings']['voice']['protect0']))
        self.ui.tempCount.setText(str(Configuration._CONFIG()['settings']['voice']['f0_key_up']))

        self.__updater()
        self.__appUpdater()

    def showNormal(self): self.show()
    def hideNormal(self): self.hide()
    def closeFROMTRAY(self):
        Configuration.stop()
        Applicator._checkSave()
        self.close()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self.oldpos = event.globalPos()
    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self.oldpos is not None:
            diff = event.globalPos() - self.oldpos
            self.move(self.pos() + diff)
            self.oldpos = event.globalPos()
    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self.oldpos = None

    def closeEvent(self, event):
        self.hide()
        event.ignore() 

    def paintEvent(self, event):
        qpainter = QPainter()
        qpainter.begin(self)

        qpainter.setBrush(Qt.NoBrush)
        qpainter.drawPixmap(0, 0, self.pixmap)

        qpainter.end()

    def pause(self):
        Configuration.pause()
        self.loadLang()

    def __appUpdater(self):
        countAll = Applicator.getAppsCount()
        countReady = Applicator.getReadyAppsCount()
        countData = Applicator.getNeedDataAppsCount()
        countConfirm = Applicator.getNeedAcceptAppsCount()
        text_1 = self.lang_Local[
            'appCountLabel_1'].replace(":BLACK:", '⚫️').replace(":cA:", str(countAll))
        text_2 = self.lang_Local[
            "appCountLabel_2"].replace(":GREEN:", '🟢').replace(":cR:", str(countReady))
        text_3 = self.lang_Local[
            "appCountLabel_3"].replace(":RED:", '🔴').replace(":cD:", str(countData))
        self.ui.appCountLabel.setText(f"{text_1}\n{text_2}\n{text_3}")
        self.ui.appConfirmLabel.setText(f"🟡{self.lang_Local['appConfirmLabel']}{countConfirm}")
        self.ui.checkAppButton.setText(f"{self.lang_Local['checkAppButton']} ({countConfirm})")

    def __updater(self):
        if Configuration._CONFIG()['settings']['voiceActive']:
            self.ui.typeLabel.setText('True')
            self.ui.modelLabel.setText(
                Configuration._CONFIG()['settings']['models'][Configuration._ACTIVE()])
            
            self.ui.comboBoxType.setCurrentIndex(1)
            self.ui.comboBoxVoice.setCurrentIndex(Configuration._ACTIVE()+1)
            self.ui.langModels.setCurrentIndex(
                Configuration._CONFIG()['settings']['lang_models'].index(
                Configuration._CONFIG()['settings']['voice']['tts'])+1
                )
        else:
            self.ui.typeLabel.setText('False')
            self.ui.modelLabel.setText('False')

            self.ui.comboBoxType.setCurrentIndex(0)
            self.ui.comboBoxVoice.setCurrentIndex(0)
            self.ui.langModels.setCurrentIndex(0)

    def loadLang(self):
        self.lang_Local = Localization.get_AppLang()

        self.ui.labelType.setText(self.lang_Local['labelType'])
        self.ui.labelVoice.setText(self.lang_Local['labelVoice'])
        self.ui.labelModel.setText(self.lang_Local['labelModel'])

        self.ui.checkAppButton.setText(self.lang_Local['checkAppButton'])
        self.ui.reloadAppButton.setText(self.lang_Local['reloadAppButton'])
        self.ui.appConfigureButton.setText(self.lang_Local['appConfigureButton'])

        self.ui.stopButton.setText(self.lang_Local['stopButton'])
        self.ui.updateModelButton.setText(self.lang_Local['updateModelButton'])

        self.ui.hideButton.setText(self.lang_Local['hideButton'])
        self.ui.closeButton.setText(self.lang_Local['closeButton'])

        self.ui.ActiveTypeLabel.setText(self.lang_Local['ActiveTypeLabel'])
        self.ui.ActiveVoiceLabel.setText(self.lang_Local['ActiveVoiceLabel'])

        self.ui.stopStatus.setText(f"{self.lang_Local['stopButton']} {Configuration._PAUSE()}")

    def _changeLang(self):
        lang = self.ui.comboBoxLang.currentText()
        index = 0 if lang == "RU" else 2
        if Configuration._CONFIG()['settings']['voiceActive']:
            self.ui.langModels.setCurrentIndex(index)
        Localization.changeLang(lang)
        self.loadLang()

    def _update_model_list_(self):
        self.ui.comboBoxVoice.clear()
        self.ui.comboBoxVoice.addItem('None')
        self.ui.comboBoxVoice.addItems(Configuration._CONFIG()['settings']['models'])
        if Configuration._CONFIG()['settings']['voiceActive']:
            self.ui.comboBoxVoice.setCurrentIndex(
                Configuration._ACTIVE()+1)
        else: self.ui.comboBoxVoice.setCurrentIndex(0)

    def _get_comboBoxVoice_choice(self):
        active = self.ui.comboBoxVoice.currentText()
        if active != "None":
            Configuration.update_voice(active)
            if not Configuration._CONFIG()['settings']['voiceActive']:
                Configuration.reverse_active()
            Configuration.loaderON()
        else:
            if Configuration._CONFIG()['settings']['voiceActive']:
                Configuration.reverse_active()
                self.dia.show()
        self.__updater()

    def _get_comboBoxType_choice(self):
        active = self.ui.comboBoxType.currentText()
        if "Prime" in active.split()[0]:
            if not Configuration._CONFIG()['settings']['voiceActive']:
                Configuration.reverse_active()
        else:
            if Configuration._CONFIG()['settings']['voiceActive']:
                Configuration.reverse_active()
                self.dia.show()
        self.__updater()

    def _get_langMobels_choice(self):
        active = self.ui.langModels.currentText()
        if active not in Configuration._CONFIG()['settings']['lang_models']:
            if Configuration._CONFIG()['settings']['voiceActive']:
                Configuration.reverse_active()
                self.dia.show()
        else:
            index = Configuration._CONFIG()['settings']['lang_models'].index(active)
            Configuration.update_tts(index)
        self.__updater()

    def speedChanged(self, value):
        Configuration.change_speed(value)
        self.ui.speedSlider.setValue(
            Configuration._CONFIG()['settings']['voice']['speed'])
        self.ui.speedCount.setText(
            str(Configuration._CONFIG()['settings']['voice']['speed']))

    def protectChanged(self, value):
        Configuration.change_protect0(value/100)
        self.ui.protectSlider.setValue(
            int(Configuration._CONFIG()['settings']['voice']['protect0']*100))
        self.ui.protectCount.setText(
            str(Configuration._CONFIG()['settings']['voice']['protect0']))

    def tempChanged(self, value):
        Configuration.change_f0_key_up(value)
        self.ui.tempSlider.setValue(
            Configuration._CONFIG()['settings']['voice']['f0_key_up'])
        self.ui.tempCount.setText(
            str(Configuration._CONFIG()['settings']['voice']['f0_key_up']))

    def enumerating(self):
        self.newWindow = AppConfigurator(self.__appUpdater, 1)
        self.newWindow.show()

    def configurating(self):
        self.confWindow = AppConfigurator(self.__appUpdater, 0)
        self.confWindow.show()

    def appUpdate(self):
        Applicator.reloadAppList()
        self.__appUpdater()


class Tray(QSystemTrayIcon):
    def __init__(self, window: MainWindow) -> None:
        QSystemTrayIcon.__init__(self)
        self.setIcon(QIcon("ui/icon.png"))
        self.setVisible(True)

        self.window = window

        self.menuLang = Localization.get_MenuLang()

        self.showB = QAction(self.menuLang['showButton'])
        self.hideB = QAction(self.menuLang['hideButton'])
        self.stopB = QAction(self.menuLang['stopButton'])
        self.quitB = QAction(self.menuLang['quitButton'])

        self.showB.triggered.connect(window.showNormal)
        self.hideB.triggered.connect(window.hideNormal)
        self.stopB.triggered.connect(window.pause)
        self.quitB.triggered.connect(window.closeFROMTRAY)

        self.mainMenu = Menu("Miko!!")

        self.mainMenu.newSection("youshika control")
        self.mainMenu.newSeparator()
        self.mainMenu.newAction(self.showB)
        self.mainMenu.newAction(self.hideB)
        self.mainMenu.newAction(self.stopB)
        self.mainMenu.newSeparator()
        self.mainMenu.newAction(self.quitB)

        self.setContextMenu(self.mainMenu)

class Menu(QMenu):
    def __init__(self, title: str) -> None:
        QMenu.__init__(self)
        self.setTitle(title)
        
    def newAction(self, action):        self.addAction(action)
    def newDefaultAction(self, action): self.setDefaultAction(action)
    def newSeparator(self):             self.addSeparator()
    def newSection(self, text):         self.addSection(text)
    def newMenu(self, menu):            self.addMenu(menu)