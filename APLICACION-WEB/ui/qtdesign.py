from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1366, 768)  # Resolución estándar de una laptop (puedes ajustar según sea necesario)

        # Espacio reservado para la barra lateral (20% del ancho total)
        barra_lateral_ancho = int(Form.width() * 0.2)
        barra_lateral_alto = Form.height() - 40  # Altura total, menos márgenes

        # Configuración del contenedor de la barra lateral
        self.barra_lateral = QtWidgets.QWidget(Form)
        self.barra_lateral.setGeometry(
            QtCore.QRect(20, 20, barra_lateral_ancho, barra_lateral_alto)
        )
        self.barra_lateral.setObjectName("barra_lateral")
        self.barra_lateral.setStyleSheet("background-color: #f0f0f0; border-radius: 5px;")

        # Botón para agregar filas
        self.aggfila = QtWidgets.QPushButton(self.barra_lateral)
        self.aggfila.setGeometry(
            QtCore.QRect(
                int(barra_lateral_ancho * 0.2),  # Centrado horizontalmente (20% del ancho total como margen)
                50,  # Posición vertical inicial (puedes ajustar según quieras)
                int(barra_lateral_ancho * 0.6),  # Ancho del botón (60% del ancho de la barra lateral)
                40,  # Altura del botón
            )
        )
        self.aggfila.setObjectName("agregar_fila")
        self.aggfila.setStyleSheet("""
            QPushButton {
                font-size: 14px;
                background-color: #4caf50;
                color: white;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

        # Configuración del contenedor para la tabla
        tabla_ancho = Form.width() - barra_lateral_ancho - 40  # Ajustando espacio total menos márgenes
        tabla_alto = Form.height() - 40  # Ajustando espacio vertical menos márgenes

        self.contenedortabla = QtWidgets.QWidget(Form)
        self.contenedortabla.setGeometry(
            QtCore.QRect(barra_lateral_ancho + 40, 20, tabla_ancho, tabla_alto)
        )
        self.contenedortabla.setObjectName("contenedortabla")

        # Configuración de la tabla
        self.tabla = QtWidgets.QTableWidget(self.contenedortabla)
        self.tabla.setGeometry(QtCore.QRect(0, 0, tabla_ancho, tabla_alto))
        self.tabla.setObjectName("tabla")
        self.tabla.setColumnCount(8)  # Configura el número de columnas
        self.tabla.setRowCount(20)  # Número inicial de filas
        self.tabla.setShowGrid(False)  # Sin grid para estilo limpio
        self.tabla.setAlternatingRowColors(True)  # Colores alternos en las filas

        # Estilo general
        self.tabla.setStyleSheet("""
            QTableWidget {
                font-size: 14px;
                border: none;
            }
            QTableWidget::item {
                border-bottom: 1px solid rgba(200, 200, 200, 0.7);
            }
            QHeaderView::section {
                background-color: #f4f4f4;
                border: 1px solid #dcdcdc;
                font-weight: bold;
                padding: 6px;
            }
        """)

        # Encabezados horizontales
        encabezados = ["ID", "SHIPIFY", "DATE", "STATUS", "CUSTOMER", "EMAIL", "COUNTRY", "ORDER TYPE"]
        self.tabla.setHorizontalHeaderLabels(encabezados)
        self.tabla.horizontalHeader().setStretchLastSection(True)
        self.tabla.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        # Oculta el encabezado vertical
        self.tabla.verticalHeader().setVisible(False)

        # Ajusta el tamaño predeterminado de las filas
        self.tabla.verticalHeader().setDefaultSectionSize(40)

        # Configuración de selección
        self.tabla.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        self.tabla.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)

        # Añadir barra de desplazamiento
        self.tabla.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.tabla.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.tabla.setSortingEnabled(True)
