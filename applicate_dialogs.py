import os

from PySide6.QtCore import Qt

from ui_assistDialog import *
from ui_changerPath import *
from ui_appendApp import Ui_MainWindow as ac_Ui_MainWindow

from PySide6.QtWidgets import QLayout, QScrollArea, QGridLayout, QWidget
from PySide6.QtGui import QIcon
from configure__main import Applicator
from win11toast import notify

colors = {"red": "🔴", "yellow": "🟡", "green": "🟢"}

class NotifyDialog(QDialog):
    def __init__(self, icon=None):
        QDialog.__init__(self)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.setWindowTitle("Miko!! notificate")
        self.setWindowIcon(icon)

class AppCreator(QMainWindow):
    def __init__(self, updater) -> None:
        QMainWindow.__init__(self)
        self.ui = ac_Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle(f"Miko!!")
        self.setStyleSheet(
            "QPushButton:hover {background-color: lightblue;}"
        )

        self.updater = updater
        self.ui.saveButton.clicked.connect(self.save_app)

    def save_app(self):
        _name = self.ui.inputName.toPlainText()
        _path = self.ui.inputPath.toPlainText()

        if _name in ["", " ", None]:
            notify("Miko!! Error!", "The name cannot be empty!", app_id="youshika")
            return
        if _path[1] != ":" or not _path.endswith(tuple([".exe", ".lnk", ".url"])):
            notify("Miko!! Error!", "The path was entered incorrectly!", app_id="youshika")
            return
        if not os.path.isfile(_path):
            notify("Miko!! Error!", "There is no such way!", app_id="youshika")
            return
        
        Applicator.appendApp(_name, _path)
        self.updater()

class PathChanger(QMainWindow):
    def __init__(
            self,
            datapack: dict,
            updater,
            windows: list[QLayout, QWidget] = None
            ) -> None:
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setStyleSheet(
            "QPushButton:hover {background-color: lightblue;}"
        )

        self.windows = windows
        self.updater = updater

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
            notify("Miko!! Error!", "There is no such way or it is wrong!", app_id="youshika")

        Applicator.deleteNeedAcceptApps(_name, _path)
        self.updater()
        if self.windows is not None:
            self.windows[0].removeWidget(self.windows[1])
            self.windows[1].deleteLater()
        self.close()

def generateApp(data: dict, updater, pch, confirmBtn: bool):

    def confirm(layout: QLayout, widget: QWidget):
        layout.removeWidget(widget)
        widget.deleteLater()
        Applicator.deleteNeedAcceptApps(data["name"], data['possible_path'])
        updater()

    def openRoot(path: str | None):
        if path is None:
            notify("Miko!! Error!", "App not found")
            return
        symbID = 0
        for i in range(-1, path.__len__()*-1, -1):
            if path[i] == "\\":
                symbID = i
                break
        if symbID != 0:
            if os.path.exists(path[:symbID]): os.startfile(path[:symbID])
            else: print("App not found", path[:symbID])
        else: print("Error")

    def delete(layout: QLayout, widget: QWidget, name: str):
        layout.removeWidget(widget)
        widget.deleteLater()
        Applicator.deleteApp(name)
        updater()

    def change(layout: QLayout, widget: QWidget):
        pch(PathChanger(data, updater, [layout, widget]))

    widget = QWidget()
    mainlayout = QVBoxLayout(widget)
    firstlayout = QVBoxLayout()
    secondlayout = QHBoxLayout()
    s1 = QFrame()
    s2 = QFrame()

    color = colors["green"]
    if data["possible_path"] is None: color = colors["red"]
    elif data["relative_path"] is None: color = colors["yellow"]
    appLabel = QLabel(color+data['name'])
    appPath = data['possible_path']

    openButton = QPushButton("Open directory")
    deleteButton = QPushButton("Delete App")
    changeButton = QPushButton("Change path")

    openButton.setToolTip(data['possible_path'])
    deleteButton.setStyleSheet("QPushButton {background-color: #ff5252;}")
    openButton.clicked.connect(lambda: openRoot(appPath))
    deleteButton.clicked.connect(lambda: delete(mainlayout, widget, data["name"]))
    changeButton.clicked.connect(lambda: change(mainlayout, widget))

    firstlayout.addWidget(appLabel)
    firstlayout.addWidget(openButton)

    if confirmBtn:
        confirmButton = QPushButton("Confirm")
        confirmButton.setStyleSheet("QPushButton {background-color: #00d26a;}")
        confirmButton.clicked.connect(
            lambda: confirm(mainlayout, widget)
            )
        secondlayout.addWidget(confirmButton)

    secondlayout.addWidget(changeButton)
    secondlayout.addWidget(deleteButton)

    firstlayout.setContentsMargins(0, 0, 0, 0)
    secondlayout.setContentsMargins(0, 0, 0, 0)

    s1.setLayout(firstlayout)
    s2.setLayout(secondlayout)

    mainlayout.addWidget(s1, alignment=Qt.AlignTop)
    mainlayout.addWidget(s2, alignment=Qt.AlignTop)

    return widget

class AppConfigurator(QMainWindow):
    def __init__(self, updater, enumerator):
        super().__init__()

        self.matrixMax = 1
        self.updater = updater

        self.setStyleSheet(
            "QPushButton:hover {background-color: lightblue;}"
        )
        self.setWindowTitle(f"Miko!! App Configurator")
        self.setWindowIcon(QIcon("ui/icon.png"))

        self.widget = QWidget()
        self.appWidget = QWidget()
        self.mainlayout = QVBoxLayout(self.widget)

        self.appLayout = QGridLayout(self.appWidget)

        self.infoFrame = QFrame()
        self.infoLayout = QHBoxLayout()
        self.addAppButton = QPushButton("Add another app")

        self.addAppButton.clicked.connect(self.newApp)
        self.infoLayout.addWidget(QLabel(
            f"{colors['green']} - Good |"\
            f"{colors['yellow']} - Need confirm to use |"\
            f"{colors['red']} - Need path |"
        ))
        self.infoLayout.addWidget(self.addAppButton)

        self.infoFrame.setLayout(self.infoLayout)

        if enumerator:
            self.apps = [
            generateApp(
                data, self.updater, self.pchangershow, confirmBtn=True
                ) for data in Applicator.getNeedAcceptApps().values() if 'name' in data
                ]
        else:
            self.matrixMax = 2
            self.apps = [
                generateApp(
                    data, self.updater, self.pchangershow, confirmBtn=False
                    ) for data in Applicator.getApps().values() if 'name' in data
                ]

        self._generate()
        self.setMinimumWidth(self.scroller.width()+25)
        self.setMinimumHeight(570)

    def _generate(self):
        self.matrix_build()
        self.paint()

    def matrix_build(self):
        matrix = [0, 0]
        for i, app in enumerate(self.apps):
            self.appLayout.addWidget(
                app, matrix[0], matrix[1],
                alignment=Qt.AlignTop
                )
            if matrix[1] != self.matrixMax:
                matrix[1] += 1
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

    def newApp(self):
        self.appCreator = AppCreator(self.updater)
        self.appCreator.show()