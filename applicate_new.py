import sys

from configure__main import App, Applicator, LlamaConfig, Localization
from applicate_dialogs import AppConfigurator, Notify, Changer

from ui_int import *

from PySide6.QtGui import QAction, QMouseEvent
from PySide6.QtWidgets import QSystemTrayIcon, QMenu

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.notify = Notify()
        self.changer = Changer()

        with open("ui_style.css", "r") as file:
            self.setStyleSheet(file.read())

        self.setWindowTitle("Fairy VA")
        self.setWindowIcon(QIcon("ui/icon.png"))
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.oldpos = None

        self.ui.SelectLangBox.addItems(["RU", "EN"])

        self.load_language()
        self.load_sliders()
        self.load_models()

        self.ui.stackedWidget.setCurrentIndex(0)

        # Отступы - новая страница/другой фрейм
        self.ui.InfoButton.clicked.connect(self._InfoClick)
        self.ui.SliderButton.clicked.connect(self._SliderClick)
        self.ui.AboutButton.clicked.connect(self._AboutClick)
        self.ui.AppsButton.clicked.connect(self._configurating)
        self.ui.hideButton.clicked.connect(self._hideNormal)
        self.ui.closeButton.clicked.connect(self._closeFROMTRAY)

        self.ui.SelectModelBox.activated.connect(self._changeVoiceModel)
        self.ui.SelectLangBox.activated.connect(self._change_language)
        self.ui.SelectVModBox.activated.connect(self._changeModel)
        self.ui.PauseButton.clicked.connect(self.pause)
        self.ui.ModButton.clicked.connect(self._mod)
        self.ui.NoLlamaButton.clicked.connect(self._NoLlama)

        self.ui.ReloadApps.clicked.connect(self._reloadApps)
        self.ui.ReloadModels.clicked.connect(self._reloadModels)
        self.ui.ReloadConfig.clicked.connect(self._reloadConfig)

        self.ui.IndexspinBox.setValue(LlamaConfig.currentContextIndex())
        self.ui.saveIndexButton.clicked.connect(self._saveIndex)
        self.ui.clearContextButton.clicked.connect(self._clearContext)
        self.ui.ollamaNameChangeButton.clicked.connect(self._ollamaNameChange)
        self.ui.promptEditButton.clicked.connect(self._promptChange)
        self.ui.GitHubbtn.clicked.connect(self._git_)
        self.ui.Supportbtn.clicked.connect(self._support_)

        self.updater()

    def _InfoClick(self): # Изменение страницы
        self.ui.stackedWidget.setCurrentIndex(0)
    def _SliderClick(self): # Изменение страницы
        self.ui.IndexspinBox.setValue(LlamaConfig.currentContextIndex())
        self.ui.stackedWidget.setCurrentIndex(1)
    def _AboutClick(self): # Изменение страницы
        self.ui.stackedWidget.setCurrentIndex(2)
    
    def _configurating(self): # Конфигуратор приложений
        # Перезагрузка сетки приложений если она изменялась (защита)
        self.confWindow = AppConfigurator()
        self.confWindow.show()
        
    def showNormal(self):
        self.show()
    def _hideNormal(self):
        self.hide()
    def _closeFROMTRAY(self):
        App.stopApp()
        Applicator._checkSave()
        LlamaConfig.save()
        self.close()
    def closeEvent(self, event):
        self.hide()
        event.ignore()

    def _changeVoiceModel(self): # Изменение голосовой одели
        active = self.ui.SelectModelBox.currentText()
        if active == "None":
            if App.voiceModule():
                App.reverseVoiceModule()
                self.notify.changeText(self.notify_lang["voiceWarn"])
                self.notify.show()
        else:
            App.updateVoiceModule(active)
            if not App.voiceModule(): App.reverseVoiceModule()
            if not App.LOAD(): App.reLOAD()
        self.updater()

    def _change_language(self): # Изменение языка локализации
        language = self.ui.SelectLangBox.currentText()
        index = 1 if language == "RU" else 3
        if App.voiceModule(): self.ui.SelectVModBox.setCurrentIndex(index)
        Localization.changeLang(language)
        self.load_language()

    def _changeModel(self): # Изменение базовой модели
        active = self.ui.SelectVModBox.currentText()
        if active == "None":
            if App.voiceModule():
                App.reverseVoiceModule()
                self.notify.changeText(self.notify_lang["voiceWarn"])
                self.notify.show()
        else: App.updateBasedModels(App.based_Mods().index(active))
        self.updater()

    def pause(self):
        App.setPause()
        pause = App.PAUSE()
        key = 'on' if not pause else 'off'
        self.ui.PauseButton.setText(self.lang_Local['PauseButton-'+key])
        text = self.ui.PauseStatusLabel.text()
        spld = text.split(": ")
        self.ui.PauseStatusLabel.setText(text.replace(spld[1], str(pause)))

    def _mod(self): pass # Изменим под управление поиском в интерноте
    def _NoLlama(self): pass # Мод отключения функции Ламы (только после добавления поиска в интернете)
    # Перезагрузка и пересчет найденных приложений (монитор отсутствует)
    def _reloadApps(self): Applicator.reloadAppList()
    # Перезагрузка RVC моделей из папки weights
    def _reloadModels(self):
        App.search()
        self.ui.SelectModelBox.clear()
        self.ui.SelectModelBox.addItem('None')
        self.ui.SelectModelBox.addItems(App.modelsList())
        index = App.modelIndex()+1
        if App.voiceModule(): self.ui.SelectModelBox.setCurrentIndex(index)
        else: self.ui.SelectModelBox.setCurrentIndex(0)
    # Принудительная перезагрузка конфигурации из файлов (на случай ошибочной записи в самой программе)
    def _reloadConfig(self): App.load()
    # Сохранение индекса кол-ва контекстных сообщений
    def _saveIndex(self):
        value = self.ui.IndexspinBox.value()
        LlamaConfig.setCurrentContextIndex(value*-1)
    # Отчистка контекста ([0] сохранится - базовый промпт)
    def _clearContext(self):
        LlamaConfig.clearContext()
        self.notify.changeText(self.notify_lang['contextClear'])
        self.notify.show()
    # Изменение ollama конфигурации
    def _ollamaNameChange(self): self.changer.show_OllamaNameChange()
    def _promptChange(self): self.changer.show_OllamaPromptChange()
    # Ссылки в браузере
    def _git_(self): App.open(0)
    def _support_(self): App.open(1)

    # Обновляет изменения от QComboBox связанные с RVC
    def updater(self):
        AML = self.ui.ActiveModelLabel.text()
        change = AML[AML.index(":"):]
        if App.voiceModule():
            modelslist, index = App.modelsList(), App.modelIndex()
            active = modelslist[index]
            AML = AML.replace(change, f": {active}")
            self.ui.ActiveModelLabel.setText(AML)
            models, model = App.based_Mods(), App.model()['tts']
            self.ui.SelectModelBox.setCurrentIndex(index+1)
            self.ui.SelectVModBox.setCurrentIndex(models.index(model)+1)
        else:
            AML = AML.replace(change, ": None")
            self.ui.ActiveModelLabel.setText(AML)
            self.ui.SelectModelBox.setCurrentIndex(0)
            self.ui.SelectVModBox.setCurrentIndex(0)
    ## Управление положением окна
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
    ## Загрузка списка Голосовых и Базовых моделей из конфига (Новые RVC не ищет)
    def load_models(self):
        self.models = App.modelsList()
        self.langModels = App.based_Mods()
        self.ui.SelectModelBox.addItem("None")
        self.ui.SelectModelBox.addItems(self.models)
        self.ui.SelectVModBox.addItem("None")
        self.ui.SelectVModBox.addItems(self.langModels)
    ## Загрузка данных слайдеров из конфига, назначение лимитов и подключение
    def load_sliders(self):
        voiceSettings = App.model()
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
    ## Изменения от слайдеров
    def _changeSpeed(self, value):
        App.change_speed(value)
        self.ui.speedKeyLabelVAL.setText(str(App.model()["speed"]))
    def _changeProtect0(self, value):
        App.change_protect0(value/100)
        self.ui.protectKeyLabelVAL.setText(str(App.model()["protect0"]))
    def _changeTemp0(self, value):
        App.change_f0_key_up(value)
        self.ui.tempKeyLabelVAL.setText(str(App.model()["f0_key_up"]))
    ## Последнее сообщение от Ollama модели
    def load_last_message(self) -> str:
        lastmessage = ""
        try: response = LlamaConfig.currentResponses()[-1]
        except Exception as exc:
            print("Please reload llama.json | ", exc)
            response = "None"
        if len(response) != 0: lastmessage = response
        return str(lastmessage)

    ## Локализация приложения
    def load_language(self):        
        lang = Localization.getLANG().replace("_TG", "")
        self.lang_Local = Localization.get_AppLang()
        self.notify_lang = Localization.get_NotificateLang()

        self.ui.SelectLangBox.setCurrentIndex(1 if lang == "EN" else 0)

        self.ui.AboutButton.setText(self.lang_Local['AboutButton'])
        self.ui.AppsButton.setText(self.lang_Local['AppsButton'])
        self.ui.InfoButton.setText(self.lang_Local['InfoButton'])
        self.ui.SliderButton.setText(self.lang_Local['SliderButton'])

        self.ui.AppVILabel.setText(self.lang_Local['AppVILabel'])
        self.ui.closeButton.setText(self.lang_Local['closeButton'])
        self.ui.hideButton.setText(self.lang_Local['hideButton'])

        message = self.lang_Local['ContextMessage'] + self.load_last_message()
        self.ui.resourceMonitor.setText(message)

        self.ui.ContextIndexLabel.setText(self.lang_Local['ContextIndexLabel'])
        self.ui.clearContextButton.setText(self.lang_Local['clearContextButton'])
        self.ui.promptEditButton.setText(self.lang_Local['promptEditButton'])
        self.ui.ollamaNameChangeButton.setText(self.lang_Local['ollamaNameChangeButton'])
        self.ui.GitHubbtn.setText(self.lang_Local['GitHubbtn'])
        self.ui.Supportbtn.setText(self.lang_Local['Supportbtn'])

        pause = App.PAUSE()
        voiceActive = App.voiceModule()

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
        
        if not App.modelsList(): App.search()
        vmodels = App.modelsList()
        models = "\n\n"
        model = vmodels[App.modelIndex()]
        if not App.voiceModule(): model = "None"
        MD = self.lang_Local['ActiveModelLabel'].replace(":MD:", model)
        for i, el in enumerate(vmodels, 0):models += f"|| {i} - {el}\n"
        MDS = self.lang_Local['FoundModelsLabel'].replace(":MDS:", models)
        P = self.lang_Local['PauseStatusLabel'].replace(":P:", str(pause))

        self.ui.ActiveModelLabel.setText(MD)
        self.ui.FoundModelsLabel.setText(MDS)
        self.ui.PauseStatusLabel.setText(P)

        self.ui.tempLabel.setText("temp0")
        self.ui.speedLabel.setText("speed")
        self.ui.protect0Label.setText("protect0")
    
    # Обновление вне системы (для обработки событий алгоритма)
    def __update(self):
        if LlamaConfig.isNewContent():
            message = self.lang_Local['ContextMessage'] + self.load_last_message()
            self.ui.resourceMonitor.setText(message)
            LlamaConfig.setNewContent(False)


