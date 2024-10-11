import os

from ui_assistDialog import *
from ui_changerPath import *

from PySide6.QtWidgets import QLayout, QScrollArea, QGridLayout
from configure__main import Applicator
from win11toast import notify

class NotifyDialog(QDialog):
    def __init__(self, icon=None):
        QDialog.__init__(self)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.setWindowTitle("Miko!! notificate")
        self.setWindowIcon(icon)

def new_app(app: dict, updater, pch) -> QWidget:
 
    def confirm(layout: QLayout, widget: QWidget):
        layout.removeWidget(widget)
        widget.deleteLater()
        Applicator.deleteNeedAcceptApps(app["name"], app['possible_path'])
        updater()

    def change(layout: QLayout, widget: QWidget):
        pch(PathChanger(
            app,
            updater,
            [layout, widget]))
 
    widget = QWidget()
    widget.setStyleSheet(
        "* {background-color: rgb(229, 229, 234);}\n"
        "QPushButton {border: 1px solid;}"
        )
    layout      = QVBoxLayout(widget)
    seplayoutf  = QHBoxLayout()
    seplayouts  = QHBoxLayout()

    _ = "Relative path is: "
    labelName   = QLabel(app['name'])
    labelUsapp  = QLabel(str(app['user_application']))
    labelPath   = QLabel(_+str(app['possible_path']))

    btn_change  = QPushButton(text="Change path")
    btn_confirm = QPushButton(text="Confirm path")

    btn_change.clicked.connect(lambda: change(layout, widget))
    btn_confirm.clicked.connect(lambda: confirm(layout, widget)) # New dialog (steam.ui in designer)
 
    seplayoutf.addWidget(labelName,  Qt.AlignLeft, Qt.AlignTop)
    seplayoutf.addWidget(labelUsapp, Qt.AlignLeft, Qt.AlignTop)

    seplayoutf.addWidget(btn_change,  Qt.AlignRight, Qt.AlignTop)
    seplayoutf.addWidget(btn_confirm, Qt.AlignRight, Qt.AlignTop)

    seplayouts.addWidget(labelPath, Qt.AlignLeft, Qt.AlignTop)

    seplayoutf.setContentsMargins(0, 0, 0, 0)
    seplayouts.setContentsMargins(0, 0, 0, 0)

    s1 = QFrame()
    s2 = QFrame()

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
            windows: list[QLayout, QWidget]
            ) -> None:
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.windows = windows
        self.updater = updater

        self.setWindowTitle(f"Miko!! {datapack['name']}")
        self.ui.t1.setText(f"Please select your Path to {datapack['name']}")
        self.ui.comboBox.setCurrentText(datapack['possible_path'])
        self.ui.path.setText(datapack['possible_path'])

        self.ui.saveButton.clicked.connect(self._savePath)

    def _savePath(self) -> None:
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

        result = checkAttr(path=_path)
        if result != 0:
            if result == -1: notify("Miko!! Error!", "Выбранный вами файл не найден!")
            elif result == 1: notify("Miko!! Error!", "Выбранный вами путь содержит ошибки!")
            return

        Applicator.deleteNeedAcceptApps(_name, _path)
        self.updater()
        self.windows[0].removeWidget(self.windows[1])
        self.windows[1].deleteLater()
        self.close()

class EnumerateApps(QMainWindow):
    def __init__(self, updater) -> None:
        super().__init__()

        # Настройка ICON
        self.setWindowTitle("Miko!! App configurator")
  
        self.grid = QGridLayout()
        self.grid.setSpacing(5)
        self.widget = QWidget()
        self.layout = QGridLayout(self.widget)
  
        self.apps = [new_app(app, updater, self.pchangershow) for app in Applicator.getNeedAcceptApps().values()]

        for i, app in enumerate(self.apps):
            self.layout.addWidget(
                app, i, 0,
                alignment=Qt.AlignTop)
  
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)
        self.setCentralWidget(self.scroll)

        self.setMinimumWidth(self.scroll.width()+25)
        self.setMinimumHeight(204)

    def pchangershow(self, pchange: PathChanger):
        self.pchange = pchange
        self.pchange.show()