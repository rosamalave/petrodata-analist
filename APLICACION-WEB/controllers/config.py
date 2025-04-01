import os 
from PIL import Image, ImageTk 

def cargar_imagen(nombre_imagen, tamanio=(20, 20)):
    """Args: nombre_imagen= nombre.png; tamanio = (20,20) tamaño pixeles """
    
    base_dir = os.path.dirname(os.path.abspath(__file__))  
    parent_dir = os.path.dirname(base_dir)  
    imagen_path = os.path.join(parent_dir, 'resources', 'images', nombre_imagen)
    imagen = Image.open(imagen_path).resize(tamanio, Image.ANTIALIAS)
    return ImageTk.PhotoImage(imagen)