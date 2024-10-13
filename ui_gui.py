# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'assistHYNkmz.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QHBoxLayout,
    QLabel, QMainWindow, QPushButton, QSizePolicy,
    QSlider, QSpacerItem, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(507, 593)
        MainWindow.setMinimumSize(QSize(507, 593))
        MainWindow.setMaximumSize(QSize(507, 593))
        MainWindow.setStyleSheet(u"QFrame {\n"
"	border: 0;\n"
"}\n"
"\n"
"QLabel {\n"
"	color: black;\n"
"}\n"
"\n"
"#frame_3, #frame_4, #frame_5, #frame_15, #frame_16, #frame_17, #frame_9, #frame_13, #frame_11 {\n"
"	background-color: rgba(229, 229, 234, 130);\n"
"}\n"
"QPushButton:hover {\n"
"   background-color: lightblue;\n"
"}\n"
"QComboBox:hover {\n"
"   background-color: lightblue;\n"
"}")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.mainmenu = QWidget(self.centralwidget)
        self.mainmenu.setObjectName(u"mainmenu")
        self.verticalLayout_2 = QVBoxLayout(self.mainmenu)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.selectorVOICE = QWidget(self.mainmenu)
        self.selectorVOICE.setObjectName(u"selectorVOICE")
        self.verticalLayout_3 = QVBoxLayout(self.selectorVOICE)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.frame = QFrame(self.selectorVOICE)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.labelType = QLabel(self.frame)
        self.labelType.setObjectName(u"labelType")

        self.horizontalLayout_2.addWidget(self.labelType)

        self.horizontalSpacer = QSpacerItem(445, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.comboBoxType = QComboBox(self.frame)
        self.comboBoxType.addItem("")
        self.comboBoxType.addItem("")
        self.comboBoxType.setObjectName(u"comboBoxType")

        self.horizontalLayout_2.addWidget(self.comboBoxType)


        self.verticalLayout_3.addWidget(self.frame)

        self.frame_2 = QFrame(self.selectorVOICE)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame_2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.labelVoice = QLabel(self.frame_2)
        self.labelVoice.setObjectName(u"labelVoice")

        self.horizontalLayout.addWidget(self.labelVoice)

        self.horizontalSpacer_2 = QSpacerItem(442, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.comboBoxVoice = QComboBox(self.frame_2)
        self.comboBoxVoice.setObjectName(u"comboBoxVoice")

        self.horizontalLayout.addWidget(self.comboBoxVoice)


        self.verticalLayout_3.addWidget(self.frame_2)

        self.frame_6 = QFrame(self.selectorVOICE)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_8 = QHBoxLayout(self.frame_6)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_4 = QLabel(self.frame_6)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_8.addWidget(self.label_4)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_6)

        self.langModels = QComboBox(self.frame_6)
        self.langModels.setObjectName(u"langModels")

        self.horizontalLayout_8.addWidget(self.langModels)


        self.verticalLayout_3.addWidget(self.frame_6)

        self.widget_3 = QWidget(self.selectorVOICE)
        self.widget_3.setObjectName(u"widget_3")
        self.horizontalLayout_10 = QHBoxLayout(self.widget_3)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(0, -1, 0, -1)
        self.frame_7 = QFrame(self.widget_3)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_7.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.frame_7)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.widget_2 = QWidget(self.frame_7)
        self.widget_2.setObjectName(u"widget_2")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy)
        self.verticalLayout_7 = QVBoxLayout(self.widget_2)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.frame_15 = QFrame(self.widget_2)
        self.frame_15.setObjectName(u"frame_15")
        self.frame_15.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_15.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_9 = QVBoxLayout(self.frame_15)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.stopStatus = QLabel(self.frame_15)
        self.stopStatus.setObjectName(u"stopStatus")

        self.verticalLayout_9.addWidget(self.stopStatus)

        self.appCount = QLabel(self.frame_15)
        self.appCount.setObjectName(u"appCount")

        self.verticalLayout_9.addWidget(self.appCount)

        self.appConfirmCount = QLabel(self.frame_15)
        self.appConfirmCount.setObjectName(u"appConfirmCount")

        self.verticalLayout_9.addWidget(self.appConfirmCount)

        self.infoStatus = QLabel(self.frame_15)
        self.infoStatus.setObjectName(u"infoStatus")

        self.verticalLayout_9.addWidget(self.infoStatus)


        self.verticalLayout_7.addWidget(self.frame_15)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_7.addItem(self.verticalSpacer)

        self.checkAppButton = QPushButton(self.widget_2)
        self.checkAppButton.setObjectName(u"checkAppButton")

        self.verticalLayout_7.addWidget(self.checkAppButton)

        self.widget_7 = QWidget(self.widget_2)
        self.widget_7.setObjectName(u"widget_7")
        self.horizontalLayout_14 = QHBoxLayout(self.widget_7)
        self.horizontalLayout_14.setSpacing(0)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.horizontalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.reloadAppButton = QPushButton(self.widget_7)
        self.reloadAppButton.setObjectName(u"reloadAppButton")

        self.horizontalLayout_14.addWidget(self.reloadAppButton)

        self.appConfigureButton = QPushButton(self.widget_7)
        self.appConfigureButton.setObjectName(u"appConfigureButton")

        self.horizontalLayout_14.addWidget(self.appConfigureButton)


        self.verticalLayout_7.addWidget(self.widget_7)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)

        self.verticalLayout_7.addItem(self.verticalSpacer_2)

        self.stopButton = QPushButton(self.widget_2)
        self.stopButton.setObjectName(u"stopButton")

        self.verticalLayout_7.addWidget(self.stopButton)

        self.updateModelButton = QPushButton(self.widget_2)
        self.updateModelButton.setObjectName(u"updateModelButton")
        self.updateModelButton.setAutoDefault(False)

        self.verticalLayout_7.addWidget(self.updateModelButton)

        self.widget = QWidget(self.widget_2)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout_5 = QHBoxLayout(self.widget)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.hideButton = QPushButton(self.widget)
        self.hideButton.setObjectName(u"hideButton")

        self.horizontalLayout_5.addWidget(self.hideButton)

        self.closeButton = QPushButton(self.widget)
        self.closeButton.setObjectName(u"closeButton")

        self.horizontalLayout_5.addWidget(self.closeButton)


        self.verticalLayout_7.addWidget(self.widget)


        self.verticalLayout_6.addWidget(self.widget_2)


        self.horizontalLayout_10.addWidget(self.frame_7)

        self.frame_8 = QFrame(self.widget_3)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_8.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_11 = QHBoxLayout(self.frame_8)
        self.horizontalLayout_11.setSpacing(0)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.widget_6 = QWidget(self.frame_8)
        self.widget_6.setObjectName(u"widget_6")
        self.verticalLayout_8 = QVBoxLayout(self.widget_6)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(9, 0, 9, 0)
        self.frame_13 = QFrame(self.widget_6)
        self.frame_13.setObjectName(u"frame_13")
        self.frame_13.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_13.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_18 = QHBoxLayout(self.frame_13)
        self.horizontalLayout_18.setSpacing(0)
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.horizontalLayout_18.setContentsMargins(0, 0, 0, 0)
        self.label_7 = QLabel(self.frame_13)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_18.addWidget(self.label_7)


        self.verticalLayout_8.addWidget(self.frame_13)

        self.frame_14 = QFrame(self.widget_6)
        self.frame_14.setObjectName(u"frame_14")
        self.frame_14.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_14.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_15 = QHBoxLayout(self.frame_14)
        self.horizontalLayout_15.setSpacing(0)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.horizontalLayout_15.setContentsMargins(0, 6, 0, 6)
        self.protectSlider = QSlider(self.frame_14)
        self.protectSlider.setObjectName(u"protectSlider")
        self.protectSlider.setOrientation(Qt.Orientation.Vertical)

        self.horizontalLayout_15.addWidget(self.protectSlider)


        self.verticalLayout_8.addWidget(self.frame_14)

        self.frame_17 = QFrame(self.widget_6)
        self.frame_17.setObjectName(u"frame_17")
        self.frame_17.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_17.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_9 = QHBoxLayout(self.frame_17)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.protectCount = QLabel(self.frame_17)
        self.protectCount.setObjectName(u"protectCount")
        self.protectCount.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_9.addWidget(self.protectCount)


        self.verticalLayout_8.addWidget(self.frame_17)


        self.horizontalLayout_11.addWidget(self.widget_6)

        self.widget_5 = QWidget(self.frame_8)
        self.widget_5.setObjectName(u"widget_5")
        self.verticalLayout_4 = QVBoxLayout(self.widget_5)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(9, 0, 9, 0)
        self.frame_9 = QFrame(self.widget_5)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_9.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_17 = QHBoxLayout(self.frame_9)
        self.horizontalLayout_17.setSpacing(0)
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.horizontalLayout_17.setContentsMargins(0, 0, 0, 0)
        self.label_6 = QLabel(self.frame_9)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_17.addWidget(self.label_6)


        self.verticalLayout_4.addWidget(self.frame_9)

        self.frame_10 = QFrame(self.widget_5)
        self.frame_10.setObjectName(u"frame_10")
        self.frame_10.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_10.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_12 = QHBoxLayout(self.frame_10)
        self.horizontalLayout_12.setSpacing(0)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(0, 6, 0, 6)
        self.speedSlider = QSlider(self.frame_10)
        self.speedSlider.setObjectName(u"speedSlider")
        self.speedSlider.setOrientation(Qt.Orientation.Vertical)

        self.horizontalLayout_12.addWidget(self.speedSlider)


        self.verticalLayout_4.addWidget(self.frame_10)

        self.frame_3 = QFrame(self.widget_5)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.speedCount = QLabel(self.frame_3)
        self.speedCount.setObjectName(u"speedCount")
        self.speedCount.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_4.addWidget(self.speedCount)


        self.verticalLayout_4.addWidget(self.frame_3)


        self.horizontalLayout_11.addWidget(self.widget_5)

        self.widget_4 = QWidget(self.frame_8)
        self.widget_4.setObjectName(u"widget_4")
        self.verticalLayout_5 = QVBoxLayout(self.widget_4)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(9, 0, 9, 0)
        self.frame_11 = QFrame(self.widget_4)
        self.frame_11.setObjectName(u"frame_11")
        self.frame_11.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_11.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_16 = QHBoxLayout(self.frame_11)
        self.horizontalLayout_16.setSpacing(0)
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.horizontalLayout_16.setContentsMargins(0, 0, 0, 0)
        self.label_5 = QLabel(self.frame_11)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_16.addWidget(self.label_5)


        self.verticalLayout_5.addWidget(self.frame_11)

        self.frame_12 = QFrame(self.widget_4)
        self.frame_12.setObjectName(u"frame_12")
        self.frame_12.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_12.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_13 = QHBoxLayout(self.frame_12)
        self.horizontalLayout_13.setSpacing(0)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalLayout_13.setContentsMargins(0, 6, 0, 6)
        self.tempSlider = QSlider(self.frame_12)
        self.tempSlider.setObjectName(u"tempSlider")
        self.tempSlider.setOrientation(Qt.Orientation.Vertical)

        self.horizontalLayout_13.addWidget(self.tempSlider)


        self.verticalLayout_5.addWidget(self.frame_12)

        self.frame_16 = QFrame(self.widget_4)
        self.frame_16.setObjectName(u"frame_16")
        self.frame_16.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_16.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.frame_16)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.tempCount = QLabel(self.frame_16)
        self.tempCount.setObjectName(u"tempCount")
        self.tempCount.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_6.addWidget(self.tempCount)


        self.verticalLayout_5.addWidget(self.frame_16)


        self.horizontalLayout_11.addWidget(self.widget_4)


        self.horizontalLayout_10.addWidget(self.frame_8)


        self.verticalLayout_3.addWidget(self.widget_3)

        self.frame_4 = QFrame(self.selectorVOICE)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.frame_4)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label = QLabel(self.frame_4)
        self.label.setObjectName(u"label")

        self.horizontalLayout_7.addWidget(self.label)

        self.typeLabel = QLabel(self.frame_4)
        self.typeLabel.setObjectName(u"typeLabel")

        self.horizontalLayout_7.addWidget(self.typeLabel)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_4)

        self.labelActiveVoice = QLabel(self.frame_4)
        self.labelActiveVoice.setObjectName(u"labelActiveVoice")

        self.horizontalLayout_7.addWidget(self.labelActiveVoice)

        self.modelLabel = QLabel(self.frame_4)
        self.modelLabel.setObjectName(u"modelLabel")

        self.horizontalLayout_7.addWidget(self.modelLabel)


        self.verticalLayout_3.addWidget(self.frame_4)


        self.verticalLayout_2.addWidget(self.selectorVOICE)


        self.verticalLayout.addWidget(self.mainmenu)

        self.infoWidget = QWidget(self.centralwidget)
        self.infoWidget.setObjectName(u"infoWidget")
        self.verticalLayout_10 = QVBoxLayout(self.infoWidget)
        self.verticalLayout_10.setSpacing(0)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.frame_5 = QFrame(self.infoWidget)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_5)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_2 = QLabel(self.frame_5)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_3.addWidget(self.label_2)

        self.label_3 = QLabel(self.frame_5)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_3.addWidget(self.label_3)


        self.verticalLayout_10.addWidget(self.frame_5)


        self.verticalLayout.addWidget(self.infoWidget)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.labelType.setText(QCoreApplication.translate("MainWindow", u"Please select type for assistant", None))
        self.comboBoxType.setItemText(0, QCoreApplication.translate("MainWindow", u"Main - no voice", None))
        self.comboBoxType.setItemText(1, QCoreApplication.translate("MainWindow", u"Prime - voice", None))

        self.labelVoice.setText(QCoreApplication.translate("MainWindow", u"Select voice for model", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Select main lang model", None))
        self.stopStatus.setText(QCoreApplication.translate("MainWindow", u"x", None))
        self.appCount.setText(QCoreApplication.translate("MainWindow", u"App found  - x", None))
        self.appConfirmCount.setText(QCoreApplication.translate("MainWindow", u"Need confirmation - x", None))
        self.infoStatus.setText(QCoreApplication.translate("MainWindow", u"https://github.com/youshika-ypite", None))
        self.checkAppButton.setText(QCoreApplication.translate("MainWindow", u"Check app configuration (0)", None))
        self.reloadAppButton.setText(QCoreApplication.translate("MainWindow", u"Reload Apps", None))
        self.appConfigureButton.setText(QCoreApplication.translate("MainWindow", u"Configurate app", None))
        self.stopButton.setText(QCoreApplication.translate("MainWindow", u"Stop - Start", None))
        self.updateModelButton.setText(QCoreApplication.translate("MainWindow", u"Update voice models", None))
        self.hideButton.setText(QCoreApplication.translate("MainWindow", u"Hide", None))
        self.closeButton.setText(QCoreApplication.translate("MainWindow", u"Close app", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Protect", None))
        self.protectCount.setText(QCoreApplication.translate("MainWindow", u"x", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"V-speed", None))
        self.speedCount.setText(QCoreApplication.translate("MainWindow", u"x", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"V-temp", None))
        self.tempCount.setText(QCoreApplication.translate("MainWindow", u"x", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Active type:", None))
        self.typeLabel.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.labelActiveVoice.setText(QCoreApplication.translate("MainWindow", u"Active model:", None))
        self.modelLabel.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"@youshika--ecosystem. 2024", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"background from artist: @adelie_cat", None))
    # retranslateUi

