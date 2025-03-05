import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk  
from controllers.pruebabackend import ConsolaDBFrontend
import os

#falta que conectar las funciones de editar, eliminar e insertar para que aplique a la bd

def iniciar_sesion_y_mostrar_tabla():
    """Inicia sesión en la BD, obtiene los datos y luego crea la ventana con la tabla."""
    print("Iniciando sesión en la BD...")
    app = ConsolaDBFrontend()
    app.iniciar_sesion()  

    if not app.backend.datos:
        print("Error: No se cargaron datos desde la BD.")
        return

    print("Datos cargados, creando ventana...")
    root = EditableTable(app.backend)
    root.mainloop()

def cargar_imagen(nombre_imagen, tamanio=(20, 20)):
    base_dir = os.path.dirname(os.path.abspath(__file__))  
    parent_dir = os.path.dirname(base_dir)  
    imagen_path = os.path.join(parent_dir, 'resources', 'images', nombre_imagen)
    imagen = Image.open(imagen_path).resize(tamanio, Image.ANTIALIAS)
    return ImageTk.PhotoImage(imagen)

class EditableTable(tk.Tk):
    def __init__(self, backend):
        super().__init__()

        self.title("Gestión de Datos")
        self.geometry("900x500")

        self.backend = backend
        main_frame = tk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)

        self.sidebar = tk.Frame(main_frame, width=200, bg="lightgray")
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)

        self.headers = self.backend.headers + ["Acciones"]  
        print("Headers cargados:", self.headers)

        self.create_filter_widgets()

        self.btn_add_row = tk.Button(self.sidebar, text="Agregar Fila", command=self.add_empty_row)
        self.btn_add_row.pack(pady=10)

        self.btn_delete_row = tk.Button(self.sidebar, text="Eliminar Fila", command=self.delete_row, state=tk.DISABLED)
        self.btn_delete_row.pack(pady=10)

        self.btn_undo_filter = tk.Button(self.sidebar, text="Deshacer Filtro", command=self.undo_filter, state=tk.DISABLED)
        self.btn_undo_filter.pack(pady=10)

        table_frame = tk.Frame(main_frame)
        table_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(table_frame, columns=self.headers, show="headings")

        for col in self.headers:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor="center")  

        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<Double-1>", self.enable_editing)

        self.check_icon = cargar_imagen('check2.ico', (20, 20))  
        self.cancel_icon = cargar_imagen('cancel2.ico', (20, 20))  

        self.load_data(self.backend.datos)

        self.entry_vars = {}  
        self.entries = {}  
        self.current_item = None  
        self.previous_values = None  
        self.btn_save = None
        self.btn_cancel = None

        self.is_filter_applied = False  # Variable que indica si un filtro está activo

        # Evento de redimensionar la ventana
        self.bind("<Configure>", self.on_resize)

    def create_filter_widgets(self):
        """Crea los widgets de filtrado en el sidebar"""
        self.filtro_valores_frame = tk.Frame(self.sidebar, bg="lightgray")
        self.filtro_valores_frame.pack(pady=15)

        tk.Label(self.filtro_valores_frame, text="Filtrar por valores", bg="lightgray").pack(pady=5)
        self.columnafiltrar = ttk.Combobox(self.filtro_valores_frame, values=self.headers[:-1], state="readonly")
        self.columnafiltrar.pack(pady=5)

        self.valor_min = tk.Spinbox(self.filtro_valores_frame, from_=0, to=20000)
        self.valor_min.pack(pady=5)
        self.valor_max = tk.Spinbox(self.filtro_valores_frame, from_=0, to=20000)
        self.valor_max.pack(pady=5)

        self.filtrar_valores_button = tk.Button(self.filtro_valores_frame, text="Filtrar", command=self.filtro_por_valores)
        self.filtrar_valores_button.pack(pady=5)

    def filtro_por_valores(self):
        """Filtra los datos según la columna y el rango de valores"""
        datos_filtrados = self.backend.filtrar_por_valores(self.columnafiltrar.get(), self.valor_min.get(), self.valor_max.get())
        
        if datos_filtrados:
            self.load_data(datos_filtrados)
            self.is_filter_applied = True  # Marcamos que el filtro está activo
            self.btn_undo_filter.config(state=tk.NORMAL)  # Habilitamos el botón de deshacer filtro
        else:
            messagebox.showinfo("Sin resultados", "No se encontraron datos que coincidan con los criterios.")

    def undo_filter(self):
        """Deshace el filtro y restaura los datos originales"""
        self.load_data(self.backend.datos)  # Restaura todos los datos
        self.is_filter_applied = False  # Marcamos que el filtro no está activo
        self.btn_undo_filter.config(state=tk.DISABLED)  # Deshabilitamos el botón de deshacer filtro

    def load_data(self, data=None):
        """Carga los datos en la tabla"""
        for item in self.tree.get_children():
            self.tree.delete(item)

        data = data if data else self.backend.datos

        for row in data:
            self.tree.insert("", tk.END, values=row + [""],)  

        self.tree.pack(fill=tk.BOTH, expand=True)

    def add_empty_row(self):
        """Agrega una fila vacía"""
        new_id = len(self.tree.get_children()) + 1
        self.tree.insert("", tk.END, values=(new_id, "", "", "", "", ""))  

    def delete_row(self):
        """Elimina la fila seleccionada"""
        if self.current_item:
            self.tree.delete(self.current_item)
            self.clear_entries()

    def enable_editing(self, event):
        """Habilita la edición de una fila completa al hacer doble clic"""
        selected_item = self.tree.selection()
        if not selected_item:
            return

        # Limpiar ediciones previas
        self.clear_entries()

        self.current_item = selected_item[0]
        self.previous_values = self.tree.item(self.current_item, "values")  # Guardar valores originales

        # Crear cuadros de entrada en lugar de los valores actuales
        self.entries = {}
        self.entry_vars = {}

        headers = self.headers  # Asegúrate de que `self.headers` contenga los nombres de las columnas
        for i, col_name in enumerate(headers):  # Recorremos las columnas en el orden de headers
            if col_name.lower() == "acciones":  # Excluimos la columna "Acciones"
                continue

            # Obtener el valor actual para la celda
            value = self.previous_values[i]

            # Obtener la posición de la celda seleccionada
            col_id = "#{}".format(i+1)
            x, y, width, height = self.tree.bbox(self.current_item, column=col_id)

            if width == 0:
                continue

            # Variable de control para el Entry
            var = tk.StringVar(value=value)
            self.entry_vars[i] = var  # Usamos índice en lugar de nombre de columna

            # Crear el Entry con texto centrado
            entry = tk.Entry(self.tree, textvariable=var, font=("Arial", 10), justify="center")
            entry.place(x=x, y=y, width=width, height=height)
            self.entries[i] = entry  # Guardamos el Entry con el índice

            # Enfocar el primer campo editable (opcional)
            if i == 0:  # Primer campo editable
                entry.focus_set()

        # Agregar botones al final de la fila
        self.add_action_buttons()

        # Mostrar el botón de eliminar en la barra lateral
        self.btn_delete_row.config(state=tk.NORMAL)

    def add_action_buttons(self):
        """Añade botones de guardar y cancelar en la columna Acciones"""
        x, y, width, height = self.tree.bbox(self.current_item, column=len(self.headers) - 1)

        if self.btn_save:
            self.btn_save.destroy()
        if self.btn_cancel:
            self.btn_cancel.destroy()

        self.btn_save = tk.Button(self.tree, image=self.check_icon, command=self.save_changes, borderwidth=0)
        self.btn_save.place(x=x + 10, y=y, width=20, height=20)

        self.btn_cancel = tk.Button(self.tree, image=self.cancel_icon, command=self.cancel_edit, borderwidth=0)
        self.btn_cancel.place(x=x + 30, y=y, width=20, height=20)

    def save_changes(self):
        """Guarda los cambios editados en la fila"""
        new_values = [self.entry_vars[i].get() for i in range(len(self.headers)-1)]

        self.tree.item(self.current_item, values=new_values + [""])
        self.clear_entries()

    def cancel_edit(self):
        """Cancela la edición y restaura los valores originales"""
        if self.previous_values:
            self.tree.item(self.current_item, values=self.previous_values)
        self.clear_entries()

    def clear_entries(self):
        """Elimina los cuadros de entrada y resetea variables"""
        for entry in self.entries.values():
            entry.destroy()
        self.entries.clear()
        self.entry_vars.clear()
        self.current_item = None
        self.previous_values = None

        if self.btn_save:
            self.btn_save.destroy()
            self.btn_save = None
        if self.btn_cancel:
            self.btn_cancel.destroy()
            self.btn_cancel = None

        self.btn_delete_row.config(state=tk.DISABLED)

    def on_resize(self, event):
        """Reajusta la posición de los botones y los Entry cuando la ventana cambia de tamaño"""
        if self.current_item:
            # Recalcular la posición de los botones
            x, y, width, height = self.tree.bbox(self.current_item, column=len(self.headers) - 1)

            # Ajustar los botones según el nuevo tamaño
            spacing = 10
            button_width = 20
            total_width = width - (2 * spacing)
            offset = (total_width - (button_width * 2 + spacing)) / 2

            if self.btn_save:
                self.btn_save.place(x=x + offset, y=y, width=button_width, height=button_width)
            if self.btn_cancel:
                self.btn_cancel.place(x=x + offset + button_width + spacing, y=y, width=button_width, height=button_width)

            # Recalcular la posición y tamaño de los Entry
            for i, entry in enumerate(self.entries.values()):
                x, y, width, height = self.tree.bbox(self.current_item, column=i)
                if width > 0:
                    entry.place(x=x, y=y, width=width, height=height)

if __name__ == "__main__":
    iniciar_sesion_y_mostrar_tabla()