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
from PySide6.QtWidgets import (QApplication, QComboBox, QListWidget, QListWidgetItem,
    QMainWindow, QMenuBar, QPushButton, QSizePolicy,
    QTabWidget, QWidget)

class Ui_LauncherMain(object):
    def setupUi(self, LauncherMain):
        if not LauncherMain.objectName():
            LauncherMain.setObjectName(u"LauncherMain")
        LauncherMain.resize(1200, 600)
        LauncherMain.setMinimumSize(QSize(1200, 600))
        LauncherMain.setMaximumSize(QSize(1200, 600))
        font = QFont()
        font.setFamilies([u"Sans Serif"])
        font.setPointSize(11)
        font.setBold(False)
        LauncherMain.setFont(font)
        LauncherMain.setStyleSheet(u"QMainWindow {\n"
"    background-color: #2b2b2b;\n"
"}\n"
"\n"
"QPushButton {\n"
"    background-color: #3c3f41;\n"
"    color: white;\n"
"    border-radius: 6px;\n"
"    padding: 6px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #4b4f52;\n"
"}\n"
"\n"
"#SettingsButton:hover {\n"
"    background-color: #4b4f52;\n"
"}\n"
"\n"
"#LaunchButtonMain {\n"
"    background-color: #3daee9;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"#LaunchButtonMain:hover {\n"
"    background-color: #52b6eb;\n"
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
        self.LaunchButtonMain = QPushButton(self.centralwidget)
        self.LaunchButtonMain.setObjectName(u"LaunchButtonMain")
        self.LaunchButtonMain.setGeometry(QRect(510, 500, 300, 70))
        font1 = QFont()
        font1.setFamilies([u"Sans Serif"])
        font1.setPointSize(25)
        font1.setBold(True)
        self.LaunchButtonMain.setFont(font1)
        self.InstanceList = QListWidget(self.centralwidget)
        QListWidgetItem(self.InstanceList)
        QListWidgetItem(self.InstanceList)
        QListWidgetItem(self.InstanceList)
        QListWidgetItem(self.InstanceList)
        self.InstanceList.setObjectName(u"InstanceList")
        self.InstanceList.setGeometry(QRect(20, 10, 251, 491))
        font2 = QFont()
        font2.setFamilies([u"Sans Serif"])
        font2.setPointSize(16)
        self.InstanceList.setFont(font2)
        self.SettingsButton = QPushButton(self.centralwidget)
        self.SettingsButton.setObjectName(u"SettingsButton")
        self.SettingsButton.setGeometry(QRect(1110, 500, 70, 70))
        font3 = QFont()
        font3.setFamilies([u"Sans Serif"])
        font3.setPointSize(25)
        self.SettingsButton.setFont(font3)
        icon = QIcon()
        icon.addFile(u"src/lcemplauncher/res/img/icons/settings_icon.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.SettingsButton.setIcon(icon)
        self.SettingsButton.setIconSize(QSize(48, 48))
        self.comboBox = QComboBox(self.centralwidget)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setGeometry(QRect(1010, 10, 171, 31))
        font4 = QFont()
        font4.setFamilies([u"Sans Serif"])
        font4.setPointSize(15)
        font4.setBold(False)
        font4.setItalic(False)
        font4.setKerning(True)
        self.comboBox.setFont(font4)
        self.LaunchButtonMain_2 = QPushButton(self.centralwidget)
        self.LaunchButtonMain_2.setObjectName(u"LaunchButtonMain_2")
        self.LaunchButtonMain_2.setGeometry(QRect(20, 509, 251, 61))
        font5 = QFont()
        font5.setFamilies([u"Sans Serif"])
        font5.setPointSize(23)
        font5.setBold(False)
        self.LaunchButtonMain_2.setFont(font5)
        LauncherMain.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(LauncherMain)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1200, 24))
        LauncherMain.setMenuBar(self.menubar)

        self.retranslateUi(LauncherMain)

        QMetaObject.connectSlotsByName(LauncherMain)
    # setupUi

    def retranslateUi(self, LauncherMain):
        LauncherMain.setWindowTitle(QCoreApplication.translate("LauncherMain", u"Legacy Launcher for Linux", None))
        self.LaunchButtonMain.setText(QCoreApplication.translate("LauncherMain", u"Launch", None))

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
        self.comboBox.setItemText(0, QCoreApplication.translate("LauncherMain", u"PalpatineGHG", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("LauncherMain", u"ChrisiGHG", None))

        self.LaunchButtonMain_2.setText(QCoreApplication.translate("LauncherMain", u"New Instance", None))
    # retranslateUi

