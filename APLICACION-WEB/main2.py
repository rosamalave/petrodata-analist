import sys
from PyQt5 import QtWidgets, QtCore
from pruebabackend import ConsolaDBBackend
from bd.conexion_bd import base_ddatos

class Main():

    def __init__(self):
        super().__init__()
        # Inicializar la conexión a la base de datos
        self.conexion = ConsolaDBBackend(base_ddatos(), "public", "produccion_c")

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

