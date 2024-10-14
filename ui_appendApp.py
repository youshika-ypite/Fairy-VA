# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'steamEoyvyj.ui'
##
## Created by: Qt User Interface Compiler version 6.7.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QMainWindow, QPushButton, QSizePolicy, QTextEdit,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(508, 150)
        MainWindow.setMinimumSize(QSize(508, 150))
        MainWindow.setMaximumSize(QSize(508, 150))
        MainWindow.setStyleSheet(u"QFrame {\n"
"	background-color: rgb(229, 229, 234);\n"
"}")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.main = QWidget(self.centralwidget)
        self.main.setObjectName(u"main")
        self.verticalLayout_2 = QVBoxLayout(self.main)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.frame = QFrame(self.main)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.t1 = QLabel(self.frame)
        self.t1.setObjectName(u"t1")

        self.horizontalLayout_3.addWidget(self.t1)

        self.inputName = QTextEdit(self.frame)
        self.inputName.setObjectName(u"inputName")

        self.horizontalLayout_3.addWidget(self.inputName)


        self.verticalLayout_2.addWidget(self.frame)

        self.frame_2 = QFrame(self.main)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frame_2)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.t2 = QLabel(self.frame_2)
        self.t2.setObjectName(u"t2")

        self.horizontalLayout_4.addWidget(self.t2)

        self.inputPath = QTextEdit(self.frame_2)
        self.inputPath.setObjectName(u"inputPath")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.inputPath.sizePolicy().hasHeightForWidth())
        self.inputPath.setSizePolicy(sizePolicy)
        self.inputPath.setMaximumSize(QSize(16777215, 40))
        self.inputPath.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.inputPath.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.inputPath.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)

        self.horizontalLayout_4.addWidget(self.inputPath)

        self.saveButton = QPushButton(self.frame_2)
        self.saveButton.setObjectName(u"saveButton")

        self.horizontalLayout_4.addWidget(self.saveButton)


        self.verticalLayout_2.addWidget(self.frame_2)


        self.verticalLayout.addWidget(self.main)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.t1.setText(QCoreApplication.translate("MainWindow", u"Please enter Name for your app", None))
        self.t2.setText(QCoreApplication.translate("MainWindow", u"Enter path to .exe", None))
        self.saveButton.setText(QCoreApplication.translate("MainWindow", u"Save", None))
    # retranslateUi