class Application:
    def __init__(self):
        self.app = QApplication(sys.argv+['-style', 'fusion', '-platform', 'windows:darkmode=0'])
        self.app.setFont(QFont("Mi Sans", 10))

        self._window()

    def set_exec(self):
        self.app.exec()

    def _window(self):
        self.window = MainWindow()
        self.window.showNormal()
        self._tray()

    def get_window(self) -> MainWindow:
        return self.window

    def _tray(self):
        self.tray = Tray(self.window)

class Menu(QMenu):
    def __init__(self, title: str) -> None:
        QMenu.__init__(self)
        self.setTitle(title)
        
    def newAction(self, action):        self.addAction(action)
    def newDefaultAction(self, action): self.setDefaultAction(action)
    def newSeparator(self):             self.addSeparator()
    def newSection(self, text):         self.addSection(text)
    def newMenu(self, menu):            self.addMenu(menu)

class Tray(QSystemTrayIcon):
    def __init__(self, window: MainWindow) -> None:
        QSystemTrayIcon.__init__(self)
        self.setIcon(QIcon("ui/icon.png"))
        self.setVisible(True)

        self.window = window

        self.mainMenu = Menu("Fairy VA")
        self.menuLang = Localization.get_MenuLang()

        self.showB = QAction(self.menuLang['showButton'])
        self.hideB = QAction(self.menuLang['hideButton'])
        self.stopB = QAction(self.menuLang['stopButton'])
        self.quitB = QAction(self.menuLang['quitButton'])

        self.showB.triggered.connect(window.showNormal)
        self.hideB.triggered.connect(window._hideNormal)
        self.stopB.triggered.connect(window.pause)
        self.quitB.triggered.connect(window._closeFROMTRAY)

        self.mainMenu.newAction(self.showB)
        self.mainMenu.newAction(self.hideB)
        self.mainMenu.newAction(self.stopB)
        self.mainMenu.newSeparator()
        self.mainMenu.newAction(self.quitB)

        self.setContextMenu(self.mainMenu)