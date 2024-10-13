import os

from ui_assistDialog import *
from ui_changerPath import *

from PySide6.QtWidgets import QLayout, QScrollArea, QGridLayout
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

def new_app(data: dict, updater, pch) -> QWidget:
 
    def confirm(layout: QLayout, widget: QWidget):
        layout.removeWidget(widget)
        widget.deleteLater()
        Applicator.deleteNeedAcceptApps(data["name"], data['possible_path'])
        updater()

    def change(layout: QLayout, widget: QWidget):
        pch(PathChanger(
            data,
            updater,
            [layout, widget]))
 
    def delete(layout: QLayout, widget: QWidget):
        layout.removeWidget(widget)
        widget.deleteLater()
        Applicator.deleteNeedAcceptApps(data["name"], data['possible_path'], True)
        updater()

    widget = QWidget()
    #widget.setStyleSheet(
    #    "* {background-color: rgb(229, 229, 234);}\n"
    #    "QPushButton {border: 1px solid;}"
    #    )
    layout      = QVBoxLayout(widget)
    seplayoutf  = QHBoxLayout()
    seplayouts  = QHBoxLayout()
    s1 = QFrame()
    s2 = QFrame()

    _ = "Relative path is: "
    labelName   = QLabel(data['name'])
    labelUsapp  = QLabel(str(data['user_application']))
    labelPath   = QLabel(_+str(data['possible_path']))

    btn_change  = QPushButton(text="Change path")
    btn_confirm = QPushButton(text="Confirm path")
    btn_delete  = QPushButton(text="Delete")

    btn_change.clicked.connect(lambda: change(layout, widget))
    btn_confirm.clicked.connect(lambda: confirm(layout, widget))
    btn_delete.clicked.connect(lambda: delete(layout, widget))

    seplayoutf.addWidget(labelName,  Qt.AlignLeft, Qt.AlignTop)
    seplayoutf.addWidget(labelUsapp, Qt.AlignLeft, Qt.AlignTop)

    seplayoutf.addWidget(btn_change,  Qt.AlignRight, Qt.AlignTop)
    seplayoutf.addWidget(btn_confirm, Qt.AlignRight, Qt.AlignTop)
    seplayoutf.addWidget(btn_delete, Qt.AlignRight, Qt.AlignTop)

    seplayouts.addWidget(labelPath, Qt.AlignLeft, Qt.AlignTop)

    seplayoutf.setContentsMargins(0, 0, 0, 0)
    seplayouts.setContentsMargins(0, 0, 0, 0)

    s1.setLayout(seplayoutf)
    s2.setLayout(seplayouts)

    layout.addWidget(s1, alignment=Qt.AlignTop)
    layout.addWidget(s2, alignment=Qt.AlignTop)
 
    return widget

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
        self.ui.comboBox.setCurrentText(datapack['possible_path'])
        self.ui.path.setText(datapack['possible_path'])

        self.ui.saveButton.clicked.connect(lambda: self._savePath(datapack['possible_path']))

    def _savePath(self, activePath) -> None:
        def checkAttr(path: str) -> int | list:
            errors = -1
            if any(
                [
                    path[1] != ":",
                    not path.endswith(tuple([".exe", ".lnk", ".url"]))
                ]
            ): errors = 1

            if errors == -1:
                if not os.path.isfile(path): errors = 0

            if errors == -1: return 0
            elif errors == 1: return 1
            else: return -1

        _name = self.ui.t1.text().replace("Please select your Path to ", "")
        _path = self.ui.inputPath.toPlainText()
        if _path is None or _path == "": _path = activePath
        result = checkAttr(path=_path)
        if result != 0:
            if result == -1: notify("Miko!! Error!", "Выбранный вами файл не найден!")
            elif result == 1: notify("Miko!! Error!", "Выбранный вами путь содержит ошибки!")
            return

        Applicator.deleteNeedAcceptApps(_name, _path)
        self.updater()
        if self.windows is not None:
            self.windows[0].removeWidget(self.windows[1])
            self.windows[1].deleteLater()
        self.close()

class EnumerateApps(QMainWindow):
    def __init__(self, updater) -> None:
        super().__init__()

        self.setStyleSheet(
            "QPushButton:hover {background-color: lightblue;}"
        )

        self.setWindowIcon(QIcon("ui/icon.png"))
        self.setWindowTitle("Miko!! App configurator")
  
        self.grid = QGridLayout()
        self.grid.setSpacing(5)
        self.widget = QWidget()
        self.layout = QGridLayout(self.widget)
  
        self.apps = [
            new_app(
                app, updater, self.pchangershow
                ) for app in Applicator.getNeedAcceptApps().values()
            ]

        for i, app in enumerate(self.apps):
            self.layout.addWidget(
                app, i, 0,
                alignment=Qt.AlignTop)
  
        self.scroller = QScrollArea()
        self.scroller.setWidgetResizable(True)
        self.scroller.setWidget(self.widget)
        self.setCentralWidget(self.scroller)

        self.setMinimumWidth(self.scroller.width()+25)
        self.setMinimumHeight(204)

    def pchangershow(self, pchange: PathChanger):
        self.pchange = pchange
        self.pchange.show()

def generateApp(data: dict, updater, pch):

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

    def change(): pch(PathChanger(data, updater))

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
    changeButton = QPushButton("Change App")

    openButton.setToolTip(data['possible_path'])

    openButton.clicked.connect(lambda: openRoot(appPath))
    deleteButton.clicked.connect(lambda: delete(mainlayout, widget, data["name"]))
    changeButton.clicked.connect(change)

    firstlayout.addWidget(appLabel)
    firstlayout.addWidget(openButton)

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
    def __init__(self, updater):
        super().__init__()

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

        matrix = [0, 0]

        self.apps = [
            generateApp(
                data, updater, self.pchangershow
                ) for data in Applicator.getApps().values() if 'name' in data
            ]
        for i, app in enumerate(self.apps):
            self.appLayout.addWidget(
                app, matrix[0], matrix[1],
                alignment=Qt.AlignTop)
            if matrix[1] != 1:
                matrix[1] += 1
            else:
                matrix[0] += 1
                matrix[1] = 0

        self.scroller = QScrollArea()
        self.scroller.setWidgetResizable(True)

        self.mainlayout.addWidget(self.infoFrame)
        self.mainlayout.addWidget(self.scroller)

        self.scroller.setWidget(self.appWidget)

        self.setCentralWidget(self.widget)
        self.setMinimumWidth(self.scroller.width()+25)
        self.setMinimumHeight(570)

    def pchangershow(self, pchange: PathChanger):
        self.pchange = pchange
        self.pchange.show()

    def newApp(self): pass