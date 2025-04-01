import tkinter as tk
from tkinter import ttk, Entry, Button, Label, PhotoImage, messagebox
from views.login import LoginView
from views.layout import MainLayout
# =================== Clase Principal MainApp ===================
#error es que no se ha cambiado la referencia del combobox con la de mainlayout
class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Aplicación Principal")
        self.geometry("862x519")
        self.start_login()
        self.protocol("WM_DELETE_WINDOW", self.on_cerrar_ventana)

    def start_login(self):
        """ Inicia la pantalla de login """
        self.login_view = LoginView(self, self.on_login_success)

    def on_login_success(self, usuario,conexion):
        """ Método llamado tras el login exitoso """
        for widget in self.winfo_children():
            widget.destroy()  # Elimina la vista de login
        self.init_main_layout(usuario,conexion)

    def init_main_layout(self,usuario,conexion):
        self.mainlayout=MainLayout(self,usuario,conexion)
        # Configuramos el protocolo de cierre para ejecutar un método personalizado
        
    def on_cerrar_ventana(self):
        # Aquí pones el código que deseas ejecutar cuando se cierre la ventana
        respuesta = messagebox.askyesno("Confirmar", "¿Seguro que deseas salir?")
        if respuesta:  # Si el usuario hace clic en "Sí"
            self.login_view.cerrarsesion()
            print("Ventana cerrada")
            self.destroy()  # Cierra la ventana
        else:
            print("Cancelado el cierre de la ventana")

# =================== Lanzar la App ===================
if __name__ == "__main__":
    app = MainApp()
    app.mainloop()