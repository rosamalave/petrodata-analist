from .qtdesign import Ui_Form  # Importa la clase generada por Qt Designer
from PyQt5.QtWidgets import QPushButton, QWidget, QTableWidgetItem, QHBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, Qt

class ExtendedUiForm(Ui_Form):
    def __init__(self, Form):
        self.setupUi(Form)


    def columnaedicion(self, accion, ruta, producto, esquema, tabla):
        num_filas = self.tabla.rowCount()
        num_columnas = self.tabla.columnCount()

        # Agregar columna para los botones
        self.tabla.setColumnCount(num_columnas + 1)
        self.tabla.setHorizontalHeaderItem(num_columnas, QTableWidgetItem("Acción"))

        for fila in range(num_filas):
            # Crear botón
            boton = QPushButton("Accionar")
            boton.setIcon(QIcon(ruta))  # Cambia la ruta por tu imagen
            boton.setIconSize(QSize(32, 32))  # Tamaño del ícono
            boton.clicked.connect(self.crear_accion(accion, fila, producto, esquema, tabla))  # Conectar a función con índice de fila

            # Agregar botón a la celda
            widget_boton = QWidget()
            layout_boton = QHBoxLayout(widget_boton)
            layout_boton.addWidget(boton)
            layout_boton.setAlignment(boton, Qt.AlignCenter)
            layout_boton.setContentsMargins(0, 0, 0, 0)
            widget_boton.setLayout(layout_boton)

            self.tabla.setCellWidget(fila, num_columnas, widget_boton)

    def crear_accion(self, accion, fila, producto, esquema, tabla):
        def accion_fila():
            accion(fila, producto, esquema, tabla)
        return accion_fila
