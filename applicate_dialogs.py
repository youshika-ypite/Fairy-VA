import os

from configure__main import Applicator, Localization

from ui_notify import *
from ui_appendApp import Ui_MainWindow as ac_Ui_MainWindow

from PySide6.QtWidgets import QLayout, QScrollArea, QGridLayout
from PySide6.QtWidgets import QWidget, QMainWindow, QLabel, QSpacerItem
from PySide6.QtWidgets import QFrame, QComboBox, QVBoxLayout
from PySide6.QtWidgets import QHBoxLayout, QPushButton, QTextEdit
from PySide6.QtGui import QMouseEvent, Qt, QIcon

class Notify(QDialog):
    def __init__(self) -> None:
        QDialog.__init__(self)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle("Fairy VA - Notificate/Уведомление")
        self.setWindowIcon(QIcon("ui/icon.png"))

        self.ui.label.setText("None")

    def notify(self): self.show()
    def changeText(self, text): self.ui.label.setText(text)

class AppCreator(QMainWindow):
    def __init__(self) -> None:
        QMainWindow.__init__(self)
        self.ui = ac_Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle(f"Fairy!!")
        self.setWindowIcon(QIcon("ui/icon.png"))
        self.setStyleSheet("QPushButton:hover {background-color: #00d26a;}")

        self.notificator = Notify()
        self.ui.saveButton.clicked.connect(self.save_app)

    def save_app(self):
        notify_lang = Localization.get_NotificateLang()

        _name = self.ui.inputName.toPlainText()
        _path = self.ui.inputPath.toPlainText()
        # Защита от копипаста пути от проводника с кавычкми
        if _path[0] == '"' and _path[-1] == '"':
            _path = _path[1:-1]
        # Проверка правльности пути
        if _name in ["", " ", None]:
            self.notificator.changeText(notify_lang["nameError_e"])
            self.notificator.show()
            return
        if _path in ["", " ", None]:
            self.notificator.changeText(notify_lang["pathError_e"])
            self.notificator.show()
            return
        if _path[1] != ":" or not _path.endswith(tuple([".exe", ".lnk", ".url"])):
            self.notificator.changeText(notify_lang["pathError_w"])
            self.notificator.show()
            return
        if not os.path.isfile(_path):
            self.notificator.changeText(notify_lang["pathError_f"])
            self.notificator.show()
            return
        
        Applicator.appendApp(_name, _path)

