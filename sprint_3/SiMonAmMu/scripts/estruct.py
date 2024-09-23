import os

def listar_estructura(directorio, nivel=0, archivo=None):
    # Indentar según el nivel de profundidad
    indent = ' ' * 4 * nivel
    archivo.write(f"{indent}{os.path.basename(directorio)}/\n")
    
    # Recorrer todos los elementos en el directorio
    for item in os.listdir(directorio):
        ruta_item = os.path.join(directorio, item)
        if os.path.isdir(ruta_item):
            # Ignorar la carpeta 'build'
            if item == 'build':
                continue
            # Si es un directorio, llamar recursivamente
            listar_estructura(ruta_item, nivel + 1, archivo)
        else:
            # Si es un archivo, escribir su nombre
            archivo.write(f"{indent}    {item}\n")

# Cambia esta ruta por la ruta de tu proyecto
ruta_proyecto = "D:/2024-segunda etapa/Practica_Profesionalizante_I/sprint_3/SiMonAmMu"
ruta_salida = "D:/2024-segunda etapa\Practica_Profesionalizante_I\sprint_3\SiMonAmMu\docs\estructura_proyecto.txt"  # Nombre del archivo de salida

with open(ruta_salida, 'w') as archivo:
    listar_estructura(ruta_proyecto, archivo=archivo)

print(f"Estructura del proyecto guardada en {ruta_salida}")
