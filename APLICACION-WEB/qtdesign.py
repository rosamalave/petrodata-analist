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

        # Crear un contenedor para el layout principal
        self.main_container = QtWidgets.QWidget(Form)  # Crear un nuevo QWidget
        self.main_layout = QtWidgets.QHBoxLayout(self.main_container)  # Inicializa el layout aquí
        Form.setLayout(self.main_layout)  # Establecer el layout en el contenedor principal

        # Crear un contenedor para la barra lateral
        self.sidebar = QtWidgets.QWidget(Form)  # Asegúrate de crear el widget de la barra lateral aquí
        self.sidebar_layout = QtWidgets.QVBoxLayout(self.sidebar)  # Crear el layout y asignarlo al widget

        # Establecer un tamaño fijo para la barra lateral (20% del ancho total)
        self.sidebar.setFixedWidth(int(Form.width() * 0.20))  # Ajusta el ancho según sea necesario

        # Crear el contenedor para filtrar por valores
        self.filtro_valores_widget = QtWidgets.QGroupBox("Filtrar por valores")
        self.filtro_valores_layout = QtWidgets.QVBoxLayout()

        # Crear un QComboBox para seleccionar la columna a filtrar
        self.columnafiltrar = QtWidgets.QComboBox()
        # Obtener los headers excluyendo 'fecha' e 'id'
        campos_numericos = [header for header in self.conexion.headers if header not in ['fecha', 'id']]
        # Agregar los campos al QComboBox
        self.columnafiltrar.addItems(campos_numericos)

        self.valor_min = QtWidgets.QSpinBox()
        self.valor_min.setRange(0, 20000)
        self.valor_max = QtWidgets.QSpinBox()
        self.valor_max.setRange(0, 20000)

        self.filtrar_valores_button = QtWidgets.QPushButton("Filtrar")
        # Conectar el botón de filtrar a un nuevo método que incluya la columna seleccionada
        self.filtrar_valores_button.clicked.connect(lambda: self.filtro_por_valores(self.columnafiltrar.currentText(), self.valor_min.value(),self.valor_max.value()))

        # Agregar widgets al layout
        self.filtro_valores_layout.addWidget(QtWidgets.QLabel("Seleccionar columna:"))
        self.filtro_valores_layout.addWidget(self.columnafiltrar)
        self.filtro_valores_layout.addWidget(QtWidgets.QLabel("Valor mínimo:"))
        self.filtro_valores_layout.addWidget(self.valor_min)
        self.filtro_valores_layout.addWidget(QtWidgets.QLabel("Valor máximo:"))
        self.filtro_valores_layout.addWidget(self.valor_max)
        self.filtro_valores_layout.addWidget(self.filtrar_valores_button)
        self.filtro_valores_widget.setLayout(self.filtro_valores_layout)

        # Agregar el widget de filtro a la barra lateral
        self.sidebar_layout.addWidget(self.filtro_valores_widget)

        # Crear el contenedor para filtrar por fechas
        self.filtro_fechas_widget = QtWidgets.QGroupBox("Filtrar por fechas")
        self.filtro_fechas_layout = QtWidgets.QVBoxLayout()
        self.fecha_inicio = QtWidgets.QDateEdit()
        self.fecha_inicio.setCalendarPopup(True)
        self.fecha_fin = QtWidgets.QDateEdit()
        self.fecha_fin.setCalendarPopup(True)
        self.filtrar_fechas_button = QtWidgets.QPushButton("Filtrar")
        self.filtrar_fechas_button.clicked.connect(self.filtro_por_fecha)

        self.filtro_fechas_layout.addWidget(QtWidgets.QLabel("Fecha inicio:"))
        self.filtro_fechas_layout.addWidget(self.fecha_inicio)
        self.filtro_fechas_layout.addWidget(QtWidgets.QLabel("Fecha fin:"))
        self.filtro_fechas_layout.addWidget(self.fecha_fin)
        self.filtro_fechas_layout.addWidget(self.filtrar_fechas_button)
        self.filtro_fechas_widget.setLayout(self.filtro_fechas_layout)

        # Agregar los widgets de filtro a la barra lateral
        self.sidebar_layout.addWidget(self.filtro_valores_widget)
        self.sidebar_layout.addWidget(self.filtro_fechas_widget)

        # Conectar el botón de agregar fila
        self.aggfila = QtWidgets.QPushButton("Agregar fila")
        self.aggfila.clicked.connect(self.agregar_fila)
        self.sidebar_layout.addWidget(self.aggfila)

        # Conectar el botón de editar fila
        self.editar_fila_button = QtWidgets.QPushButton("Editar fila")
        self.editar_fila_button.clicked.connect(self.editar_fila)
        self.sidebar_layout.addWidget(self.editar_fila_button)

        # Botón para guardar cambios
        self.guardar_button = QtWidgets.QPushButton("Guardar cambios")
        self.guardar_button.clicked.connect(self.guardar_cambios)
        self.sidebar_layout.addWidget(self.guardar_button)
        self.guardar_button.setVisible(False)  # Ocultar inicialmente

        # Variable para almacenar el índice de la fila seleccionada
        self.indice_seleccionado = None
        
        # Agregar la barra lateral al layout principal
        self.main_layout.addWidget(self.sidebar)

        # Crear el contenedor para la tabla
        self.contenedortabla = QtWidgets.QWidget(Form)
        self.tabla_layout = QtWidgets.QVBoxLayout(self.contenedortabla)

        # Configuración de la tabla
        self.tabla = QtWidgets.QTableWidget(self.contenedortabla)
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
        
        self.cargar_datos(self.conexion.datos)


    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.tabla.setSortingEnabled(True)


    def obtener_indice(self, index):
        return index

    def cargar_datos(self,datos):
        self.tabla.setRowCount(0)
                # Cargar los datos en la tabla
        for fila in datos:
            row_position = self.tabla.rowCount()
            self.tabla.insertRow(row_position)
            for column, value in enumerate(fila):
                item = QtWidgets.QTableWidgetItem(str(value))
                item.setTextAlignment(QtCore.Qt.AlignCenter)  # Alinear texto al centro
                self.tabla.setItem(row_position, column, item)

        # Agregar la tabla al layout del contenedor de la tabla
        self.tabla_layout.addWidget(self.tabla)

        # Agregar el contenedor de la tabla al layout principal
        self.main_layout.addWidget(self.contenedortabla)
        # Ajustar el tamaño de la barra lateral y la tabla
        self.sidebar.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)  # Fijo en ancho, expandible en alto
        self.contenedortabla.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)  # Expandible en ambos

    def agregar_fila(self):
        self.conexion.agregar_fila()
        print("\nFila vacía agregada.")
        self.cargar_datos()  # Recargar datos después de agregar

    def editar_fila(self):
        self.tabla.setEditTriggers(QtWidgets.QAbstractItemView.EditKeyPressed)  # Activar edición
        self.guardar_button.setVisible(True)  # Mostrar botón de guardar
        self.editar_fila_button.setVisible(False)  # Ocultar botón de editar

        # Obtener el índice de la fila seleccionada
        self.indice_seleccionado = self.tabla.currentRow()
        if self.indice_seleccionado != -1:
            self.tabla.selectRow(self.indice_seleccionado)  # Seleccionar la fila

    def guardar_cambios(self):
        self.tabla.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)  # Desactivar edición
        self.guardar_button.setVisible(False)  # Ocultar botón de guardar
        self.editar_fila_button.setVisible(True)  # Mostrar botón de editar

        # Guardar cambios en la fila seleccionada
        if self.indice_seleccionado is not None:
            cambios = {}
            for column in range(self.tabla.columnCount()):
                nuevo_valor = self.tabla.item(self.indice_seleccionado, column).text()
                cambios[column] = nuevo_valor
            self.conexion.editar_fila(self.indice_seleccionado, cambios)
            print(f"Cambios guardados en la fila {self.indice_seleccionado}.")
            self.cargar_datos()  # Recargar datos después de guardar

    def filtro_por_valores(self, header, valor_min, valor_max):

        datos_filtrados = self.conexion.filtrar_por_valores(header,valor_min,valor_max)
        print(f"Filtrado entre {valor_min} y {valor_max}. Datos:")
        self.cargar_datos(datos_filtrados)

    def filtro_por_fecha(self):
        fecha_inicio = self.fecha_inicio.date().toString("yyyy-MM-dd")
        fecha_fin = self.fecha_fin.date().toString("yyyy-MM-dd")
        if fecha_inicio > fecha_fin:
            print("La fecha de inicio no puede ser mayor que la fecha final.")
            return
        datos_filtrados = self.conexion.filtrar_por_fecha(fecha_inicio, fecha_fin)
        print(f"Filtrado entre {fecha_inicio} y {fecha_fin}. Datos:")
        self.mostrar_datos(datos_filtrados)

    def mostrar_datos(self, datos):
        self.tabla.setRowCount(0)  # Limpiar la tabla
        for fila in datos:
            row_position = self.tabla.rowCount()
            self.tabla.insertRow(row_position)
            for column, value in enumerate(fila):
                self.tabla.setItem(row_position, column, QtWidgets.QTableWidgetItem(str(value)))

    def salir(self):
        print("Saliendo del programa.")
        sys.exit()



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