class PathChanger(QMainWindow):
    def __init__(
            self,
            datapack: dict,
            windows: list[QLayout, QWidget] = None
            ) -> None:
        super().__init__()
        
        self.windows = windows
        self.notificator = Notify()

        self.secondWin = Localization.get_SecondsWinLang()
        self.notify_lang = Localization.get_NotificateLang()

        self.activePath = datapack['possible_path']
        if self.activePath is None: self.activePath = "None"
        self.name = datapack['name']

        self.setWindowTitle("Fairy!!"+self.name)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowIcon(QIcon("ui/icon.png"))
        self.setStyleSheet(
            "QFrame {border-color: black; border-width: 2px}\n"\
            "#tittle {border-style: solid solid dotted solid;}\n"\
            "#input {border-style: none solid none solid;}\n"\
            "#info {border-style: dotted solid solid solid;}\n"\
            "#saveButton:hover {background-color: #00d26a;}\n"\
            "#deltButton:hover {background-color: #ff5252;}\n"\
            "#cancButton:hover {background-color: lightblue;}"
            )
        
        self.oldpos = None

        self.widget = QWidget()
        self.mainlayout = QVBoxLayout(self.widget)

        self.tittleFrame = QFrame()
        self.inputFrame = QFrame()
        self.infoFrame = QFrame()

        self.inputFrame.setObjectName("input")
        self.tittleFrame.setObjectName("tittle")
        self.infoFrame.setObjectName("info")

        self.tittlelayout = QHBoxLayout()
        self.inputlayout = QHBoxLayout()
        self.infolayout = QHBoxLayout()

        self.tittle_infoText = QLabel(self.secondWin['infoText']+self.name)
        self.tittle_pathBox = QComboBox()
        self.tittle_pathBox.addItem(self.activePath)
        self.tittle_pathBox.activated.connect(self.boxTrigger)

        self.tittlelayout.addWidget(self.tittle_infoText)
        self.tittlelayout.addWidget(self.tittle_pathBox)

        self.tittleFrame.setLayout(self.tittlelayout)

        self.input_info = QLabel(self.secondWin['inputText'])
        self.input_inputPath = QTextEdit()
        self.input_inputPath.setMaximumHeight(40)
        self.input_saveButton = QPushButton(self.secondWin['saveButton'])
        self.input_saveButton.clicked.connect(self._savePath)
        self.input_saveButton.setObjectName("saveButton")

        self.inputlayout.addWidget(self.input_info)
        self.inputlayout.addWidget(self.input_inputPath)
        self.inputlayout.addWidget(self.input_saveButton)

        self.inputFrame.setLayout(self.inputlayout)

        self.info_path = QLabel(self.secondWin["infoPath"]+self.activePath)
        self.info_deltButton = QPushButton(self.secondWin["deleteButton"])
        self.info_deltButton.clicked.connect(self._delete)
        self.info_deltButton.setObjectName("deltButton")
        self.info_cancButton = QPushButton(self.secondWin["cancelButton"])
        self.info_cancButton.clicked.connect(self._cancel)
        self.info_cancButton.setObjectName("cancButton")

        self.infolayout.addWidget(self.info_path)
        self.infolayout.addWidget(self.info_deltButton)
        self.infolayout.addWidget(self.info_cancButton)

        self.infoFrame.setLayout(self.infolayout)

        self.mainlayout.addWidget(self.tittleFrame)
        self.mainlayout.addWidget(self.inputFrame)
        self.mainlayout.addWidget(self.infoFrame)

        self.setCentralWidget(self.widget)

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

    def getBoxText_(self) -> str: return self.tittle_pathBox.currentText()

    def getPath_(self) -> str:
        _path = self.input_inputPath.toPlainText()
        if any([_path is None, _path == "", _path == " "]):
            selected = self.tittle_pathBox.currentText()
            _path = selected if selected == self.activePath else self.activePath
        if _path[0] == '"': _path = _path.replace('"', '')
        if _path[1] != ":" or not _path.endswith(tuple([".exe", ".lnk", ".url"])
                                                 ) or not os.path.isfile(_path):
            self.notificator.changeText(self.notify_lang["pathError_w"])
            self.notificator.show()
        return _path
    
    def remove_(self) -> None:
        if self.windows is not None:
            self.windows[0].removeWidget(self.windows[1])
            self.windows[1].deleteLater()

    def _delete(self) -> None:
        Applicator.deleteApp(self.name, appKey=True)
        self.remove_()
        self.close()

    def _savePath(self) -> None:
        _path = self.getPath_()

        Applicator.deleteApp(self.name, acceptKey=True, path=_path)
        self.close()

    def _cancel(self) -> None: self.close()
    def boxTrigger(self): self.input_inputPath.setText(self.getBoxText_())

