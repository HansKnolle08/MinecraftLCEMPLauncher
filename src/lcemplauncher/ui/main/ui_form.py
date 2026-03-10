# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QLabel,
    QLineEdit, QListWidget, QListWidgetItem, QMainWindow,
    QMenuBar, QPushButton, QSizePolicy, QTabWidget,
    QWidget)

class Ui_LauncherMain(object):
    def setupUi(self, LauncherMain):
        if not LauncherMain.objectName():
            LauncherMain.setObjectName(u"LauncherMain")
        LauncherMain.resize(1200, 600)
        LauncherMain.setMinimumSize(QSize(1200, 600))
        LauncherMain.setMaximumSize(QSize(1200, 600))
        font = QFont()
        font.setFamilies([u"Sans Serif"])
        font.setPointSize(10)
        font.setBold(False)
        LauncherMain.setFont(font)
        LauncherMain.setStyleSheet(u"QMainWindow {\n"
"    background-color: #2b2b2b;\n"
"}\n"
"\n"
"QLabel {\n"
"	color: white;\n"
"}\n"
"\n"
"QPushButton {\n"
"    background-color: rgb(20, 150, 8);\n"
"	color: white;\n"
"    font-weight: bold;\n"
"    border-radius: 6px;\n"
"    padding: 6px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"   background-color: rgb(20, 195, 8);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"	background-color: rgb(20, 250, 8);\n"
"}\n"
"\n"
"#DeleteInstanceButton {\n"
"	background-color: rgb(224, 27, 36);\n"
"}\n"
"\n"
"#DeleteInstanceButton:hover {\n"
"	background-color: rgb(242, 99, 99);\n"
"}\n"
"\n"
"#DeleteInstanceButton:pressed {\n"
"	background-color: rgb(255, 120, 120)\n"
"}\n"
"\n"
"QListWidget {\n"
"    background-color: #3c3f41;\n"
"    color: white;\n"
"    border-radius: 6px;\n"
"}\n"
"\n"
"QListWidget::item {\n"
"    padding: 8px;\n"
"}\n"
"\n"
"QListWidget::item:selected {\n"
"    background-color: #4b4f52;\n"
"}\n"
"\n"
"QComboBox {\n"
"    background-color: #3c3f41;\n"
"    color: white;\n"
"    padding: 5px;\n"
""
                        "}\n"
"\n"
"QComboBox QAbstractItemView {\n"
"    background-color: #3c3f41;\n"
"    color: white;\n"
"    selection-background-color: #4b4f52;\n"
"}")
        LauncherMain.setTabShape(QTabWidget.TabShape.Rounded)
        self.centralwidget = QWidget(LauncherMain)
        self.centralwidget.setObjectName(u"centralwidget")
        self.LaunchButton = QPushButton(self.centralwidget)
        self.LaunchButton.setObjectName(u"LaunchButton")
        self.LaunchButton.setGeometry(QRect(300, 510, 320, 60))
        font1 = QFont()
        font1.setFamilies([u"Sans Serif"])
        font1.setPointSize(25)
        font1.setBold(True)
        self.LaunchButton.setFont(font1)
        self.InstanceList = QListWidget(self.centralwidget)
        QListWidgetItem(self.InstanceList)
        QListWidgetItem(self.InstanceList)
        QListWidgetItem(self.InstanceList)
        QListWidgetItem(self.InstanceList)
        self.InstanceList.setObjectName(u"InstanceList")
        self.InstanceList.setGeometry(QRect(20, 10, 251, 490))
        font2 = QFont()
        font2.setFamilies([u"Sans Serif"])
        font2.setPointSize(16)
        self.InstanceList.setFont(font2)
        self.SettingsButton = QPushButton(self.centralwidget)
        self.SettingsButton.setObjectName(u"SettingsButton")
        self.SettingsButton.setGeometry(QRect(1110, 510, 60, 60))
        self.SettingsButton.setFont(font1)
        icon = QIcon()
        icon.addFile(u"src/lcemplauncher/res/img/icons/settings_icon.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.SettingsButton.setIcon(icon)
        self.SettingsButton.setIconSize(QSize(48, 48))
        self.UserSelectBox = QComboBox(self.centralwidget)
        self.UserSelectBox.addItem("")
        self.UserSelectBox.addItem("")
        self.UserSelectBox.setObjectName(u"UserSelectBox")
        self.UserSelectBox.setGeometry(QRect(1000, 10, 170, 30))
        font3 = QFont()
        font3.setFamilies([u"Sans Serif"])
        font3.setPointSize(15)
        font3.setBold(False)
        font3.setItalic(False)
        font3.setKerning(True)
        self.UserSelectBox.setFont(font3)
        self.NewInstanceButton = QPushButton(self.centralwidget)
        self.NewInstanceButton.setObjectName(u"NewInstanceButton")
        self.NewInstanceButton.setGeometry(QRect(20, 510, 250, 60))
        font4 = QFont()
        font4.setFamilies([u"Sans Serif"])
        font4.setPointSize(23)
        font4.setBold(True)
        self.NewInstanceButton.setFont(font4)
        self.InstanceSettingsFrame = QFrame(self.centralwidget)
        self.InstanceSettingsFrame.setObjectName(u"InstanceSettingsFrame")
        self.InstanceSettingsFrame.setEnabled(True)
        self.InstanceSettingsFrame.setGeometry(QRect(300, 10, 320, 490))
        self.InstanceSettingsFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.InstanceSettingsFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.InstanceName = QLabel(self.InstanceSettingsFrame)
        self.InstanceName.setObjectName(u"InstanceName")
        self.InstanceName.setGeometry(QRect(10, 0, 601, 51))
        font5 = QFont()
        font5.setFamilies([u"Sans Serif"])
        font5.setPointSize(25)
        font5.setBold(True)
        font5.setItalic(False)
        font5.setUnderline(True)
        self.InstanceName.setFont(font5)
        self.PlaytimeLabel = QLabel(self.InstanceSettingsFrame)
        self.PlaytimeLabel.setObjectName(u"PlaytimeLabel")
        self.PlaytimeLabel.setGeometry(QRect(10, 60, 271, 21))
        font6 = QFont()
        font6.setFamilies([u"Sans Serif"])
        font6.setPointSize(14)
        self.PlaytimeLabel.setFont(font6)
        self.DeleteInstanceButton = QPushButton(self.InstanceSettingsFrame)
        self.DeleteInstanceButton.setObjectName(u"DeleteInstanceButton")
        self.DeleteInstanceButton.setEnabled(True)
        self.DeleteInstanceButton.setGeometry(QRect(10, 450, 131, 31))
        self.DeleteInstanceButton.setAutoDefault(False)
        self.DeleteInstanceButton.setFlat(False)
        self.OpenFolderButton = QPushButton(self.InstanceSettingsFrame)
        self.OpenFolderButton.setObjectName(u"OpenFolderButton")
        self.OpenFolderButton.setGeometry(QRect(180, 450, 131, 31))
        self.OpenFolderButton.setAutoDefault(False)
        self.ProtonSelectBox = QComboBox(self.InstanceSettingsFrame)
        self.ProtonSelectBox.addItem("")
        self.ProtonSelectBox.addItem("")
        self.ProtonSelectBox.setObjectName(u"ProtonSelectBox")
        self.ProtonSelectBox.setGeometry(QRect(10, 170, 200, 30))
        self.ProtonSelectBox.setFont(font3)
        self.ProtonLabel = QLabel(self.InstanceSettingsFrame)
        self.ProtonLabel.setObjectName(u"ProtonLabel")
        self.ProtonLabel.setGeometry(QRect(10, 130, 140, 40))
        self.ProtonLabel.setFont(font6)
        self.IPAddress = QLabel(self.InstanceSettingsFrame)
        self.IPAddress.setObjectName(u"IPAddress")
        self.IPAddress.setGeometry(QRect(10, 220, 140, 40))
        self.IPAddress.setFont(font6)
        self.IPAddressInput = QLineEdit(self.InstanceSettingsFrame)
        self.IPAddressInput.setObjectName(u"IPAddressInput")
        self.IPAddressInput.setGeometry(QRect(10, 270, 200, 30))
        LauncherMain.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(LauncherMain)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1200, 24))
        LauncherMain.setMenuBar(self.menubar)

        self.retranslateUi(LauncherMain)

        self.DeleteInstanceButton.setDefault(False)


        QMetaObject.connectSlotsByName(LauncherMain)
    # setupUi

    def retranslateUi(self, LauncherMain):
        LauncherMain.setWindowTitle(QCoreApplication.translate("LauncherMain", u"Legacy Launcher for Linux", None))
        self.LaunchButton.setText(QCoreApplication.translate("LauncherMain", u"Launch Instance", None))

        __sortingEnabled = self.InstanceList.isSortingEnabled()
        self.InstanceList.setSortingEnabled(False)
        ___qlistwidgetitem = self.InstanceList.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("LauncherMain", u"LCEMP 1.0.3", None));
        ___qlistwidgetitem1 = self.InstanceList.item(1)
        ___qlistwidgetitem1.setText(QCoreApplication.translate("LauncherMain", u"LCEMP 1.0.2", None));
        ___qlistwidgetitem2 = self.InstanceList.item(2)
        ___qlistwidgetitem2.setText(QCoreApplication.translate("LauncherMain", u"Development", None));
        ___qlistwidgetitem3 = self.InstanceList.item(3)
        ___qlistwidgetitem3.setText(QCoreApplication.translate("LauncherMain", u"TestWorld", None));
        self.InstanceList.setSortingEnabled(__sortingEnabled)

        self.SettingsButton.setText("")
        self.UserSelectBox.setItemText(0, QCoreApplication.translate("LauncherMain", u"PalpatineGHG", None))
        self.UserSelectBox.setItemText(1, QCoreApplication.translate("LauncherMain", u"ChrisiGHG", None))

        self.NewInstanceButton.setText(QCoreApplication.translate("LauncherMain", u"New Instance", None))
        self.InstanceName.setText(QCoreApplication.translate("LauncherMain", u"LCEMP 1.0.3", None))
        self.PlaytimeLabel.setText(QCoreApplication.translate("LauncherMain", u"Playtime: 0d 0h 0m", None))
        self.DeleteInstanceButton.setText(QCoreApplication.translate("LauncherMain", u"Delete Instance", None))
        self.OpenFolderButton.setText(QCoreApplication.translate("LauncherMain", u"Open Folder", None))
        self.ProtonSelectBox.setItemText(0, QCoreApplication.translate("LauncherMain", u"GE-Proton 8-21", None))
        self.ProtonSelectBox.setItemText(1, QCoreApplication.translate("LauncherMain", u"GE-Proton 10-32", None))

        self.ProtonLabel.setText(QCoreApplication.translate("LauncherMain", u"Proton Version:", None))
        self.IPAddress.setText(QCoreApplication.translate("LauncherMain", u"IP Address", None))
    # retranslateUi

