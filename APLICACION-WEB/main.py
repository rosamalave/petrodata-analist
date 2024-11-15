import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem
from primera_tabla import Ui_Form
from conexion_bd import base_ddatos

class MainApp(QWidget):
    def __init__(self, tabla,ctabla):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
        # Crear una instancia de la clase de conexión a la base de datos
        self.conectarbd = base_ddatos()

        # Inicializar la tabla en la interfaz con los datos desde la base de datos
        self.inicializar_tabla(tabla,ctabla)  # Pasa el nombre de la tabla a inicializar

        # Conectar el botón "aggfila" al método agregar_fila
        self.ui.aggfila.clicked.connect(self.agregar_fila)

    def inicializar_tabla(self, tabla,ctabla):
        # Crear un cursor
        cursor = self.conectarbd.conn.cursor()

        # Ejecutar consulta para obtener datos de la tabla
        cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_schema = 'public' AND table_name = '{tabla}' AND column_name NOT LIKE 'id%'")
        nombres = []
        for col in cursor.fetchall():
            nombres.append(str(col[0]))
 
        cursor.execute(f"SELECT * FROM {ctabla}")
        rows = cursor.fetchall()  # Obtiene todas las filas

        # Configurar la tabla en la interfaz
        self.ui.tabla.setRowCount(len(rows))
        self.ui.tabla.setColumnCount(len(rows[0]))  # Configura el número de columnas según la base de datos

        for i, row in enumerate(rows):
            for j, col in enumerate(row):
                self.ui.tabla.setItem(i, j, QTableWidgetItem(str(col)))  # Agrega los datos a la tabla
        
        cursor.close()
        
        self.ui.tabla.setColumnHidden(0, True)  # Oculta la primera columna
        self.ui.tabla.setColumnHidden(1, True)  # Oculta la segunda columna
        #asignando encabezados a la tabla
        for col in range(len(nombres)):
            self.ui.tabla.setHorizontalHeaderItem(col+2, QTableWidgetItem(nombres[col]))
        
        
    def agregar_fila(self):
        # Obtiene el número de filas actuales y añade una nueva al final
        nfilas = self.ui.tabla.rowCount()
        self.ui.tabla.insertRow(nfilas)

        # Opcional: Si deseas que las celdas de la nueva fila estén vacías
        for col in range(self.ui.tabla.columnCount()):
            item = QTableWidgetItem("")  # Crea un item vacío
            self.ui.tabla.setItem(nfilas, col, item)  # Añade el item vacío a la nueva fila

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Inicia el MainApp y especifica el nombre de la tabla que deseas cargar al inicio
    mainApp = MainApp("produccion_c","public.produccion_c")
    mainApp.show()
    sys.exit(app.exec_())