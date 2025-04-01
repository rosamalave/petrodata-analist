from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Frame, messagebox
import tkinter as tk
from tkinter import ttk
from views.homepage import HomePage
from views.tablawidget import EditableTable

class MainLayout(tk.Frame):
    def __init__(self, root, usuario, conexion):
        super().__init__(root)
        self.root = root
        self.usuario=usuario
        self.conexion=conexion 
        self.estado_sidebar = 0  # Comienza en estado default
        self.ultimo_boton = None  # Guarda el último botón presionado

        self.setup_ui()
        # Diccionario de imágenes de los botones
        self.imagenes_botones = {
            1: {"normal": self.button_image_1, "seleccionado": self.image_image_1},
            2: {"normal": self.button_image_2, "seleccionado": self.image_image_2},
            3: {"normal": self.button_image_3, "seleccionado": self.image_image_3},
            4: {"normal": self.button_image_4, "seleccionado": self.image_image_4},
        }

        # Diccionario de botones para referencia rápida
        self.botones = {
            1: {"boton": self.button_1, "x": 0.0, "y": 137.0},
            2: {"boton": self.button_2, "x": 0.0, "y": 194.0},
            3: {"boton": self.button_3, "x": 0.0, "y": 251.0},
            4: {"boton": self.button_4, "x": 0.0, "y": 308.0},
        }

        # Asignación de funciones a los botones
        self.botones[1]["boton"].config(command=lambda: self.gestionar_click(1, True))
        self.botones[2]["boton"].config(command=lambda: self.gestionar_click(2, True))
        self.botones[3]["boton"].config(command=lambda: self.gestionar_click(3, False))
        self.botones[4]["boton"].config(command=lambda: self.gestionar_click(4, False))
        

    def relative_to_assets(self, path: str) -> Path:
        ASSETS_PATH = Path(r"R:\Rosa\PASANTIAS\PROYECTO-PDVSA\APLICACION-WEB\resources\images\layout")
        return ASSETS_PATH / Path(path)

    def setup_ui(self):
        self.root.geometry("862x519")
        self.root.configure(bg="#FFFFFF")

        self.canvas = Canvas(
            self.root,
            bg="#FFFFFF",
            height=519,
            width=862,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )

        self.canvas.place(x=0, y=0)
        self.canvas.create_rectangle(0.0, 0.0, 188.0, 519.0, fill="#144A96", outline="")
        self.canvas.create_rectangle(0.0, 0.0, 862.0, 48.0, fill="#144A96", outline="")

        self.image_image_9 = PhotoImage(file=self.relative_to_assets("image_9.png"))
        self.image_9 = self.canvas.create_image(518.0, 296.0, image=self.image_image_9)

        self.button_image_5 = PhotoImage(file=self.relative_to_assets("image_5_2.png"))
        self.button_5 = Button(
            image=self.button_image_5,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_5 clicked"),
            relief="flat"
        )
        self.button_5.place(x=146.0, y=10.0, width=42.0, height=29.0)

        # Agregar el Notebook aquí
        self.setup_styles()
        self.setup_notebook()

        self.image_image_5 = PhotoImage(file=self.relative_to_assets("image_5.png"))
        self.image_5 = self.canvas.create_image(167.0, 24.0, image=self.image_image_5)
        self.canvas.itemconfig(self.image_5, state="hidden")
        self.image_image_7 = PhotoImage(file=self.relative_to_assets("image_7.png"))
        self.image_7 = self.canvas.create_image(63.0, 438.0, image=self.image_image_7)

        self.image_image_6 = PhotoImage(file=self.relative_to_assets("image_6.png"))
        self.image_6 = self.canvas.create_image(63.0, -123.0, image=self.image_image_6)

        self.rect_id = self.canvas.create_rectangle(0.0, 0.0, 127.0, 519.0, fill="#003462", outline="")

        self.image_image_8 = PhotoImage(file=self.relative_to_assets("image_8.png"))
        self.image_8 = self.canvas.create_image(61.0, 70.0, image=self.image_image_8)

        self.image_image_4 = PhotoImage(file=self.relative_to_assets("image_4.png"))
        self.image_4 = self.canvas.create_image(63.0, 329.0, image=self.image_image_4)

        self.image_image_3 = PhotoImage(file=self.relative_to_assets("image_3.png"))
        self.image_3 = self.canvas.create_image(63.0, 272.0, image=self.image_image_3)

        self.image_image_2 = PhotoImage(file=self.relative_to_assets("image_2.png"))
        self.image_2 = self.canvas.create_image(63.0, 215.0, image=self.image_image_2)

        self.image_image_1 = PhotoImage(file=self.relative_to_assets("image_1.png"))
        self.image_1 = self.canvas.create_image(63.0, 158.0, image=self.image_image_1)

        self.button_image_4 = PhotoImage(file=self.relative_to_assets("button_4.png"))
        self.button_4 = Button(
            image=self.button_image_4,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_4 clicked"),
            relief="flat"
        )
        self.button_4.place(x=0.0, y=308.0, width=127.0, height=42.0)

        self.button_image_3 = PhotoImage(file=self.relative_to_assets("button_3.png"))
        self.button_3 = Button(
            image=self.button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_3 clicked"),
            relief="flat"
        )
        self.button_3.place(x=0.0, y=251.0, width=127.0, height=42.0)

        self.button_image_2 = PhotoImage(file=self.relative_to_assets("button_2.png"))
        self.button_2 = Button(
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_2 clicked"),
            relief="flat"
        )
        self.button_2.place(x=0.0, y=194.0, width=127.0, height=42.0)

        self.button_image_1 = PhotoImage(file=self.relative_to_assets("button_1.png"))
        self.button_1 = Button(
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_1 clicked"),
            relief="flat"
        )
        self.button_1.place(x=0.0, y=137.0, width=127.0, height=42.0)

        self.button_5.place_forget()

        self.contenedor_filtro = tk.Frame(self.root, bg="white")

        self.headers = ['pred', 'pred', 'pred']
        self.filter_widgets = self.create_filter_widgets(self.contenedor_filtro, self.headers)
        self.notebook.bind("<<NotebookTabChanged>>", lambda e: self.update_filter_headers())

    def setup_styles(self):
        
        style = ttk.Style()
        style.theme_use("default")  # Asegura compatibilidad con cambios de color

        # Cambia el fondo de la barra de pestañas (área donde están los títulos)
        style.configure("TNotebook", background="#144A96", borderwidth=0)

        # Cambia el color de fondo de las pestañas (cuando NO están seleccionadas)
        style.configure("TNotebook.Tab", background="white", padding=[-1,-1], borderwidth=0, font=('Poppins', 10))

        # Cambia el color de la pestaña seleccionada
        style.map("TNotebook.Tab", background=[("selected", "white"), ])

    def setup_notebook(self):
        self.notebook_frame = tk.Frame(self.root, bg="white")
        self.notebook_frame.place(x=155, y=25, width=720, height=465)  # Ajusta la posición y tamaño según sea necesario
        self.notebook = ttk.Notebook(self.notebook_frame, style="TNotebook")
        self.notebook.pack(expand=True, fill="both")  # Asegura que el Notebook ocupe todo el espacio disponible
        # Pestaña inicial homepage
        self.homepage_frame = HomePage(self)      
        self.notebook.add(self.homepage_frame, image=self.button_image_5)  # Espacio vacío
        self.notebook.select(self.homepage_frame)  # Seleccionar la primera pestaña por defecto
    
    def update_filter_headers(self):
        """Actualiza los encabezados del filtro cuando cambia la pestaña activa"""

        current_tab = self.notebook.nametowidget(self.notebook.select())  # Obtener la pestaña activa
        
        if hasattr(current_tab, 'headers'):  # Verificar si la tabla tiene encabezados
            self.headers = current_tab.headers  # Obtener headers dinámicamente

            filtered_headers = [h for h in self.headers[:-1] if h.lower() != "fecha"]
            
            # Actualizar valores del Combobox de columnas
            self.filter_widgets["columnafiltrar"]["values"] = filtered_headers

            # Reiniciar selección para evitar errores
            self.filter_widgets["columnafiltrar"].set("")  
        else:
            self.headers = []
            self.filter_widgets["columnafiltrar"]["values"] = []  # Vaciar el combobox
            print("No hay una tabla activa con encabezados para filtrar.")

    def apply_filter_to_active_table(self):
        """Aplica el filtro a la tabla activa en el Notebook"""
        current_tab = self.notebook.nametowidget(self.notebook.select())  # Obtiene la pestaña activa
        
        if hasattr(current_tab, 'filtro_por_valores'):
            columna = self.filter_widgets["columnafiltrar"].get()
            min_val = self.filter_widgets["valor_min"].get()
            max_val = self.filter_widgets["valor_max"].get()

            current_tab.filtro_por_valores(columna, min_val, max_val)  # ✅ Llama al método de `EditableTable`
        else:
            messagebox.showwarning("Error", "No hay una tabla activa para aplicar filtros.")    

    def create_filter_widgets(self, contenedor_filtro, headers):
        """Crea los widgets de filtrado en el contenedor de filtros"""
        filtro_valores_frame = tk.Frame(contenedor_filtro, bg="white")
        filtro_valores_frame.place(x=10, y=10, width=80, height=180)

        tk.Label(filtro_valores_frame, text="Filtro por valores", bg="white", font=('Poppins Medium', 7)).pack(pady=5)

        columnafiltrar = ttk.Combobox(filtro_valores_frame, values=headers[:-1], state="readonly")
        columnafiltrar.pack(pady=5)

        valor_min = tk.Spinbox(filtro_valores_frame, from_=0, to=20000)
        valor_min.pack(pady=5)

        valor_max = tk.Spinbox(filtro_valores_frame, from_=0, to=20000)
        valor_max.pack(pady=5)

        filtrar_valores_button = tk.Button(filtro_valores_frame, text="Filtrar", font=('Poppins Medium', 8), bg="#144A96", height=1, width=15, fg="white", command=self.apply_filter_to_active_table)
        filtrar_valores_button.pack(pady=10)

        return {
            "filtro_valores_frame": filtro_valores_frame,
            "columnafiltrar": columnafiltrar,
            "valor_min": valor_min,
            "valor_max": valor_max,
            "filtrar_valores_button": filtrar_valores_button
        }
    
    def cambiar_imagen_boton(self, nuevo_numero):
        if self.ultimo_boton is not None:
            self.botones[self.ultimo_boton]["boton"].config(image=self.imagenes_botones[self.ultimo_boton]["normal"])
        self.botones[nuevo_numero]["boton"].config(image=self.imagenes_botones[nuevo_numero]["seleccionado"])
        self.ultimo_boton = nuevo_numero

    def gestionar_click(self, n, es_expandible):
        if self.ultimo_boton == n:
            if self.estado_sidebar == 1:
                if es_expandible:
                    self.estado_sidebar = 2
                    self.canvas.itemconfig(self.image_1, state="hidden")
                    self.canvas.itemconfig(self.image_2, state="hidden")
                    self.canvas.itemconfig(self.image_3, state="hidden")
                    self.canvas.itemconfig(self.image_4, state="hidden")
                    self.mover_rectangulos_y_ocultar_boton(n)
                    print("Estado cambiado a {}: Botón expandible seleccionado".format(self.estado_sidebar))
                else:
                    self.estado_sidebar = 0
                    print("Estado cambiado a {}: Botón sin expandir, regresando a default".format(self.estado_sidebar))
                    self.botones[n]["boton"].config(image=self.imagenes_botones[n]["normal"])
                    self.canvas.itemconfig(self.rect_id, state="normal")
                    self.ultimo_boton = None
                    return
            elif self.estado_sidebar == 2:
                self.estado_sidebar = 1
                self.contenedor_filtro.place_forget()
                self.mover_rectangulos_y_ocultar_boton(n)
                self.canvas.itemconfig(self.image_1, state="normal")
                self.canvas.itemconfig(self.image_2, state="normal")
                self.canvas.itemconfig(self.image_3, state="normal")
                self.canvas.itemconfig(self.image_4, state="normal")
                self.restaurarbotones()
                print("Estado cambiado a {}: Cerrando opciones desplegadas".format(self.estado_sidebar))
            else:
                self.estado_sidebar = 1
                print("Estado cambiado a {}: Seleccionado".format(self.estado_sidebar))
                self.mover_rectangulos_y_ocultar_boton(n)
        else:
            self.estado_sidebar = 1
            print("Estado cambiado a {}: Nuevo botón seleccionado".format(self.estado_sidebar))
            self.mover_rectangulos_y_ocultar_boton(n)

        self.ultimo_boton = n

    def mover_rectangulos_y_ocultar_boton(self, n):
        y_boton = 137 + (n - 1) * (42 + 15)
        y_imagen = y_boton + 21
        y_rect_superior = y_imagen - 281
        y_rect_inferior = y_imagen + 280

        self.canvas.coords(self.image_6, 63.0, y_rect_superior)
        self.canvas.itemconfig(self.rect_id, state="hidden")

        if self.estado_sidebar == 2:
            y_filtro = y_boton + 42
            x_filtro = (127 - 100) / 2
            self.contenedor_filtro.place(x=x_filtro, y=y_filtro, width=100, height=200)

            y_rect_inferior = y_filtro + 460 + 15
            for i, btn in self.botones.items():
                if i != n:
                    btn["boton"].place_forget()
        else:
            self.contenedor_filtro.place_forget()

        self.canvas.coords(self.image_7, 63.0, y_rect_inferior)
        self.cambiar_imagen_boton(n)

    def restaurarbotones(self):
        for key, value in self.botones.items():
            boton = value["boton"]
            x = value["x"]
            y = value["y"]
            boton.place(x=x, y=y)

    def add_tab(self, widget,tabla):
        # Agregar una nueva pestaña con EditableTable
        self.notebook.add(widget, text="     {}     ".format(tabla))
        self.notebook.select(widget)
   
    def close_tab(self, index):
        """Cierra una pestaña específica por su índice"""
        if index > 0:  # No permite cerrar la pestaña HomePage
            self.notebook.forget(index)
    def on_tab_change(self, event=None):
        """Actualiza el filtro cuando cambia la pestaña."""
        self.update_filter()


if __name__ == "__main__":
    window = Tk()
    app = MainLayout(window)
    window.mainloop()