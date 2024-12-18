import sys
import datetime
from collections import defaultdict
from PyQt5 import QtCore, QtGui, QtWidgets 
from PyQt5.QtCore import QDate
from pruebabackend import ConsolaDBBackend
from bd.conexion_bd import base_ddatos

class Ui_Form(object):
    def __init__(self):
        self.conexion= ConsolaDBBackend(base_ddatos(), "public", "produccion_c")
        self.en_modo_edicion = False 
        self.backupfilas = []  # Lista para almacenar el estado de las filas
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

        self.controles_paginacion = ControlesPaginacionYPeriodicidad(self, Form)
        self.sidebar_layout.addWidget(self.controles_paginacion)

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
        # Establecer la fecha mínima y máxima
        fecha_minima = QDate(2013, 1, 1)  # Cambia esto a la fecha mínima que desees
        fecha_maxima = QDate.currentDate()  # Por ejemplo, la fecha actual
        self.fecha_inicio.setMinimumDate(fecha_minima)
        self.fecha_inicio.setMaximumDate(fecha_maxima)
        self.fecha_fin.setMinimumDate(fecha_minima)
        self.fecha_fin.setMaximumDate(fecha_maxima)
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


        self.eliminar_fila_button = QtWidgets.QPushButton("Eliminar fila")
        self.eliminar_fila_button.clicked.connect(self.eliminar_fila)
        self.sidebar_layout.addWidget(self.eliminar_fila_button)


                # Botón para deshacer cambios
        self.deshacer_button = QtWidgets.QPushButton("Deshacer")
        self.deshacer_button.clicked.connect(self.deshacer_cambios)
        self.sidebar_layout.addWidget(self.deshacer_button)

        # Variable para almacenar el índice de la fila seleccionada
        self.indice_seleccionado = -1
        
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
            QTableWidget::item:selected {
                background-color: #007BFF;  /* Color de fondo azul */
                color: white;  /* Color de texto blanco */
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
        #configurando el dobleclick para obtener indice de la fila dobleclicada
        self.tabla.itemDoubleClicked.connect(self.dobleclick)
        self.cargar_datos(self.conexion.datos)
        self.reiniciar_interfaz()

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.tabla.setSortingEnabled(True)

    def dobleclick(self, item):
        if not self.en_modo_edicion:
            # Si no estamos en modo de edición, activamos los botones de editar y eliminar
            self.indice_seleccionado = item.row()  # Obtener el índice de la fila seleccionada
            self.tabla.selectRow(self.indice_seleccionado)  # Seleccionar la fila completa
            print(f"Fila seleccionada: {self.indice_seleccionado}")
            fila_actual = tuple(self.tabla.item(self.indice_seleccionado, column).text() for column in range(self.tabla.columnCount()))
            self.backupfilas.append(fila_actual)  # Almacenar en la lista de backup
            self.editar_fila_button.setVisible(True)
            self.eliminar_fila_button.setVisible(True)
            self.aggfila.setVisible(False)  # Ocultar el botón "Agregar fila"
        else:
            # Si estamos en modo de edición, permitimos la edición de la celda
            self.tabla.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked)  # Permitir edición al hacer doble clic

    def deshacer_cambios(self):
        if self.backupfilas:
            # Obtener el estado anterior de la fila
            fila_anterior = self.backupfilas.pop()  # Obtener la última tupla guardada
            for column, valor in enumerate(fila_anterior):
                item = QtWidgets.QTableWidgetItem(str(valor))
                self.tabla.setItem(self.indice_seleccionado, column, item)  # Restaurar el valor en la tabla
            print(f"Deshacer cambios en la fila {self.indice_seleccionado}.")
        self.reiniciar_interfaz()

    def eliminar_fila(self):
        self.indice_seleccionado=self.tabla.currentRow()
        if self.indice_seleccionado != -1:
            try:
                self.conexion.eliminar_fila(self.indice_seleccionado)  # Llamada al método del backend
                print("Fila eliminada.")
            except (IndexError, ValueError) as e:
                print(f"Error: {e}")
        self.reiniciar_interfaz()
        self.cargar_datos(self.conexion.datos)
        
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

    def reiniciar_interfaz(self):
        # Ocultar botones de edición y eliminación
        self.editar_fila_button.setVisible(False)  # Ocultar botón de editar fila
        self.eliminar_fila_button.setVisible(False)  # Ocultar botón de eliminar fila
        self.guardar_button.setVisible(False)  # Ocultar botón de guardar
        self.aggfila.setVisible(True)  # Hacer visible el botón de agregar fila
        self.deshacer_button.setVisible(False)  # Ocultar inicialmente

        # Restablecer cualquier otro estado que necesites
        self.indice_seleccionado = -1  # Reiniciar el índice seleccionado
        self.tabla.clearSelection()  # Limpiar la selección de la tabla
        self.tabla.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)  # Desactivar edición

    def agregar_fila(self):
        self.conexion.agregar_fila()
        print("\nFila vacía agregada.")
        self.cargar_datos(self.conexion.datos)  # Recargar datos después de agregar
        self.reiniciar_interfaz()

    def editar_fila(self):
        self.en_modo_edicion = True
        self.deshacer_button.setVisible(True)
        self.tabla.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked) 
        self.indice_seleccionado = self.tabla.currentRow()  # Obtener el índice de la fila seleccionada
        if self.indice_seleccionado != -1:
            self.tabla.selectRow(self.indice_seleccionado)  # Seleccionar la fila
            print(f"Fila seleccionada para editar: {self.indice_seleccionado}")

        self.tabla.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked)  # Permitir edición al hacer doble clic
        self.guardar_button.setVisible(True)  # Mostrar botón de guardar
        self.editar_fila_button.setVisible(False)  # Ocultar botón de editar
        self.eliminar_fila_button.setVisible(False) 

    def guardar_cambios(self):
        self.en_modo_edicion = False
        self.tabla.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)  # Desactivar edición
        self.guardar_button.setVisible(False)  # Ocultar botón de guardar
        self.editar_fila_button.setVisible(True)  # Mostrar botón de editar
        try:
            # Obtener el índice de la fila seleccionada
            self.indice_seleccionado = self.tabla.currentRow()
            if self.indice_seleccionado == -1:
                raise ValueError("No se ha seleccionado ninguna fila.")

         # Obtener la fila actual y los cambios realizados
            cambios = {}
            fila_actual = []
            for column in range(self.tabla.columnCount()):
                nuevo_valor = self.tabla.item(self.indice_seleccionado, column).text()
                fila_actual.append(nuevo_valor)
                cambios[column] = nuevo_valor  # Guardar el nuevo valor en el diccionario de cambios

            if self.indice_seleccionado not in self.conexion.nuevas_filas_indices:
                # Llamar al método editar_fila para guardar los cambios en la base de datos
                self.conexion.agregar_datos(self.conexion.editar_fila, self.indice_seleccionado, cambios)

                
            else:
                self.conexion.agregar_datos(self.conexion.insertar_fila, self.indice_seleccionado, cambios)
                self.conexion.nuevas_filas_indices.remove(self.indice_seleccionado)
            print(f"Cambios guardados en la fila {self.indice_seleccionado}.")
            # Recargar datos después de guardar
            self.cargar_datos(self.conexion.datos)

        except (ValueError, IndexError) as e:
            print(f"Error: {e}")
        finally:
            self.reiniciar_interfaz()

    def filtro_por_valores(self, header, valor_min, valor_max):

        datos_filtrados = self.conexion.filtrar_por_valores(header,valor_min,valor_max)
        print(f"Filtrado entre {valor_min} y {valor_max}. Datos:")
        self.cargar_datos(datos_filtrados)

    def filtro_por_fecha(self):
        fecha_inicio = self.fecha_inicio.date().toString("dd-MM-yyyy")
        fecha_fin = self.fecha_fin.date().toString("dd-MM-yyyy")
        datos_filtrados = self.conexion.filtro_por_fecha(fecha_inicio, fecha_fin)
        print(f"Filtrado entre {fecha_inicio} y {fecha_fin}. Datos:")
        self.cargar_datos(datos_filtrados)


    def salir(self):
        print("Saliendo del programa.")
        sys.exit()


