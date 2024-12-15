import sys
from PyQt5 import QtWidgets, QtCore
from pruebabackend import ConsolaDBBackend, ConsolaDBFrontend
from qtdesign import Ui_Form
from bd.conexion_bd import base_ddatos

class Main(QtWidgets.QWidget, Ui_Form):

    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Inicializa la interfaz de QtDesign

        # Crear un layout horizontal para la clase Main
        self.main_layout = QtWidgets.QHBoxLayout(self)  # Inicializa el layout aquí
        self.setLayout(self.main_layout)

        # Crear un contenedor para la barra lateral
        self.sidebar = QtWidgets.QWidget()
        self.sidebar_layout = QtWidgets.QVBoxLayout(self.sidebar)

        # Establecer un tamaño mínimo para la barra lateral
        self.sidebar.setMinimumWidth(200)  # Ajusta el ancho mínimo según sea necesario

        # Crear el contenedor para filtrar por valores
        self.filtro_valores_widget = QtWidgets.QGroupBox("Filtrar por valores")
        self.filtro_valores_layout = QtWidgets.QVBoxLayout()
        self.valor_min = QtWidgets.QSpinBox()
        self.valor_min.setRange(500, 20000)
        self.valor_max = QtWidgets.QSpinBox()
        self.valor_max.setRange(500, 20000)
        self.filtrar_valores_button = QtWidgets.QPushButton("Filtrar")
        self.filtrar_valores_button.clicked.connect(self.filtro_por_valores)

        self.filtro_valores_layout.addWidget(QtWidgets.QLabel("Valor mínimo:"))
        self.filtro_valores_layout.addWidget(self.valor_min)
        self.filtro_valores_layout.addWidget(QtWidgets.QLabel("Valor máximo:"))
        self.filtro_valores_layout.addWidget(self.valor_max)
        self.filtro_valores_layout.addWidget(self.filtrar_valores_button)
        self.filtro_valores_widget.setLayout(self.filtro_valores_layout)

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

        # Inicializar la conexión a la base de datos
        self.conexion = ConsolaDBBackend(base_ddatos(), "public", "produccion_c")
        self.frontend = ConsolaDBFrontend(self.conexion)

        # Agregar la barra lateral al layout principal
        self.main_layout.addWidget(self.sidebar)

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

    def filtro_por_valores(self):
        valor_min = self.valor_min.value()
        valor_max = self.valor_max.value()
        if valor_min > valor_max:
            print("El valor mínimo no puede ser mayor que el valor máximo.")
            return
        datos_filtrados = self.conexion.filtrar_por_valores(valor_min, valor_max)
        print(f"Filtrado entre {valor_min} y {valor_max}. Datos:")
        self.mostrar_datos(datos_filtrados)

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
    app = QtWidgets.QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())