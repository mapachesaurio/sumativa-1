# fix_links.py
# Ejecuta este script para agregar comillas automáticamente a todos los enlaces

input_file = "arreglo de links/links.txt"      # ← Cambia esto si tu archivo se llama diferente
output_file = "arreglo de links/links_fixed.txt"

with open(input_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

fixed = []
for line in lines:
    url = line.strip()
    if url:  # ignora líneas vacías
        fixed.append(f'          "{url}",')

# Guardar resultado
with open(output_file, "w", encoding="utf-8") as f:
    f.write("\n".join(fixed))

print(f"✅ Listo!")
print(f"   Se procesaron {len(fixed)} enlaces")
print(f"   Resultado guardado en: {output_file}")
print("\nCopia y pega el contenido de links_fixed.txt en tu mangas.js")