import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QWidget
from vistalogin import vistalogin
from qtdesign import Ui_Form  # Asegúrate de importar Ui_Form aquí

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mi Aplicación")

        # Establecer el tamaño de la ventana principal
        self.setFixedSize(1366, 768)  # Tamaño fijo de la ventana

        self.stacked_widget = QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)

        self.login_view = vistalogin(self.show_table)  # Pasamos show_table como callback
        self.stacked_widget.addWidget(self.login_view)  # Agregar la vista de inicio de sesión

        # Inicializa la vista de la tabla como None
        self.table_view_widget = None

    def show_table(self):
        # Crear la instancia de Ui_Form y configurar la interfaz
        if self.login_view.backend:  # Asegúrate de que el backend esté inicializado
            self.table_view_widget = QWidget()  # Crear un QWidget para la tabla
            self.table_view = Ui_Form(self.login_view.backend)  # Crear la instancia de Ui_Form
            self.table_view.setupUi(self.table_view_widget)  # Configurar la interfaz en el QWidget
            self.stacked_widget.addWidget(self.table_view_widget)  # Agregar el QWidget configurado
            self.stacked_widget.setCurrentWidget(self.table_view_widget)  # Cambia a la vista de la tabla
        else:
            print("Error: El backend no está inicializado.")

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