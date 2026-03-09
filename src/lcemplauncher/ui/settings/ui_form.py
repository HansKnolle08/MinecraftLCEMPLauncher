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
from PySide6.QtWidgets import (QApplication, QMainWindow, QMenuBar, QSizePolicy,
    QStatusBar, QWidget)

class Ui_SettingsMain(object):
    def setupUi(self, SettingsMain):
        if not SettingsMain.objectName():
            SettingsMain.setObjectName(u"SettingsMain")
        SettingsMain.resize(800, 600)
        self.centralwidget = QWidget(SettingsMain)
        self.centralwidget.setObjectName(u"centralwidget")
        SettingsMain.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(SettingsMain)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 24))
        SettingsMain.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(SettingsMain)
        self.statusbar.setObjectName(u"statusbar")
        SettingsMain.setStatusBar(self.statusbar)

        self.retranslateUi(SettingsMain)

        QMetaObject.connectSlotsByName(SettingsMain)
    # setupUi

    def retranslateUi(self, SettingsMain):
        SettingsMain.setWindowTitle(QCoreApplication.translate("SettingsMain", u"SettingsMain", None))
    # retranslateUi

