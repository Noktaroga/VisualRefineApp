import os
from PIL import Image, ImageEnhance, ImageFilter

path = os.path.abspath("imgs")        # carpeta de imágenes no editadas
pathOut = os.path.abspath("editedImgs")  # carpeta de imágenes editadas

# Crear el directorio de salida si no existe
if not os.path.exists(pathOut):
    os.makedirs(pathOut)

for filename in os.listdir(path):
    img = Image.open(os.path.join(path, filename))

    # Aplicar las transformaciones
    edit = img.filter(ImageFilter.SHARPEN).convert('L')

    # Contraste
    factor = 1.5
    enhancer = ImageEnhance.Contrast(edit)
    edit = enhancer.enhance(factor)

    # Nombre limpio del archivo
    clean_name = os.path.splitext(filename)[0]

    # Formar la ruta completa del archivo de imagen editada
    edited_filename = f"{clean_name}_edited.jpg"
    edited_filepath = os.path.join(pathOut, edited_filename)

    # Guardar la imagen editada en la carpeta de salida
    edit.save(edited_filepath)

print("Proceso completado.")
