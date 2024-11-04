import sys

from configure_localization import Localization
from configure__main import Configuration, Applicator
from applicate_dialogs import AppConfigurator, NotifyDialog

from ui_int import *

from PySide6.QtGui import QAction, QMouseEvent
from PySide6.QtWidgets import QSystemTrayIcon, QMenu
from PySide6.QtCore import Qt

class Application:
    def __init__(self):
        self.app = QApplication(sys.argv + ['-platform', 'windows:darkmode=0'])
        self.app.setStyle('Fusion')

        self.window = MainWindow()
        self.tray   = Tray(self.window)

        self.window.show()
        self.app.exec()

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.dia = NotifyDialog()
        self.dia.setText(key="voiceWarn")

        self.setWindowTitle("Fairy VA")
        self.setWindowIcon(QIcon("ui/icon.png"))
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.oldpos = None
        self.load_models()
        self.load_language()
        self.load_sliders()

        self.ui.InfoButton.clicked.connect(self._InfoClick)
        self.ui.SliderButton.clicked.connect(self._SliderClick)
        self.ui.AboutButton.clicked.connect(self._AboutClick)
        self.ui.AppsButton.clicked.connect(self.configurating)

        self.ui.PauseButton.clicked.connect(self.pause)

        self.ui.hideButton.clicked.connect(self.hideNormal)
        self.ui.closeButton.clicked.connect(self.closeFROMTRAY)

        self.ui.SelectModelBox.activated.connect(self._changeVoiceModel)
        self.ui.SelectLangBox.activated.connect(self._change_language)
        self.ui.SelectVModBox.activated.connect(self._changeModel)

        self.ui.ReloadApps.clicked.connect(self._reloadApps)
        self.ui.ReloadModels.clicked.connect(self._reloadModels)
        self.ui.ReloadConfig.clicked.connect(self._reloadConfig)

        self.updater()

    def _InfoClick(self):
        self.ui.stackedWidget.setCurrentIndex(0)
    def _SliderClick(self):
        self.ui.stackedWidget.setCurrentIndex(1)
    def _AboutClick(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    def _reloadApps(self):
        Applicator.reloadAppList()

        countALL = Applicator.getAppsCount()
        countReady = Applicator.getReadyAppsCount()
        countData = Applicator.getNeedDataAppsCount()
        countConfirm = Applicator.getNeedAcceptAppsCount()

    def _reloadModels(self):
        self.ui.SelectModelBox.clear()
        Configuration.search()
        self.ui.SelectModelBox.addItem('None')
        self.ui.SelectModelBox.addItems(Configuration._CONFIG()['settings']['models'])
        if Configuration._CONFIG()['settings']['voiceActive']:
            self.ui.SelectModelBox.setCurrentIndex(
                Configuration._ACTIVE()+1)
        else: self.ui.SelectModelBox.setCurrentIndex(0)

    def _reloadConfig(self):
        Configuration.save()
        Configuration.load()

    def _changeVoiceModel(self):
        settings = Configuration._CONFIG()['settings']
        active = self.ui.SelectModelBox.currentText()
        if active == "None":
            if settings['voiceActive']:
                Configuration.reverse_active()
                self.dia.show()
        else:
            Configuration.update_voice(active)
            if not settings['voiceActive']:
                Configuration.reverse_active()
            Configuration.loaderON()
    
        self.updater()

    def _changeModel(self):
        settings = Configuration._CONFIG()['settings']
        active = self.ui.SelectVModBox.currentText()
        if active == "None":
            if settings['voiceActive']: Configuration.reverse_active()
        else:
            index = settings['lang_models'].index(active)
            Configuration.update_tts(index)

        self.updater()

    def updater(self):
        settings = Configuration._CONFIG()['settings']
        AML = self.ui.ActiveModelLabel.text()
        change = AML[AML.index(":"):]
        
        if settings['voiceActive']:
            vm = Configuration._CONFIG()['settings']['models']
            active = vm[Configuration._ACTIVE()]
            AML = AML.replace(change, f": {active}")
            self.ui.ActiveModelLabel.setText(AML)

            self.ui.SelectModelBox.setCurrentIndex(Configuration._ACTIVE()+1)
            self.ui.SelectVModBox.setCurrentIndex(
                Configuration._CONFIG()['settings']['lang_models'].index(
                Configuration._CONFIG()['settings']['voice']['tts'])+1
            )
        else:
            AML = AML.replace(change, ": None")
            self.ui.ActiveModelLabel.setText(AML)

            self.ui.SelectModelBox.setCurrentIndex(0)
            self.ui.SelectVModBox.setCurrentIndex(0)

    def enumerating(self):
        self.newWindow = AppConfigurator(self.appUpdater, 1)
        self.newWindow.show()

    def configurating(self):
        self.confWindow = AppConfigurator(self.appUpdater, 0)
        self.confWindow.show()

    def appUpdater(self):
        Applicator.reloadAppList()
        
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

    def pause(self):
        Configuration.pause()
        pause = Configuration._PAUSE()
        key = 'on' if not pause else 'off'
        self.ui.PauseButton.setText(self.lang_Local['PauseButton-'+key])
        text = self.ui.PauseStatusLabel.text()
        spld = text.split(": ")
        self.ui.PauseStatusLabel.setText(text.replace(spld[1], str(pause)))

    def showNormal(self): self.show()
    def hideNormal(self): self.hide()
    def closeFROMTRAY(self):
        Configuration.stop()
        Applicator._checkSave()
        self.close()
    def closeEvent(self, event):
        self.hide()
        event.ignore()    

    def load_models(self):
        self.models = Configuration._CONFIG()['settings']['models']
        self.langModels = Configuration._CONFIG()['settings']['lang_models']

        self.ui.SelectModelBox.addItem("None")
        self.ui.SelectModelBox.addItems(self.models)

        self.ui.SelectVModBox.addItem("None")
        self.ui.SelectVModBox.addItems(self.langModels)

    def load_sliders(self):
        voiceSettings = Configuration._CONFIG()['settings']['voice']

        val = voiceSettings['speed']
        self.ui.speedKeyLabelVAL.setText(str(val))
        self.ui.speedSlider.setMinimum(0)
        self.ui.speedSlider.setMaximum(12)
        self.ui.speedSlider.setSingleStep(1)
        self.ui.speedSlider.setValue(val)
        self.ui.speedSlider.valueChanged.connect(self._changeSpeed)

        val = voiceSettings['protect0']
        self.ui.protectKeyLabelVAL.setText(str(val))
        self.ui.protect0Slider.setMinimum(0)
        self.ui.protect0Slider.setMaximum(100)
        self.ui.protect0Slider.setSingleStep(10)
        self.ui.protect0Slider.setValue(int(val*100))
        self.ui.protect0Slider.valueChanged.connect(self._changeProtect0)

        val = voiceSettings['f0_key_up']
        self.ui.tempKeyLabelVAL.setText(str(val))
        self.ui.temp0Slider.setMinimum(-12)
        self.ui.temp0Slider.setMaximum(12)
        self.ui.temp0Slider.setSingleStep(1)
        self.ui.temp0Slider.setValue(val)
        self.ui.temp0Slider.valueChanged.connect(self._changeTemp0)

    def _changeSpeed(self, value):
        Configuration.change_speed(value)
        self.ui.speedKeyLabelVAL.setText(
            str(Configuration._CONFIG()['settings']['voice']['speed'])
        )

    def _changeProtect0(self, value):
        Configuration.change_protect0(value/100)
        self.ui.protectKeyLabelVAL.setText(
            str(Configuration._CONFIG()['settings']['voice']['protect0'])
        )

    def _changeTemp0(self, value):
        Configuration.change_f0_key_up(value)
        self.ui.tempKeyLabelVAL.setText(
            str(Configuration._CONFIG()['settings']['voice']['f0_key_up'])
        )

    def _change_language(self):
        language = self.ui.SelectLangBox.currentText()
        index = 1 if language == "RU" else 3
        if Configuration._CONFIG()['settings']['voiceActive']:
            self.ui.SelectVModBox.setCurrentIndex(index)
        Localization.changeLang(language)
        self.load_language()

    def load_language(self):
        lang = Localization.getLANG().replace("_TG_LOCAL", "")
        self.lang_Local = Localization.get_AppLang()

        cnt = self.ui.SelectLangBox.count()
        if cnt == 0: self.ui.SelectLangBox.addItems(["RU", "EN"])
        self.ui.SelectLangBox.setCurrentIndex(1 if lang == "EN" else 0)

        self.ui.AboutButton.setText(self.lang_Local['AboutButton'])
        self.ui.AppsButton.setText(self.lang_Local['AppsButton'])
        self.ui.InfoButton.setText(self.lang_Local['InfoButton'])
        self.ui.SliderButton.setText(self.lang_Local['SliderButton'])

        self.ui.AppVILabel.setText(self.lang_Local['AppVILabel'])
        self.ui.closeButton.setText(self.lang_Local['closeButton'])
        self.ui.hideButton.setText(self.lang_Local['hideButton'])

        pause = Configuration._PAUSE()
        voiceActive = Configuration._CONFIG()['settings']['voiceActive']

        self.ui.ModLabel.setText(self.lang_Local['ModLabel'])
        key = 'on' if not voiceActive else 'off'
        self.ui.ModButton.setText(self.lang_Local['ModButton-'+key])

        self.ui.NoLlamaLabel.setText(self.lang_Local['NoLlamaLabel'])
        self.ui.NoLlamaButton.setText(self.lang_Local['NoLlamaButton-'+key])

        self.ui.PauseLabel.setText(self.lang_Local['PauseLabel'])
        key = 'on' if not pause else 'off'
        self.ui.PauseButton.setText(self.lang_Local['PauseButton-'+key])

        self.ui.SelectLangLabel.setText(self.lang_Local['SelectLangLabel'])
        self.ui.SelectModelLabel.setText(self.lang_Local['SelectModelLabel'])
        self.ui.SelectVModLabel.setText(self.lang_Local['SelectVModLabel'])

        self.ui.ReloadApps.setText(self.lang_Local['ReloadApps'])
        self.ui.ReloadModels.setText(self.lang_Local['ReloadModels'])
        self.ui.ReloadConfig.setText(self.lang_Local['ReloadConfig'])
        
        vmodels = Configuration._CONFIG()['settings']['models']
        models = "\n"
        model = vmodels[Configuration._ACTIVE()]
        if not Configuration._CONFIG()['settings']['voiceActive']: model = "None"
        MD = self.lang_Local['ActiveModelLabel'].replace(":MD:", model)
        for i, el in enumerate(vmodels, 0):models += f"{i}. - {el}\n"
        MDS = self.lang_Local['FoundModelsLabel'].replace(":MDS:", models)
        P = self.lang_Local['PauseStatusLabel'].replace(":P:", str(pause))

        self.ui.ActiveModelLabel.setText(MD)
        self.ui.FoundModelsLabel.setText(MDS)
        self.ui.LinksLabel.setText(self.lang_Local['LinksLabel'])
        self.ui.PauseStatusLabel.setText(P)

        self.ui.tempLabel.setText("temp0")
        self.ui.speedLabel.setText("speed")
        self.ui.protect0Label.setText("protect0")

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

        self.mainMenu = Menu("Fairy VA")

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