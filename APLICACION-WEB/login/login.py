import sys
from PyQt5.QtCore import Qt, QTranslator, QLocale, QRect
from PyQt5.QtGui import QIcon, QPixmap, QColor
from PyQt5.QtWidgets import QApplication, QAction, QMenu
from qfluentwidgets import (
    Action, RoundMenu, setThemeColor, FluentTranslator, setTheme, Theme, 
    SplitTitleBar, isDarkTheme, SplitPushButton, FluentIcon, BodyLabel, 
    CheckBox, HyperlinkButton, LineEdit, PrimaryPushButton, PasswordLineEdit
)
from PyQt5 import QtCore, QtGui, QtWidgets
import resource_rc

def isWin11():
    return sys.platform == 'win32' and sys.getwindowsversion().build >= 22000

if isWin11():
    from qframelesswindow import AcrylicWindow as Window
else:
    from qframelesswindow import FramelessWindow as Window

class LoginWindow(Window):

    def __init__(self):
        super().__init__()
        self.setupUi()
        setTheme(Theme.LIGHT)
        setThemeColor('#023059')
        self.setTitleBar(SplitTitleBar(self))
        self.titleBar.raise_()

        self.label.setScaledContents(False)
        self.setWindowTitle('GESTOR BD PETROJUNIN')
        self.setWindowIcon(QIcon(":/images/pdvsalogo.png"))
        self.resize(1000, 650)

        self.windowEffect.setMicaEffect(self.winId(), isDarkMode=isDarkTheme())
        if not isWin11():
            color = QColor(25, 33, 42) if isDarkTheme() else QColor(240, 244, 249)
            self.setStyleSheet(f"LoginWindow{{background: {color.name()}}}")

        if sys.platform == "darwin":
            self.setSystemTitleBarButtonVisible(True)
            self.titleBar.minBtn.hide()
            self.titleBar.maxBtn.hide()
            self.titleBar.closeBtn.hide()

        self.titleBar.titleLabel.setStyleSheet("""
            QLabel{
                background: transparent;
                font: 13px 'Segoe UI';
                padding: 0 4px;
                color: white
            }
        """)

        self.widget.setStyleSheet("""
            QWidget {
                background-color: #172763;
                border-radius: 10px;
                padding: 10px;
            }
            QLabel {
                font: 13px 'Microsoft YaHei';
            }
        """)

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)

    def setupUi(self):
        self.setObjectName("Form")
        self.resize(1250, 809)
        self.setMinimumSize(QtCore.QSize(700, 500))
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self)
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/images/login.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.widget = QtWidgets.QWidget(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setMinimumSize(QtCore.QSize(360, 0))
        self.widget.setMaximumSize(QtCore.QSize(360, 16777215))
        self.widget.setStyleSheet("""
            QLabel {
                font: 13px 'Microsoft YaHei';
            }
        """)
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setContentsMargins(20, 20, 20, 20)
        self.verticalLayout_2.setSpacing(9)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMinimumSize(QtCore.QSize(100, 100))
        self.label_2.setMaximumSize(QtCore.QSize(100, 100))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap(":/images/pdvsalogogrande.png"))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2, 0, QtCore.Qt.AlignHCenter)
        spacerItem1 = QtWidgets.QSpacerItem(20, 15, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_2.addItem(spacerItem1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setHorizontalSpacing(4)
        self.gridLayout.setVerticalSpacing(9)
        self.gridLayout.setObjectName("gridLayout")
        self.label_3 = BodyLabel(self.widget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)
        self.gridLayout.setColumnStretch(0, 2)
        self.gridLayout.setColumnStretch(1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)

        self.splitpushbutton = SplitPushButton(self.tr("selecciona tu usuario                             "), self.widget, FluentIcon.PEOPLE)
        self.splitpushbutton.setFlyout(self.createStandMenu(self.splitpushbutton))
        self.verticalLayout_2.addWidget(self.splitpushbutton)

        self.label_6 = BodyLabel(self.widget)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_2.addWidget(self.label_6)

        self.passwordLineEdit = PasswordLineEdit(self.widget)
        self.passwordLineEdit.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_2.addWidget(self.passwordLineEdit)

        spacerItem2 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_2.addItem(spacerItem2)
        self.checkBox = CheckBox(self.widget)
        self.checkBox.setChecked(True)
        self.checkBox.setObjectName("checkBox")
        self.verticalLayout_2.addWidget(self.checkBox)
        spacerItem3 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_2.addItem(spacerItem3)
        self.pushButton = PrimaryPushButton(self.widget)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_2.addWidget(self.pushButton)
        spacerItem4 = QtWidgets.QSpacerItem(20, 6, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_2.addItem(spacerItem4)
        self.pushButton_2 = HyperlinkButton(self.widget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout_2.addWidget(self.pushButton_2)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem5)
        self.horizontalLayout.addWidget(self.widget)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def createStandMenu(self, button):
        menu = RoundMenu(parent=self.widget)
        menu.addActions([
            Action(self.tr("Marielys"), triggered=lambda c, b=button: b.setText(self.tr("Marielys                                                 "))),
            Action(self.tr("Luis"), triggered=lambda c, b=button: b.setText(self.tr("Luis                                                         ")))
        ])
        return menu

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "Form"))
        self.label_3.setText(_translate("Form", "usuario"))
        self.label_6.setText(_translate("Form", "contraseña"))
        self.passwordLineEdit.setPlaceholderText(self.tr("ingrese contraseña"))
        self.checkBox.setText(_translate("Form", "mantener sesión iniciada"))
        self.pushButton.setText(_translate("Form", "iniciar sesión"))
        self.pushButton_2.setText(_translate("Form", "olvide contraseña"))

    def resizeEvent(self, e):
        super().resizeEvent(e)
        pixmap = QPixmap(":/images/login.png").scaled(
            self.label.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        self.label.setPixmap(pixmap)

    def systemTitleBarRect(self, size):
        """ Returns the system title bar rect, only works for macOS """
        return QRect(size.width() - 75, 0, 75, size.height())

if __name__ == '__main__':
    # Configuración para la ejecución principal
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    
    # Traducción para internacionalización
    translator = FluentTranslator(QLocale())
    app.installTranslator(translator)

    # Crear y mostrar la ventana de inicio de sesión
    login_window = LoginWindow()
    login_window.show()
    
    # Ejecutar la aplicación
    sys.exit(app.exec_())