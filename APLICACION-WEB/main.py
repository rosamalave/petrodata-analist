# main.py
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QWidget
from vistalogin import vistalogin

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mi Aplicación")

        # Establecer el tamaño de la ventana principal
        self.setFixedSize(1366, 768)  # Tamaño fijo de la ventana

        self.stacked_widget = QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)

        self.login_view = vistalogin(self.show_table)  # Pasamos show_table como callback
        
        # Crear un QWidget para la tabla y configurar la interfaz
        self.table_view_widget = QWidget()  # Crear un QWidget
        self.table_view = vistalogin(self.show_table).frontend  # Crear la instancia de Ui_Form
        
        self.table_view.setupUi(self.table_view_widget)  # Configurar la interfaz en el QWidget

        self.stacked_widget.addWidget(self.login_view)
        self.stacked_widget.addWidget(self.table_view_widget)  # Agregar el QWidget configurado

        self.stacked_widget.setCurrentWidget(self.login_view)  # Muestra la vista de inicio de sesión al inicio

    def show_table(self):
        self.stacked_widget.setCurrentWidget(self.table_view_widget)  # Cambia a la vista de la tabla

    def closeEvent(self, event):
        # Aquí puedes agregar la lógica que deseas ejecutar al cerrar la aplicación
        self.login_view.cerrarsesion()
        # Acepta el cierre de la ventana
        event.accept()    
        
if __name__ == "__main__":

    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())