def generateApp(data: dict, pchangershow, ToolTip_lang: dict):

    notificator = Notify()
    notify_lang = Localization.get_NotificateLang()

    colors = ["#ff5252", "#e4ce0c"]

    def remover(layout: QLayout, widget: QWidget):
        layout.removeWidget(widget)
        widget.deleteLater()

    def confirm(layout: QLayout, button: QWidget):
        remover(layout, button)
        Applicator.deleteApp(data["name"], acceptKey=True)

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

    def _change(layout: QLayout, widget: QWidget):
        pchangershow(PathChanger(data, [layout, widget]))

    dataNeed = data["possible_path"] is None
    accessNeed = data['relative_path'] is None and not dataNeed

    color = colors[0] if dataNeed else colors[1] if accessNeed else None

    widget = QWidget()

    mainlayout = QHBoxLayout(widget)
    mainlayout.setContentsMargins(0, 0, 0, 0)
    
    secondlayout = QHBoxLayout()
    secondlayout.setContentsMargins(0, 0, 0, 0)
    
    mainframe = QFrame()
    mainframe.setObjectName("mainframeB")
    if color is not None:
        mainframe.setStyleSheet(\
            "#mainframeB{"\
                "border-left-style: solid;"\
                "border-left-width: 3px;"\
                "border-left-color: "+color+";"\
            "}")
    mainframe.setContentsMargins(0, 0, 0, 0)

    Name = QLabel(data["name"])
    Name.setObjectName("namer")

    spacer_item = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

    buttonSize = QSize(18, 18)

    secondlayout.addWidget(Name)
    secondlayout.addItem(spacer_item)

    editButton = QPushButton("")
    editButton.setIconSize(buttonSize)
    editButton.setObjectName("editBtn")
    editButton.setToolTip(str(ToolTip_lang["editBtn"]))
    editButton.setToolTipDuration(0.5)
    editButton.setIcon(QIcon("ui/svg/edit.svg"))
    editButton.clicked.connect(lambda: _change(mainlayout, widget))

    deleteButton = QPushButton("")
    deleteButton.setIconSize(buttonSize)
    deleteButton.setObjectName("deleteBtn")
    deleteButton.setToolTip(str(ToolTip_lang["deleteBtn"]))
    deleteButton.setToolTipDuration(0.5)
    deleteButton.setIcon(QIcon("ui/svg/slash.svg"))
    deleteButton.clicked.connect(lambda: _delete(mainlayout, widget, data["name"]))
    
    applyButton = QPushButton("")
    applyButton.setIconSize(buttonSize)
    applyButton.setObjectName("applyBtn")
    applyButton.setToolTip(str(ToolTip_lang["applyBtn"]))
    applyButton.setToolTipDuration(0.5)
    applyButton.setIcon(QIcon("ui/svg/check.svg"))
    applyButton.clicked.connect(lambda: confirm(secondlayout, applyButton))

    urlButton = QPushButton("")
    urlButton.setIconSize(buttonSize)
    urlButton.setObjectName("urlBtn")
    urlButton.setToolTip(str(ToolTip_lang["urlBtn"])+str(data['possible_path']))
    urlButton.setToolTipDuration(0.5)
    urlButton.setIcon(QIcon("ui/svg/arrow-up-right.svg"))
    urlButton.clicked.connect(lambda: openDir(data["possible_path"]))

    if dataNeed: urlButton.setVisible(False)
    if not accessNeed: applyButton.setVisible(False)

    secondlayout.addWidget(applyButton)
    secondlayout.addWidget(urlButton)

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

        self.localizationSeconds = Localization.get_SecondsWinLang()
        self.localizationToolTip = Localization.get_ToolLang()

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
                self.apps.append(generateApp(data, self.pchangershow, self.localizationToolTip))
                if data['relative_path'] is None and data['possible_path'] is not None:
                    self.appsPath[data['name']] = data['possible_path']  

        self.infoLayout.addWidget(self.addAppButton)
        self.infoFrame.setLayout(self.infoLayout)

        self.matrix_build()

        self.setMinimumWidth(int(self.scroller.width()))
        self.setMinimumHeight(570)

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

    def pchangershow(self, pchange: PathChanger):
        self.pchange = pchange
        self.pchange.show()

    def newApp(self):
        self.appCreator = AppCreator()
        self.appCreator.show()

    def confirm(self):
        def close(): self.tempFrame.deleteLater()
        def agree():
            for app in self.appsPath:
                Applicator.deleteApp(app, acceptKey=True)
            self.warningText.setText(
                self.localizationSeconds["warningText"]
            )
            self.agreeButton.deleteLater()
            for i, app in enumerate(self.apps): app.deleteLater()

        text = self.localizationSeconds["warningText_1"]+"\n"
        text += self.localizationSeconds["warningText_2"]+"\n"

        for app in self.appsPath.values():
            text = f"{text}\n{str(app)}"

        self.tempLayout = QVBoxLayout()
        self.tempFrame = QFrame()
        self.tempFrame.setObjectName("mainTempFrame")
        self.secondTempLayout = QHBoxLayout()
        self.secondTempFrame = QFrame()

        self.warningText = QLabel(text)

        self.agreeButton = QPushButton(self.localizationSeconds["agreeButton"])
        self.agreeButton.setObjectName("agreeButton")
        self.agreeButton.clicked.connect(agree)
        
        self.backButton = QPushButton(self.localizationSeconds["backdButton"])
        self.backButton.clicked.connect(close)

        self.secondTempLayout.addWidget(self.agreeButton)
        self.secondTempLayout.addWidget(self.backButton)
        self.secondTempFrame.setLayout(self.secondTempLayout)

        self.tempLayout.addWidget(self.warningText)
        self.tempLayout.addWidget(self.secondTempFrame)

        self.tempFrame.setLayout(self.tempLayout)

        self.mainlayout.addWidget(self.tempFrame)