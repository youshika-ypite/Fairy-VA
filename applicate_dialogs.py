import os

from ui_assistDialog import *
from ui_changerPath import *
from ui_appendApp import Ui_MainWindow as ac_Ui_MainWindow

from PySide6.QtWidgets import QLayout, QScrollArea, QGridLayout, QWidget
from configure__main import Applicator

colors = {"red": "🔴", "yellow": "🟡", "green": "🟢"}

class NotifyDialog(QDialog):
    def __init__(self, icon=None):
        QDialog.__init__(self)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.setWindowTitle("Miko!! notificate")
        self.setWindowIcon(icon)

        self.notificateTexts = {
            "voiceWarn": "Please, close and open again app for the changes to free up mem",

            "pathError_f": "Path not found",
            "pathError_w": "Path is incorrect",
            "pathError_e": "Path cannot be empty",
            "pathError_n": "The path does not exist",
            
            "nameError_e": "Name cannot be empty"
            }
        

    def setText(self, text: str = None, key: str = None):
        """
        ### Keys : values
        * voiceWarn - "Please, close and open again app for the changes to free up mem"
        * pathError_f - "Path not found"
        * pathError_w - "Path is incorrect"
        * pathError_e - "Path cannot be an empty"
        * pathError_n - "The path does not exist"
        * nameError_e - "Name cannot be empty"
        """
        if text is None: text = self.notificateTexts[key]
        trigger = text
        self.ui.label.setText(trigger)

    def fastNotificate(self, text: str = None, key: str = None):
        """
        ### Keys : values
        * voiceWarn - "Please, close and open again app for the changes to free up mem"
        * pathError_f - "Path not found"
        * pathError_w - "Path is incorrect"
        * pathError_e - "Path cannot be an empty"
        * pathError_n - "The path does not exist"
        * nameError_e - "Name cannot be empty"
        """
        self.setText(text, key)
        self.show()

class AppCreator(QMainWindow):
    def __init__(self, icon: QIcon, updater, notificator: NotifyDialog) -> None:
        QMainWindow.__init__(self)
        self.ui = ac_Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle(f"Miko!!")
        self.setWindowIcon(icon)
        self.setStyleSheet(
            "QPushButton:hover {background-color: lightblue;}"
            )

        self.updater = updater
        self.notificator = notificator
        self.ui.saveButton.clicked.connect(self.save_app)

    def save_app(self):
        _name = self.ui.inputName.toPlainText()
        _path = self.ui.inputPath.toPlainText()

        if _name in ["", " ", None]:
            self.notificator.fastNotificate(key="nameError_e")
            return
        if _path in ["", " ", None]:
            self.notificator.fastNotificate(key="pathError_e")
            return
        if _path[1] != ":" or not _path.endswith(tuple([".exe", ".lnk", ".url"])):
            self.notificator.fastNotificate(key="pathError_w")
            return
        if not os.path.isfile(_path):
            self.notificator.fastNotificate(key="pathError_n")
            return
        
        Applicator.appendApp(_name, _path)
        self.updater()

class PathChanger(QMainWindow):
    def __init__(
            self,
            datapack: dict, updater,
            icon: QIcon,
            notificator: NotifyDialog,
            windows: list[QLayout, QWidget] = None
            ) -> None:
        
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowIcon(icon)
        self.setStyleSheet(
            "QPushButton:hover {background-color: lightblue;}"
            )

        self.windows = windows
        self.updater = updater
        self.notificator = notificator

        self.setWindowTitle(f"Miko!! {datapack['name']}")
        self.ui.t1.setText(f"Please select your Path to {datapack['name']}")
        self.ui.comboBox.addItem(datapack['possible_path'])
        self.ui.path.setText(datapack['possible_path'])

        self.ui.comboBox.activated.connect(self.boxTrigger)

        self.ui.saveButton.clicked.connect(
            lambda: self._savePath(datapack['possible_path'])
            )

    def boxTrigger(self):
        self.ui.inputPath.setText(self.ui.comboBox.currentText())

    def _savePath(self, activePath) -> None:

        _name = self.ui.t1.text().replace("Please select your Path to ", "")
        _path = self.ui.inputPath.toPlainText()
        if any([_path is None, _path == "", _path == " "]):
            selected = self.ui.comboBox.currentText()
            _path = selected if selected == activePath else activePath
        if _path[0] == '"': _path = _path.replace('"', '')
        if _path[1] != ":" or not _path.endswith(tuple([".exe", ".lnk", ".url"])) or not os._path.isfile(_path):
            self.notificator.fastNotificate(key="pathError_w")

        Applicator.deleteNeedAcceptApps(_name, _path)
        self.updater()
        if self.windows is not None:
            self.windows[0].removeWidget(self.windows[1])
            self.windows[1].deleteLater()
        self.close()

