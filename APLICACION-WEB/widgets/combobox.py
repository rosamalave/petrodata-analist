import tkinter as tk
from tkinter import PhotoImage
from pathlib import Path

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"R:\Rosa\PASANTIAS\EMPAQUETADO-PROYECTO\Tkinter-Designer-master\pruebas\build\assets\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class ButtonCustom(tk.Button):
    def __init__(self, master, options, image, width, height, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        # Parámetros
        self.options = options  # Opciones para el menú
        self.image = image  # Imagen del botón
        self.width = width  # Ancho del botón
        self.height = height  # Alto del botón
        self.selected_option = tk.StringVar(value=options[0])  # Valor predeterminado de la opción seleccionada

        # Configuración inicial del botón
        self.config(
            image=image,
            compound="center",  # Imagen y texto centrados
            relief="flat",
            borderwidth=0,
            command=self.toggle_menu
        )

        self.option_menu = None  # Inicializamos el menú desplegable como None
        self.menu_visible = False  # El menú no es visible inicialmente

    def toggle_menu(self):
        # Función que maneja el clic en el botón
        if self.menu_visible:
            # Si el menú está visible, lo ocultamos
            self.hide_menu()
        else:
            # Si el menú no está visible, lo mostramos
            self.show_menu()

    def show_menu(self):
        # Crear el menú desplegable debajo del botón
        y_position = self.winfo_y() + self.winfo_height()
        self.option_menu = tk.Listbox(self.master, height=len(self.options), selectmode="single", bd=0, font=("Poppins", 10))
        
        for option in self.options:
            self.option_menu.insert(tk.END, option)
        
        self.option_menu.place(x=self.winfo_x(), y=y_position, width=self.width, height=self.height * len(self.options))
        self.option_menu.bind("<ButtonRelease-1>", self.select_option)  # Llamamos a select_option al seleccionar

        self.menu_visible = True

    def hide_menu(self):
        # Ocultar el menú
        if self.option_menu:
            self.option_menu.place_forget()
            self.option_menu = None
        self.menu_visible = False

    def select_option(self, event):
        # Obtener la opción seleccionada y actualizar el texto del botón
        selected_index = self.option_menu.curselection()
        if selected_index:
            selected_option = self.option_menu.get(selected_index[0])
            self.selected_option.set(selected_option)
            self.config(text=self.selected_option.get(), font=("Poppins", 9))  # Actualizar el texto del botón
        self.hide_menu()  # Ocultar el menú después de seleccionar

# EJEMPLO Crear la ventana principal
#root = tk.Tk()
#root.geometry("800x600")

# Cargar la imagen para el botón
#button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))

# Crear el botón personalizado con las opciones
#options = ['Rojo', 'Azul', 'Verde']
#button_custom = ButtonCustom(root, options, button_image_2, width=227, height=22)

# Colocar el botón en la ventana con .place()
#button_custom.place(x=561.0, y=293.0, width=227, height=22)

#root.mainloop()