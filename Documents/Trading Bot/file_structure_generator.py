import os

def listar_archivos(ruta):
    for ruta_actual, directorios, archivos in os.walk(ruta):
        # Excluir las carpetas especificadas
        if ".git" in directorios:
            directorios.remove(".git")
        if "migrations" in directorios:
            directorios.remove("migrations")
        if "node_modules" in directorios:
            directorios.remove("node_modules")
        if "scripts" in directorios:
            directorios.remove("scripts")
        
        for archivo in archivos:
            ruta_relativa = os.path.relpath(ruta_actual, ruta)
            yield ruta_relativa, archivo

def escribir_estructura(estructura, archivo_salida):
    with open(archivo_salida, 'w') as archivo:
        for ruta, nombre_archivo in estructura:
            archivo.write(f"{ruta}\t{nombre_archivo}\n")

# Ruta de la carpeta principal
carpeta_principal = "C:\\Users\\durot\\Documents\\Trading Bot"  # Cambiar por la ruta deseada

# Obtener la estructura de archivos
estructura_archivos = listar_archivos(carpeta_principal)

# Nombre del archivo de salida
archivo_salida = "estructura_archivos.txt"

# Escribir la estructura en el archivo de salida
escribir_estructura(estructura_archivos, archivo_salida)

# Mostrar la estructura en la consola
for ruta, nombre_archivo in listar_archivos(carpeta_principal):
    print(ruta, nombre_archivo)

print("Estructura de archivos generada con éxito.")