def generateApp(data: dict, updater, icon: QIcon, pch, confirmBtn: bool, notificator: NotifyDialog):

    def remover(layout: QLayout, widget: QWidget):
        layout.removeWidget(widget)
        widget.deleteLater()

    def confirm(layout: QLayout, widget: QWidget):
        remover(layout, widget)
        Applicator.deleteNeedAcceptApps(data["name"], data["possible_path"])
        updater()

    def openDir(_path: str | None):
        if _path is None:
            notificator.fastNotificate(key='pathError_f')
            return
        symbol_ID = 0
        for ind in range(-1, len(_path)*-1, -1):
            if _path[ind] == "\\":
                symbol_ID = ind
                break
        if symbol_ID != 0:
            openPATH = _path[:symbol_ID]
            if os.path.exists(openPATH): os.startfile(openPATH)
            else: notificator.fastNotificate(key="pathError_f")
        else: notificator.fastNotificate(key="pathError_w")

    def _delete(layout: QLayout, widget: QWidget, name: str):
        remover(layout, widget)
        Applicator.deleteApp(name)
        updater()

    def _change(layout: QLayout, widget: QWidget):
        pch(PathChanger(data, updater, icon, notificator, [layout, widget]))

    widget = QWidget()

    mainlayout = QVBoxLayout(widget)
    _firstdlayout = QVBoxLayout()
    _firstlayout_adt = QHBoxLayout()
    _secondlayout = QHBoxLayout()

    __firstdFrame, __secondFrame, __firstFrame_adt = QFrame(), QFrame(), QFrame()
    
    color, status = colors["green"], 'ready'
    styleSheet = '*{background-color: #00d26a; border: 0.5px solid gray; border-radius:2px;}'

    if data["possible_path"] is None:
        color, status = colors["red"], 'need confirm'
        styleSheet = '*{background-color: #ff5252; border: 0.5px solid gray; border-radius:2px;}'
    elif data["relative_path"] is None:
        color, status = colors["yellow"], 'need path'
        styleSheet = '*{background-color: #ffda13; border: 0.5px solid gray; border-radius:2px;}'

    appName, _appStatus, appPath = QLabel(color+data["name"]), QLabel(status), data["possible_path"]
    openButton = QPushButton("Open directory")
    chngButton, _delButton = QPushButton("Change path"), QPushButton("Delete app")

    _appStatus.setStyleSheet(styleSheet)
    _delButton.setStyleSheet("QPushButton {background-color: #ff5252;}")

    openButton.setToolTip(data['possible_path'])

    openButton.clicked.connect(lambda: openDir(appPath))
    _delButton.clicked.connect(lambda: _delete(mainlayout, widget, data["name"]))
    chngButton.clicked.connect(lambda: _change(mainlayout, widget))

    _firstlayout_adt.addWidget(appName)
    _firstlayout_adt.addWidget(_appStatus, alignment=Qt.AlignRight)

    __firstFrame_adt.setLayout(_firstlayout_adt)

    _firstdlayout.addWidget(__firstFrame_adt)
    _firstdlayout.addWidget(openButton)

    if confirmBtn:
        confirmButton = QPushButton("Confirm")
        confirmButton.setStyleSheet("QPushButton {background-color: #00d26a;}")
        confirmButton.clicked.connect(
            lambda: confirm(mainlayout, widget)
        )
        _secondlayout.addWidget(confirmButton)
    _secondlayout.addWidget(chngButton)
    _secondlayout.addWidget(_delButton)

    _firstdlayout.setContentsMargins(0, 0, 0, 0)
    _secondlayout.setContentsMargins(0, 0, 0, 0)

    __firstdFrame.setLayout(_firstdlayout)
    __secondFrame.setLayout(_secondlayout)

    mainlayout.addWidget(__firstdFrame)
    mainlayout.addWidget(__secondFrame)

    return widget

class AppConfigurator(QMainWindow):
    def __init__(self, updater, enumerator):
        super().__init__()

        icon = QIcon("ui/icon.png")

        self.setStyleSheet(
            "QPushButton:hover {background-color: lightblue;}"
            )
        self.setWindowTitle(f"Miko!! App Configurator")
        self.setWindowIcon(icon)

        self.notificator = NotifyDialog(icon)

        self.widget = QWidget()
        self.appWidget = QWidget()
        self.mainlayout = QVBoxLayout(self.widget)

        self.appLayout = QGridLayout(self.appWidget)

        self.infoFrame = QFrame()
        self.infoLayout = QHBoxLayout()

        self.addAppButton = QPushButton("Add another app")
        self.addAppButton.clicked.connect(lambda: self.newApp(icon, updater))
        
        self.infoLayout.addWidget(QLabel(
            "| "\
            f"{colors['green']} - Good |"\
            f"{colors['yellow']} - Need confirm to use |"\
            f"{colors['red']} - Need path |"
            ))
        self.infoLayout.addWidget(self.addAppButton)
        self.infoFrame.setLayout(self.infoLayout)

        if enumerator:
            self.apps = [
                generateApp(
                    data, updater, icon, self.pchangershow, confirmBtn=True, notificator=self.notificator
                    ) for data in Applicator.getNeedAcceptApps().values() if 'name' in data
                ]
        else:
            self.apps = [
                generateApp(
                    data, updater, icon, self.pchangershow, confirmBtn=False, notificator=self.notificator
                    ) for data in Applicator.getApps().values() if 'name' in data
                ]

        self.matrix_build()
        self.paint()

        self.setMinimumWidth(self.scroller.width()+75)
        self.setMinimumHeight(570)

    def matrix_build(self):
        matrix = [0, 0]
        for i, app in enumerate(self.apps):
            self.appLayout.addWidget(
                app, matrix[0], matrix[1],
                alignment=Qt.AlignTop
                )
            if matrix[1] != 1: matrix[1] += 1
            else:
                matrix[0] += 1
                matrix[1] = 0

    def paint(self):
        self.scroller = QScrollArea()
        self.scroller.setWidgetResizable(True)

        self.mainlayout.addWidget(self.infoFrame)
        self.mainlayout.addWidget(self.scroller)

        self.scroller.setWidget(self.appWidget)

        self.setCentralWidget(self.widget)

    def pchangershow(self, pchange: PathChanger):
        self.pchange = pchange
        self.pchange.show()

    def newApp(self, icon, updater):
        self.appCreator = AppCreator(icon, updater, self.notificator)
        self.appCreator.show()