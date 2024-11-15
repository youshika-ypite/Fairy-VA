import os

from configure__main import Applicator, Localization, LlamaConfig

from ui_notify import Ui_Dialog as UID_notify
from ui_changer import *

from PySide6.QtWidgets import QLayout, QScrollArea, QGridLayout
from PySide6.QtWidgets import QWidget, QMainWindow, QLabel, QSpacerItem
from PySide6.QtWidgets import QFrame, QVBoxLayout
from PySide6.QtWidgets import QHBoxLayout, QPushButton
from PySide6.QtGui import Qt, QIcon

class Notify(QDialog):
    def __init__(self) -> None:
        QDialog.__init__(self)
        self.ui = UID_notify()
        self.ui.setupUi(self)
        self.setWindowTitle("Fairy VA - Notificate/Уведомление")
        self.setWindowIcon(QIcon("ui/icon.png"))

        self.ui.label.setText("None")

    def notify(self): self.show()
    def changeText(self, text): self.ui.label.setText(text)

class Changer(QDialog):
    def __init__(self) -> None:
        QDialog.__init__(self)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon("ui/icon.png"))

        self.notify = Notify()

        self.lang = Localization.get_ChangerLang()
        self.ui.buttonBox.rejected.connect(self.closer)

    def passing(self):
        pass

    def closer(self):
        self.ui.buttonBox.accepted.connect(self.passing)

    def shower(self):
        self.ui.buttonBox.button(QDialogButtonBox.StandardButton.Save).setEnabled(True)
        self.show()

    def disconnect(self):
        try: self.ui.buttonBox.accepted.disconnect()
        except: pass

    def path_init(self, app_dict: dict):
        self.disconnect()
        name = app_dict["name"]
        self.setWindowTitle(name)
        self.ui.label.setText(self.lang["PathChange"]["text"].replace(":APP:", name))
        _path = app_dict["possible_path"]
        pht = self.lang["PathChange"]["placeHolderText"] if _path is None else _path 
        self.ui.textEdit.setPlaceholderText(pht)

        self.ui.buttonBox.accepted.connect(lambda: self.savePath(app_dict))

    def show_PathChanger(self): self.shower()
        
    def savePath(self, app_dict: dict):
        self.disconnect()
        path_ = app_dict["possible_path"]
        _path = self.ui.textEdit.toPlainText()
        if _path not in ["", " ", None]:
            if _path != path_:
                if all(
                    [
                        _path[1] == ":",
                        os.path.isfile(_path)
                    ]
                    ):
                    Applicator.updateApp(app_dict["name"], _path)
                    
                    self.ui.label.setText('✅'+self.ui.label.text())
                    self.ui.buttonBox.button(QDialogButtonBox.StandardButton.Save).setEnabled(False)

                else:
                    self.ui.label.setText(self.ui.label.text()+"\n"+self.lang["error_wp"])
                    self.ui.buttonBox.accepted.connect(lambda: self.savePath(app_dict))
            else:
                self.ui.label.setText(self.ui.label.text()+"\n"+self.lang["error_rp"])
                self.ui.buttonBox.accepted.connect(lambda: self.savePath(app_dict))
        else:
            self.ui.textEdit.setPlaceholderText(self.lang["error_e"])
            self.ui.buttonBox.accepted.connect(lambda: self.savePath(app_dict))

    def create_init(self):
        self.disconnect()
        self.setWindowTitle("Create app")
        self.ui.label.setText(self.lang["AppCreate"]["text_0"])
        self.ui.textEdit.setPlaceholderText(self.lang["AppCreate"]["placeHolderText_0"])

        self.ui.buttonBox.accepted.connect(self.next_step)

    def show_AppCreator(self): self.shower()

    def next_step(self):
        self.disconnect()
        _name = self.ui.textEdit.toPlainText()
        if _name not in ["", " ", None]:
            self.ui.label.setText(self.lang["AppCreate"]["text_1"] +" "+ _name)
            self.ui.textEdit.setPlaceholderText(self.lang["AppCreate"]["placeHolderText_1"])
            self.ui.textEdit.setText("")
            self.ui.buttonBox.accepted.connect(lambda: self.saveApp(_name))
        else:
            self.ui.textEdit.setPlaceholderText(self.lang["error_e"])
            self.ui.buttonBox.accepted.connect(self.next_step)

    def saveApp(self, name: str):
        self.disconnect()
        text = self.ui.label.text()
        if "\n" in text:
            self.ui.label.setText(text[:text.index("\n")])
        _path = self.ui.textEdit.toPlainText()
        if _path not in ["", " ", None]:
            if all(
                [
                    _path[1] == ":",
                    os.path.isfile(_path)
                ]
                ):
                Applicator.appendApp(name, _path)

                self.ui.label.setText('✅'+self.ui.label.text())
                self.ui.buttonBox.button(QDialogButtonBox.StandardButton.Save).setEnabled(False)

            else:
                self.ui.label.setText(self.ui.label.text()+"\n"+self.lang["error_wp"])
                self.ui.buttonBox.accepted.connect(lambda: self.saveApp(name))
        else:
            self.ui.textEdit.setPlaceholderText(self.lang["error_e"])
            self.ui.buttonBox.accepted.connect(lambda: self.saveApp(name))

    def show_OllamaPromptChange(self):
        self.disconnect()
        self.ui.label.setText(self.lang['OllamaPromptChange']['text'])
        self.ui.textEdit.setPlaceholderText(self.lang['OllamaPromptChange']['placeHolderText'])
        self.ui.textEdit.setText(LlamaConfig.currentPrompt())

        self.ui.buttonBox.accepted.connect(self.savePrompt)
        self.shower()

    def savePrompt(self):
        self.disconnect()
        prompt = self.ui.textEdit.toPlainText()
        if prompt not in ["", " ", None]:
            if prompt != LlamaConfig.currentPrompt():
                LlamaConfig.setCurrentPrompt(prompt)
                LlamaConfig.clearContext(prompt=True)

            self.ui.label.setText('✅'+self.ui.label.text())
            self.ui.buttonBox.button(QDialogButtonBox.StandardButton.Save).setEnabled(False)
        else:
            self.ui.textEdit.setText(self.lang['error_e'])
            self.ui.buttonBox.accepted.connect(self.savePrompt)

    def show_OllamaNameChange(self):
        self.disconnect()
        self.ui.label.setText(self.lang['OllamaNameChange']['text'])
        self.ui.textEdit.setPlaceholderText(self.lang['OllamaNameChange']['placeHolderText'])
        self.ui.textEdit.setText(LlamaConfig.currentModel())

        self.ui.buttonBox.accepted.connect(self.saveName)
        self.shower()

    def saveName(self):
        self.disconnect()
        name = self.ui.textEdit.toPlainText()
        if name not in ["", " ", None]:
            if name != LlamaConfig.currentModel():
                LlamaConfig.setModelName(name)
            
            self.ui.label.setText('✅'+self.ui.label.text())
            self.ui.buttonBox.button(QDialogButtonBox.StandardButton.Save).setEnabled(False)
        else:
            self.ui.textEdit.setText(self.lang['error_e'])
            self.ui.buttonBox.accepted.connect(self.saveName)

