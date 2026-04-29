import re

def mostrar_menu():
    print("\n--- MENÚ ---")
    print("1. Agregar manga")
    print("2. Editar título de manga")
    print("3. Añadir capítulo")
    print("4. Actualizar datos de manga")
    print("5. Salir")

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
      chapters: {{}}
    }}"""
    with open("data/mangas.js", "r+", encoding="utf-8") as f:
        contenido = f.read()
        pos = contenido.rfind("]")
        contenido = contenido[:pos] + nuevo + contenido[pos:]
        f.seek(0)
        f.write(contenido)
        f.truncate()
    print("Manga agregado.")


def editar_titulo():
    id_manga = input("ID del manga: ")
    nuevo_titulo = input("Nuevo título: ")
    with open("data/mangas.js", "r+", encoding="utf-8") as f:
        contenido = f.read()
        contenido = contenido.replace(f'id: {id_manga},\n      title: "',
                                      f'id: {id_manga},\n      title: "{nuevo_titulo}')
        f.seek(0)
        f.write(contenido)
        f.truncate()
    print("Título editado.")


def encontrar_cierre_chapters(contenido, pos_chapters):
    """
    Dado que `pos_chapters` apunta a 'chapters:',
    encuentra el índice del '{' que abre chapters y el '}' que lo cierra.
    Retorna (pos_open, pos_close) o None si no es chapters: {...}.
    """
    # Avanzar hasta el primer { o [
    i = pos_chapters + len("chapters:")
    while i < len(contenido) and contenido[i] in (' ', '\t', '\n', '\r'):
        i += 1

    if i >= len(contenido):
        return None

    if contenido[i] == '[':
        # chapters: [] — vacío, necesitamos convertirlo a {}
        return ('array', i)

    if contenido[i] != '{':
        return None

    # Balance de llaves para encontrar el cierre
    depth = 0
    start = i
    while i < len(contenido):
        if contenido[i] == '{':
            depth += 1
        elif contenido[i] == '}':
            depth -= 1
            if depth == 0:
                return ('object', start, i)
        i += 1

    return None


def añadir_capitulo():
    id_manga = input("ID del manga: ")
    num_cap  = input("Número de capítulo: ")
    print("Pega las URLs (una por línea). Termina con una línea vacía:")
    urls = []
    while True:
        linea = input()
        if linea.strip() == "":
            break
        urls.append(linea.strip())

    if not urls:
        print("No ingresaste URLs.")
        return

    bloque_urls = ',\n          '.join([f'"{u}"' for u in urls])

    with open("data/mangas.js", "r+", encoding="utf-8") as f:
        contenido = f.read()

        # Ubicar el manga
        marcador  = f'id: {id_manga},'
        pos_manga = contenido.find(marcador)
        if pos_manga == -1:
            print("Manga no encontrado.")
            return

        # Obtener título para el comentario
        m_titulo = re.search(r'title:\s*"([^"]*)"', contenido[pos_manga:])
        titulo   = m_titulo.group(1) if m_titulo else f"Manga {id_manga}"
        comentario = f'        // {titulo} - cap {num_cap}'

        nuevo_cap = f'{comentario}\n        {num_cap}:[\n          {bloque_urls}\n        ]'

        # Ubicar 'chapters:' dentro de ese manga
        pos_chapters = contenido.find("chapters:", pos_manga)
        if pos_chapters == -1:
            print("No se encontró 'chapters' para ese manga.")
            return

        resultado = encontrar_cierre_chapters(contenido, pos_chapters)

        if resultado is None:
            print("No se pudo parsear el bloque 'chapters'.")
            return

        if resultado[0] == 'array':
            # chapters: []  →  reemplazar por  chapters: { nuevo_cap }
            pos_open  = resultado[1]
            pos_close = contenido.find(']', pos_open)
            reemplazo = f'{{\n{nuevo_cap}\n      }}'
            contenido = contenido[:pos_open] + reemplazo + contenido[pos_close + 1:]

        elif resultado[0] == 'object':
            _, pos_open, pos_close = resultado
            # Buscar el último ']' dentro del bloque (fin del último capítulo)
            ultimo_cierre = contenido.rfind(']', pos_open, pos_close)
            if ultimo_cierre == -1:
                # chapters: {}  vacío
                insercion = f'\n{nuevo_cap}\n      '
                contenido = contenido[:pos_open + 1] + insercion + contenido[pos_open + 1:]
            else:
                # Insertar después del último ']'
                insercion = f',\n{nuevo_cap}'
                contenido = contenido[:ultimo_cierre + 1] + insercion + contenido[ultimo_cierre + 1:]

        # Actualizar chapters_count
        def incrementar_count(m):
            return f'chapters_count: {int(m.group(1)) + 1}'
        # Solo dentro del bloque del manga encontrado
        bloque_manga = contenido[pos_manga:]
        bloque_actualizado = re.sub(r'chapters_count:\s*(\d+)', incrementar_count, bloque_manga, count=1)
        contenido = contenido[:pos_manga] + bloque_actualizado

        f.seek(0)
        f.write(contenido)
        f.truncate()

    print(f"Capítulo {num_cap} agregado correctamente.")


def actualizar_manga():
    id_manga = input("ID del manga a actualizar: ")

    with open("data/mangas.js", "r+", encoding="utf-8") as f:
        contenido = f.read()

        marcador  = f'id: {id_manga},'
        pos_manga = contenido.find(marcador)
        if pos_manga == -1:
            print("Manga no encontrado.")
            return

        # Extraer valores actuales para mostrarlos
        def extraer(campo, patron):
            m = re.search(patron, contenido[pos_manga:])
            return m.group(1) if m else "?"

        titulo   = extraer('title',          r'title:\s*"([^"]*)"')
        genero   = extraer('genre',          r'genre:\s*"([^"]*)"')
        rating   = extraer('rating',         r'rating:\s*([\d.]+)')
        cover    = extraer('cover',          r'cover:\s*"([^"]*)"')
        synopsis = extraer('synopsis',       r'synopsis:\s*"([^"]*)"')

        print(f"\nDeja vacío para mantener el valor actual.")
        print(f"  title:    {titulo}")
        print(f"  genre:    {genero}")
        print(f"  rating:   {rating}")
        print(f"  cover:    {cover}")
        print(f"  synopsis: {synopsis}\n")

        campos = {
            'title':    (input(f"title [{titulo}]: ").strip(),    r'(title:\s*)"([^"]*)"',    True),
            'genre':    (input(f"genre [{genero}]: ").strip(),    r'(genre:\s*)"([^"]*)"',    True),
            'rating':   (input(f"rating [{rating}]: ").strip(),   r'(rating:\s*)([\d.]+)',     False),
            'cover':    (input(f"cover [{cover}]: ").strip(),     r'(cover:\s*)"([^"]*)"',    True),
            'synopsis': (input(f"synopsis [{synopsis}]: ").strip(),r'(synopsis:\s*)"([^"]*)"',True),
        }

        bloque = contenido[pos_manga:]
        for campo, (nuevo_val, patron, es_string) in campos.items():
            if not nuevo_val:
                continue
            if es_string:
                bloque = re.sub(patron, lambda m, v=nuevo_val: f'{m.group(1)}"{v}"', bloque, count=1)
            else:
                bloque = re.sub(patron, lambda m, v=nuevo_val: f'{m.group(1)}{v}', bloque, count=1)

        contenido = contenido[:pos_manga] + bloque
        f.seek(0)
        f.write(contenido)
        f.truncate()

    print("Manga actualizado.")


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
        actualizar_manga()
    elif opcion == "5":
        break
    else:
        print("Opción inválida.")