import os

# Ruta de la carpeta donde están tus capítulos
folder = r"C:\Users\yo\Desktop\sumativa-1\mangas\El_Mago_Pastor/Cap_015"

# Obtiene todos los archivos de la carpeta
files = os.listdir(folder)

# Filtra solo imágenes (puedes ajustar extensiones si usas .png)
images = [f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

# Ordena los archivos por nombre
images.sort()

# Renombra cada archivo con número consecutivo
for i, filename in enumerate(images, start=1):
    ext = os.path.splitext(filename)[1]  # conserva la extensión original (.jpg/.png)
    new_name = f"{i}{ext}"
    old_path = os.path.join(folder, filename)
    new_path = os.path.join(folder, new_name)
    os.rename(old_path, new_path)
    print(f"Renombrado: {filename} -> {new_name}")

print("✅ Renombrado completo")
