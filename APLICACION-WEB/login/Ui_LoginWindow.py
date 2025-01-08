from PyQt5 import QtCore, QtGui, QtWidgets
from qfluentwidgets import BodyLabel, CheckBox, HyperlinkButton, LineEdit, PrimaryPushButton, SplitPushButton, FluentIcon, RoundMenu, Action, PasswordLineEdit
import resource_rc

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1250, 809)
        Form.setMinimumSize(QtCore.QSize(700, 500))
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Form)
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/images/login.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.widget = QtWidgets.QWidget(Form)
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

        # Reemplazar lineEdit_3 con SplitPushButton
        self.splitpushbutton = SplitPushButton(self.tr("selecciona tu usuario                             "), self.widget, FluentIcon.PEOPLE)
        self.splitpushbutton.setFlyout(self.createStandMenu(self.splitpushbutton))
        self.verticalLayout_2.addWidget(self.splitpushbutton)

        self.label_6 = BodyLabel(self.widget)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_2.addWidget(self.label_6)

        # Reemplazo de lineEdit_4 con PasswordLineEdit
        self.passwordLineEdit = PasswordLineEdit(self.widget)
        self.passwordLineEdit.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)  # Adaptable al ancho
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

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def createStandMenu(self, button):
        menu = RoundMenu(parent=self.widget)
        menu.addActions([
            Action(self.tr("Marielys"), triggered=lambda c, b=button: b.setText(self.tr("Marielys                                                 "))),
            Action(self.tr("Luis"), triggered=lambda c, b=button: b.setText(self.tr("Luis                                                         ")))
        ])
        return menu

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_3.setText(_translate("Form", "usuario"))
        self.label_6.setText(_translate("Form", "contraseña"))
        self.passwordLineEdit.setPlaceholderText(self.tr("ingrese contraseña"))
        self.checkBox.setText(_translate("Form", "mantener sesión iniciada"))
        self.pushButton.setText(_translate("Form", "iniciar sesión"))
        self.pushButton_2.setText(_translate("Form", "olvide contraseña"))