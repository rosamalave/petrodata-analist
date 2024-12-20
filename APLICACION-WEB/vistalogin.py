from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout
from bd.conexion_bd import base_ddatos

class vistalogin(QWidget):
    def __init__(self, on_login):
        super().__init__()
        self.on_login = on_login
        self.init_ui()
        self.conexion=base_ddatos()

    def init_ui(self):
        layout = QVBoxLayout()
        # Layout horizontal para los botones de login
        button_layout = QHBoxLayout()

        self.marielys_button = QPushButton("Marielys", self)
        self.marielys_button.clicked.connect(lambda: self.handle_login("marielys"))
        button_layout.addWidget(self.marielys_button)

        self.luis_button = QPushButton("Luis", self)
        self.luis_button.clicked.connect(lambda: self.handle_login("luis"))
        button_layout.addWidget(self.luis_button)
        layout.addLayout(button_layout)
        self.setLayout(layout)

    def handle_login(self, user_type):

        # Lógica de autenticación basada en el tipo de usuario
        if user_type == "marielys":
            # Lógica específica para Marielys
            self.conexion.iniciarsesion("marielys")
        elif user_type == "luis":
            # Lógica específica para Luis
            self.conexion.iniciarsesion("luis")

    def authenticate_user(self, user_type, username, password):
        # Simulación de autenticación
        if (user_type == "marielys" and username == "marielys" and password == "password1") or \
           (user_type == "luis" and username == "luis" and password == "password2"):
            self.on_login()  # Llama a la función de inicio de sesión exitosa