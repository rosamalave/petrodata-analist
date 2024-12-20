from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout
from bd.conexion_bd import base_ddatos

class vistalogin(QWidget):
    def __init__(self, on_login):
        super().__init__()
        self.on_login = on_login
        self.init_ui()
        self.conexion = base_ddatos()
        self.usuario = ""
        self.existe = False

    def init_ui(self):
        self.layout = QVBoxLayout()

        # Layout inicial para los botones de login
        self.button_layout = QHBoxLayout()

        self.marielys_button = QPushButton("Marielys", self)
        self.marielys_button.clicked.connect(lambda: self.handle_login("Marielys"))
        self.button_layout.addWidget(self.marielys_button)

        self.luis_button = QPushButton("Luis", self)
        self.luis_button.clicked.connect(lambda: self.handle_login("Luis"))
        self.button_layout.addWidget(self.luis_button)

        self.layout.addLayout(self.button_layout)
        
        # Widgets de inicio de sesión (inicialmente ocultos)
        self.welcome_label = QLabel("", self)
        self.layout.addWidget(self.welcome_label)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Ingrese su contraseña")
        self.password_input.setEchoMode(QLineEdit.Password)  # Para ocultar la contraseña
        self.layout.addWidget(self.password_input)

        self.login_button = QPushButton("Iniciar sesión", self)
        self.login_button.clicked.connect(lambda: self.confirm_login(self.usuario))
        self.layout.addWidget(self.login_button)

        self.back_button = QPushButton("Volver", self)
        self.back_button.setStyleSheet("text-decoration: underline; color: blue;")  # Estilo de texto link
        self.back_button.clicked.connect(self.show_user_selection)
        self.layout.addWidget(self.back_button)

        # Ocultar los widgets de inicio de sesión inicialmente
        self.welcome_label.setVisible(False)
        self.password_input.setVisible(False)
        self.login_button.setVisible(False)
        self.back_button.setVisible(False)

        self.setLayout(self.layout)

    def handle_login(self, user_type):
        self.usuario = user_type

        # Muestra el mensaje de bienvenida
        self.welcome_label.setText(f"Bienvenido, {user_type.capitalize()}!")
        self.welcome_label.setVisible(True)

        # Muestra los campos de contraseña y botones
        self.password_input.setVisible(True)
        self.login_button.setVisible(True)
        self.back_button.setVisible(True)

        # Oculta los botones de selección de usuario
        self.marielys_button.setVisible(False)
        self.luis_button.setVisible(False)

    def confirm_login(self, user_type):
        # Obtiene la contraseña ingresada y llama a la función de autenticación
        password = self.password_input.text()
        # Lógica de autenticación basada en el tipo de usuario
        if self.conexion.verificariniciarsesion(self.usuario, password):
            self.existe = True
            self.on_login()
        else:
            print("usuario invalido, no existe en la base de datos")

    def show_user_selection(self):
        # Oculta los widgets de inicio de sesión
        self.welcome_label.setVisible(False)
        self.password_input.setVisible(False)
        self.login_button.setVisible(False)
        self.back_button.setVisible(False)

        # Muestra los botones de selección de usuario
        self.marielys_button.setVisible(True)
        self.luis_button.setVisible(True)
        
    def cerrarsesion(self):
        self.conexion.cerrarsesion(self.usuario, self.existe)
