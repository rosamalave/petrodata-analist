import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from pruebabackend import ConsolaDBBackend
from bd.conexion_bd import base_ddatos

class Ui_Form(object):
    def __init__(self):
        self.conexion= ConsolaDBBackend(base_ddatos(), "public", "produccion_c")

        
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
        # Configuraciones adicionales de la tabla
        self.tabla.setAlternatingRowColors(True)  # Alternar colores de fila
        self.tabla.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)  # Seleccionar filas completas
        self.tabla.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)  # Desactivar edición de celdas

        # Configuraciones adicionales de la tabla
        self.tabla.setRowCount(0)  # Limpiar filas existentes
        self.tabla.setColumnCount(len(self.conexion.headers))  # Establecer el número de columnas según los headers
        self.tabla.setHorizontalHeaderLabels(self.conexion.headers)  # Establecer los encabezados desde la base de datos

        header = self.tabla.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        
        # Cargar los datos en la tabla
        for fila in self.conexion.datos:
            row_position = self.tabla.rowCount()
            self.tabla.insertRow(row_position)
            for column, value in enumerate(fila):
                item = QtWidgets.QTableWidgetItem(str(value))
                item.setTextAlignment(QtCore.Qt.AlignCenter)  # Alinear texto al centro
                self.tabla.setItem(row_position, column, item)


    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.tabla.setSortingEnabled(True)

 

if __name__ == "__main__":
    # Crear una instancia de QApplication
    app = QtWidgets.QApplication(sys.argv)

    # Crear el contenedor principal de la ventana
    MainWindow = QtWidgets.QWidget()

    # Crear una instancia de la clase Ui_Form
    ui = Ui_Form()

    # Configurar la interfaz para el contenedor principal
    ui.setupUi(MainWindow)


    # Mostrar la ventana principal
    MainWindow.show()

    # Ejecutar el bucle principal de la aplicación
    sys.exit(app.exec_())