def generateApp(data: dict, pchangershow, notify_lang: dict, ToolTip_lang: dict):

    notificator = Notify()

    colors = ["#ff5252", "#e4ce0c", "rgba(0, 0, 0, 0)"]

    def remover(layout: QLayout, widget: QWidget):
        layout.removeWidget(widget)
        widget.deleteLater()

    def confirm(layout:QLayout, button: QWidget, infoButton: QWidget, mainframe: QFrame):
        Applicator.deleteApp(data["name"], acceptKey=True)
        remover(layout, button)
        infoButton.setToolTip(str(ToolTip_lang["infoBtn_0"]))
        mainframe.setStyleSheet("#mainframeB {"\
                                    "border-left-style: solid;"\
                                    "border-left-width: 3px;"\
                                    "border-left-color: rgba(0, 0, 0, 0);"\
                                "}")

    def openDir(_path: str | None):
        if _path is None:
            notificator.changeText(notify_lang["pathError_e"])
            notificator.show()
            return
        symbol_ID = 0
        for ind in range(-1, len(_path)*-1, -1):
            if _path[ind] == "\\":
                symbol_ID = ind
                break
        if symbol_ID != 0:
            openPATH = _path[:symbol_ID]
            if os.path.exists(openPATH): os.startfile(openPATH)
            else:
                notificator.changeText(notify_lang["pathError_f"])
                notificator.show()
        else:
            notificator.changeText(notify_lang["pathError_w"])
            notificator.show()

    def _delete(layout: QLayout, widget: QWidget, name: str):
        remover(layout, widget)
        Applicator.deleteApp(name, appKey=True)

    def _change():
        ch = Changer()
        ch.path_init(data)
        pchangershow(ch)

    dataNeed = data["possible_path"] is None
    accessNeed = data['relative_path'] is None and not dataNeed

    color = colors[0] if dataNeed else colors[1] if accessNeed else colors[2]

    widget = QWidget()

    mainlayout = QHBoxLayout(widget)
    mainlayout.setContentsMargins(0, 0, 0, 0)
    
    secondlayout = QHBoxLayout()
    secondlayout.setContentsMargins(0, 0, 0, 0)
    
    mainframe = QFrame()
    mainframe.setObjectName("mainframeB")
    mainframe.setStyleSheet("#mainframeB {"\
                                    "border-left-style: solid;"\
                                    "border-left-width: 3px;"\
                                    "border-left-color: "+color+";"\
                                "}")
    mainframe.setContentsMargins(0, 0, 0, 0)

    Name = QLabel(data["name"])
    Name.setObjectName("namer")

    spacer_item = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

    buttonSize = QSize(18, 18)

    infoButton = QPushButton("")
    infoButton.setIconSize(buttonSize)
    infoButton.setObjectName("infoBtn")
    key = "infoBtn_1" if accessNeed and not dataNeed else "infoBtn_0"
    infoButton.setToolTip(ToolTip_lang[key])
    infoButton.setToolTipDuration(0.5)
    infoButton.setIcon(QIcon("ui/svg/alert-circle.svg"))

    warnButton = QPushButton("")
    warnButton.setIconSize(buttonSize)
    warnButton.setObjectName("warnBtn")
    warnButton.setToolTip(ToolTip_lang["warnBtn"])
    warnButton.setToolTipDuration(0.5)
    warnButton.setIcon(QIcon("ui/svg/alert-triangle.svg"))

    editButton = QPushButton("")
    editButton.setIconSize(buttonSize)
    editButton.setObjectName("editBtn")
    editButton.setToolTip(ToolTip_lang["editBtn"])
    editButton.setToolTipDuration(0.5)
    editButton.setIcon(QIcon("ui/svg/edit.svg"))
    editButton.clicked.connect(_change)

    deleteButton = QPushButton("")
    deleteButton.setIconSize(buttonSize)
    deleteButton.setObjectName("deleteBtn")
    deleteButton.setToolTip(ToolTip_lang["deleteBtn"])
    deleteButton.setToolTipDuration(0.5)
    deleteButton.setIcon(QIcon("ui/svg/slash.svg"))
    deleteButton.clicked.connect(lambda: _delete(mainlayout, widget, data["name"]))
    
    applyButton = QPushButton("")
    applyButton.setIconSize(buttonSize)
    applyButton.setObjectName("applyBtn")
    applyButton.setToolTip(ToolTip_lang["applyBtn"])
    applyButton.setToolTipDuration(0.5)
    applyButton.setIcon(QIcon("ui/svg/check.svg"))
    applyButton.clicked.connect(lambda: confirm(secondlayout, applyButton, infoButton, mainframe))

    urlButton = QPushButton("")
    urlButton.setIconSize(buttonSize)
    urlButton.setObjectName("urlBtn")
    urlButton.setToolTip(ToolTip_lang["urlBtn"]+str(data['possible_path']))
    urlButton.setToolTipDuration(0.5)
    urlButton.setIcon(QIcon("ui/svg/arrow-up-right.svg"))
    urlButton.clicked.connect(lambda: openDir(data["possible_path"]))

    if not dataNeed: secondlayout.addWidget(infoButton)
    else: secondlayout.addWidget(warnButton)

    secondlayout.addWidget(Name)
    secondlayout.addItem(spacer_item)

    if accessNeed and not dataNeed: secondlayout.addWidget(applyButton)
    if not dataNeed: secondlayout.addWidget(urlButton)

    secondlayout.addWidget(editButton)
    secondlayout.addWidget(deleteButton)

    mainframe.setLayout(secondlayout)
    mainlayout.addWidget(mainframe)

    return widget