class ControlesPaginacionYPeriodicidad(QtWidgets.QWidget):
    def __init__(self, ui_form_instance, parent=None):
        super(ControlesPaginacionYPeriodicidad, self).__init__(parent)
        self.ui= ui_form_instance
        self.conexion= ConsolaDBBackend(base_ddatos(), "public", "produccion_c")
        # Layout para los controles
        self.layout = QtWidgets.QVBoxLayout(self)

        # Crear botón de periodicidad (QComboBox)
        self.etiqueta_periodicidad = QtWidgets.QLabel("Seleccionar periodicidad:")
        self.combo_periodicidad = QtWidgets.QComboBox()
        self.combo_periodicidad.addItems(["Todos", "Anual", "Mensual"])
        self.combo_periodicidad.currentIndexChanged.connect(self.on_periodicidad_change)

        # Crear botón de cantidad (QComboBox)
        self.etiqueta_cantidad = QtWidgets.QLabel("Seleccionar cantidad:")
        self.combo_cantidad = QtWidgets.QComboBox()
        self.combo_cantidad.addItems([str(i) for i in range(10, 101)])  # Predeterminado para anual
        self.combo_cantidad.currentIndexChanged.connect(self.on_cantidad_change)
        # Crear botón de paginación
        self.boton_paginacion = QtWidgets.QPushButton("Paginar")
        self.boton_paginacion.clicked.connect(self.paginar)  # Conectar al método

        # Crear botón para eliminar paginacion
        self.boton_deshacer_paginacion = QtWidgets.QPushButton("Deshacer Paginacion")
        self.boton_deshacer_paginacion.clicked.connect(self.deshacer_paginacion)  # Conectar al método
        self.boton_deshacer_paginacion.setVisible(False)  # Inicialmente oculto

        # Crear controles de paginación
        self.layout_paginacion = QtWidgets.QHBoxLayout()

        # Botones de paginación
        self.boton_2_paginas_menos = QtWidgets.QPushButton("<<")
        self.boton_2_paginas_menos.clicked.connect(self.ir_a_dos_paginas_anterior)

        self.boton_pagina_anterior = QtWidgets.QPushButton("n-1")
        self.boton_pagina_anterior.clicked.connect(self.ir_a_pagina_anterior)

        self.boton_pagina_actual = QtWidgets.QPushButton("n")  # Inicialmente en la página actual
        self.boton_pagina_actual.setEnabled(False)  # Desactivar el botón para que no sea clickeable

        self.boton_pagina_siguiente = QtWidgets.QPushButton("n+1")
        self.boton_pagina_siguiente.clicked.connect(self.ir_a_pagina_siguiente)

        self.boton_2_paginas_mas = QtWidgets.QPushButton(">>")
        self.boton_2_paginas_mas.clicked.connect(self.ir_a_dos_paginas_siguiente)

        # Agregar botones al layout de paginación en el orden especificado
        self.layout_paginacion.addWidget(self.boton_2_paginas_menos)
        self.layout_paginacion.addWidget(self.boton_pagina_anterior)
        self.layout_paginacion.addWidget(self.boton_pagina_actual)
        self.layout_paginacion.addWidget(self.boton_pagina_siguiente)
        self.layout_paginacion.addWidget(self.boton_2_paginas_mas)

        # Agregar el layout de paginación al layout principal
        self.layout.addLayout(self.layout_paginacion)

        # Agregar widgets al layout principal
        self.layout.addWidget(self.etiqueta_periodicidad)
        self.layout.addWidget(self.combo_periodicidad)
        self.layout.addWidget(self.etiqueta_cantidad)
        self.layout.addWidget(self.combo_cantidad)
        self.layout.addLayout(self.layout_paginacion)
        self.layout.addWidget(self.boton_paginacion)
        self.layout.addWidget(self.boton_deshacer_paginacion)

        # Inicializar la página actual
        self.pagina_actual = 1
        self.boton_paginacion_activado = False  # Variable para controlar si se ha activado el botón de paginación
        self.actualizar_botones_paginacion()

    def paginar(self):
        self.boton_paginacion_activado = True
        self.boton_deshacer_paginacion.setVisible(True)  
        tamanos_paginas = self.calcular_paginacion(self.combo_periodicidad.currentText(), int(self.combo_cantidad.currentText()))
    
        # Inicializar el índice de inicio para la página actual
        inicio = 0
    
        # Calcular el índice de inicio para la página actual
        for i in range(self.pagina_actual - 1):
            if i < len(tamanos_paginas):
                inicio += tamanos_paginas[i]  # Sumar el tamaño de las páginas anteriores

        # Obtener el número de filas para la página actual
        if self.pagina_actual - 1 < len(tamanos_paginas):
            fin = inicio + tamanos_paginas[self.pagina_actual - 1]
        else:
            fin = inicio  # Si no hay más páginas, no se debe exceder el rango

        # Slicing de los datos para obtener solo las filas de la página actual
        datos_pagina_actual = self.conexion.datos[inicio:fin]

        # Actualizar la tabla con los datos de la página actual
        self.ui.cargar_datos(datos_pagina_actual)
        self.ui.reiniciar_interfaz()

        # Actualizar los botones de paginación
        self.actualizar_botones_paginacion()

    def actualizar_botones_paginacion(self):
        self.boton_pagina_actual.setText(str(self.pagina_actual))
        self.boton_pagina_siguiente.setText(f"{self.pagina_actual + 1}")

        # Mostrar botones de paginación solo si el botón de paginación ha sido activado y no es "Todos"
        if self.boton_paginacion_activado:
            for i in range(self.layout_paginacion.count()):
                self.layout_paginacion.itemAt(i).widget().setVisible(True)  # Hacer visibles los widgets en el layout
        else:
            for i in range(self.layout_paginacion.count()):
                self.layout_paginacion.itemAt(i).widget().setVisible(False)  # Ocultar los widgets en el layout
        # Ocultar o mostrar botones según la página actual y si se ha activado el botón de paginación
        if self.pagina_actual == 1:
            self.boton_2_paginas_menos.setVisible(False)
            self.boton_pagina_anterior.setVisible(False)
        else:
            self.boton_2_paginas_menos.setVisible(True)
            self.boton_pagina_anterior.setText(f"{self.pagina_actual - 1}")  # Actualizar el texto del botón anterior
            self.boton_pagina_anterior.setVisible(True)

            tamano_paginas = self.calcular_paginacion(self.combo_periodicidad.currentText(), int(self.combo_cantidad.currentText()))
            if self.pagina_actual==len(tamano_paginas):   
                self.boton_pagina_siguiente.setVisible(False)  # Actualizar el texto del botón anterior
                self.boton_2_paginas_mas.setVisible(False)

    def deshacer_paginacion(self):
        # Lógica para cargar todos los datos sin segmentación
        self.boton_paginacion_activado = False  # Desactivar el botón de paginación
        self.boton_deshacer_paginacion.setVisible(False)  # Ocultar el botón de eliminar segmentación
        self.ui.cargar_datos(self.conexion.datos)  # Método para cargar todos los datos
        self.ui.reiniciar_interfaz()
        self.pagina_actual = 1
        self.actualizar_botones_paginacion()

    def ir_a_dos_paginas_anterior(self):
        if self.pagina_actual > 2:
            self.pagina_actual -= 2  # Decrementar la página actual en 2
        elif self.pagina_actual == 2:
            self.pagina_actual = 1  # Si estamos en la segunda página, ir a la primera
        else:
            self.pagina_actual = 1  # No permitir que la página sea menor que 1
        self.paginar()  # Llama al método paginar para actualizar la tabla

    def ir_a_pagina_anterior(self):
        if self.pagina_actual > 1:
            self.pagina_actual -= 1
        self.paginar()    
        self.actualizar_botones_paginacion()

    def ir_a_pagina_siguiente(self):
        self.pagina_actual += 1
        self.paginar()
        self.actualizar_botones_paginacion()

    def ir_a_dos_paginas_siguiente(self):
        tamanos_paginas = self.calcular_paginacion(self.combo_periodicidad.currentText(), int(self.combo_cantidad.currentText()))
    
        if self.pagina_actual < len(tamanos_paginas) - 1:  # Si hay más de una página
            self.pagina_actual += 2  # Incrementar la página actual en 2
        else:
            self.pagina_actual = len(tamanos_paginas)  # Ir a la última página si no hay suficientes páginas
        self.paginar()  # Llama al método paginar para actualizar la tabla
        
    # Métodos vacíos como marcadores de posición para las acciones de los botones
    def on_periodicidad_change(self):
        if self.combo_periodicidad.currentText() == "Anual":
            self.combo_cantidad.clear()
            self.combo_cantidad.addItems(["1", "2", "3", "4"])  # Opciones para anual
        elif self.combo_periodicidad.currentText() == "Mensual":
            self.combo_cantidad.clear()
            self.combo_cantidad.addItems(["1", "2", "3"])  # Opciones para mensual
        elif self.combo_periodicidad.currentText() == "Todos":
            self.combo_cantidad.clear()
            self.combo_cantidad.addItems([str(i) for i in range(10, 101)])  # Números del 10 al 100

    def on_cantidad_change(self):
        pass  # Implementar lógica para el cambio de cantidad

    def calcular_paginacion(self, periodicidad, cantidad):
        """
        Calcula la paginación de los datos según la periodicidad (anual, mensual o todos) y la cantidad de filas por página.

        Args:
            periodicidad (str): La periodicidad para agrupar los datos, "anual", "mensual" o "todos".
            cantidad (int): El número de filas por página (1 a 4 para anual y mensual, o el número total de filas para todos).

        Returns:
            list: Una lista donde cada elemento representa el tamaño de cada página (número de filas).
        """
        if periodicidad not in ["Todos", "Anual", "Mensual"]:
            raise ValueError("Periodicidad no válida. Use 'anual', 'mensual' o 'todos'.")

        if periodicidad == "Todos":
            # Para "Todos", la cantidad determina cuántas filas habrá por página
            tamanos_paginas = []
            total_filas = len(self.conexion.datos)  # Total de filas en los datos

            # Calcular el número de páginas
            num_paginas = total_filas // cantidad  # Número completo de páginas
            resto = total_filas % cantidad  # Filas restantes para la última página

            # Agregar el tamaño de cada página
            for _ in range(num_paginas):
                tamanos_paginas.append(cantidad)  # Agregar páginas completas

            if resto > 0:
                tamanos_paginas.append(resto)  # Agregar la última página con las filas restantes

            return tamanos_paginas

        if not (1 <= cantidad <= 4):
            raise ValueError("Cantidad debe estar entre 1 y 4 para 'anual' y 'mensual'.")

        # Índice de la columna "fecha"
        fecha_index = self.conexion.headers.index("fecha")

        # Agrupar los datos por periodo
        conteo_por_periodo = defaultdict(int)

        for fila in self.conexion.datos:
            fecha = fila[fecha_index]
            if periodicidad == "Anual":
                clave_periodo = fecha.year
            elif periodicidad == "Mensual":
                clave_periodo = (fecha.year, fecha.month)
            conteo_por_periodo[clave_periodo] += 1

        # Convertir los conteos por periodo a una lista (respetando el orden original)
        conteo_filas = list(conteo_por_periodo.values())

        # Agrupar por cantidad para calcular el tamaño de las páginas
        tamanos_paginas = []
        acumulador = 0

        for i, conteo in enumerate(conteo_filas):
            acumulador += conteo
            if (i + 1) % cantidad == 0 or i == len(conteo_filas) - 1:
                tamanos_paginas.append(acumulador)
                acumulador = 0
        return tamanos_paginas

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

