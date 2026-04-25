def mostrar_menu():
    print("\n--- MENÚ ---")
    print("1. Agregar manga")
    print("2. Editar título de manga")
    print("3. Añadir capítulo")
    print("4. Salir")

def agregar_manga():
    _id    = input("id: ")
    titulo = input("Título: ")
    genero = input("Género: ")
    rating = input("Rating: ")
    chapter_count = input("Cantidad de capitulos: ")
    cover = str(input("portada: "))
    synopsis = input("synopsis: ")
    nuevo = f"""\n    ,{{
      id: {_id},
      title: "{titulo}",
      genre: "{genero}",
      rating: {rating},
      chapters_count: {chapter_count},
      cover: "{cover}",
      synopsis: "{synopsis}",
      chapters: {[]}
    }}"""
    with open("data\mangas.js", "r+", encoding="utf-8") as f:
        contenido = f.read()
        pos = contenido.rfind("]")
        contenido = contenido[:pos] + nuevo + contenido[pos:]
        f.seek(0)
        f.write(contenido)
    print("Manga agregado.")


def editar_titulo():
    id_manga = input("ID del manga: ")
    nuevo_titulo = input("Nuevo título: ")
    with open("data\\mangas.js", "r+", encoding="utf-8") as f:
        contenido = f.read()
        contenido = contenido.replace(f'id: {id_manga},\n      title: "', 
                                      f'id: {id_manga},\n      title: "{nuevo_titulo}')
        f.seek(0)
        f.write(contenido)
    print("Título editado.")

def añadir_capitulo():
    id_manga = input("ID del manga: ")
    num_cap = input("Número de capítulo: ")
    print("Pega las URLs (una por línea). Termina con una línea vacía:")
    urls = []
    while True:
        linea = input()
        if linea.strip() == "":
            break
        urls.append(linea.strip())
    bloque_urls = ",\n          ".join([f'"{u}"' for u in urls])

    with open("data\\mangas.js", "r+", encoding="utf-8") as f:
        contenido = f.read()
        marcador = f'id: {id_manga},'
        pos = contenido.find(marcador)
        if pos == -1:
            print("Manga no encontrado.")
            return
        inicio = contenido.find("chapters:", pos)
        fin = contenido.find("}", inicio)
        sub_bloque = contenido[inicio:fin+1]

        cap_marker = f'"{num_cap}": ['
        if cap_marker in sub_bloque:
            nuevo_sub = sub_bloque.replace(cap_marker, cap_marker + "\n          " + bloque_urls + ",")
        else:
            nuevo_sub = sub_bloque.replace("chapters: {", 
                                           f'chapters: {{\n        "{num_cap}": [\n          {bloque_urls}\n        ]')
        contenido = contenido.replace(sub_bloque, nuevo_sub)

        f.seek(0)
        f.write(contenido)
        f.truncate()
    print("Capítulo agregado correctamente.")

# Loop principal
while True:
    mostrar_menu()
    opcion = input("Elige una opción: ")
    if opcion == "1":
        agregar_manga()
    elif opcion == "2":
        editar_titulo()
    elif opcion == "3":
        añadir_capitulo()
    elif opcion == "4":
        break
    else:
        print("Opción inválida.")