class AppConfigurator(QMainWindow):
    def __init__(self):
        super().__init__()

        with open("ui_confStyle.css", "r") as file:
            self.setStyleSheet(file.read())
        self.setWindowTitle(f"Fairy!! | App Configurator / Конфигуратор приложений")
        self.setWindowIcon(QIcon("ui/icon.png"))

        self.notificator = Notify()

        self.lang_load()

        self.pchange = None
        self.appCreator = None

        self.widget = QWidget()
        self.appWidget = QWidget()
        self.mainlayout = QVBoxLayout(self.widget)

        self.infoFrame = QFrame()
        self.infoLayout = QHBoxLayout()

        self.addAppButton = QPushButton(self.localizationSeconds["addAppButton"])
        self.addAppButton.setObjectName("AABtn")
        self.addAppButton.clicked.connect(self.newApp)
        
        apps = Applicator.getApps().values()
        self.apps, self.appsPath = [], {}

        for data in apps:
            if "name" in data:
                self.apps.append(
                    generateApp(
                        data,
                        self.pchangershow,
                        self.notifyLang,
                        self.localizationToolTip))
                if data['relative_path'] is None and data['possible_path'] is not None:
                    self.appsPath[data['name']] = data['possible_path']  

        self.infoLayout.addWidget(self.addAppButton)
        self.infoFrame.setLayout(self.infoLayout)

        self.matrix_build()

        self.setMinimumWidth(int(self.scroller.width()))
        self.setMinimumHeight(570)

    def lang_load(self):
        self.notifyLang = Localization.get_NotificateLang()
        self.localizationSeconds = Localization.get_SecondsWinLang()
        self.localizationToolTip = Localization.get_ToolLang()

    def closeEvent(self, event):
        if self.pchange is not None:
            try: self.pchange.close()
            except: pass
        if self.appCreator is not None:
            try: self.appCreator.close()
            except: pass
        Applicator._checkSave()

    def matrix_build(self):
        self.appLayout = QGridLayout(self.appWidget)
        for i, app in enumerate(self.apps):
            self.appLayout.addWidget(
                app, i, 0,
                alignment=Qt.AlignTop
                )

        self.scroller = QScrollArea()
        self.scroller.setWidgetResizable(True)

        self.mainlayout.addWidget(self.infoFrame)
        self.mainlayout.addWidget(self.scroller)

        self.scroller.setWidget(self.appWidget)
        self.setCentralWidget(self.widget)

    def pchangershow(self, pchange: Changer):
        self.pchange = pchange
        self.pchange.show_PathChanger()

    def newApp(self):
        self.appCreator = Changer()
        self.appCreator.create_init()
        self.appCreator.show_AppCreator()