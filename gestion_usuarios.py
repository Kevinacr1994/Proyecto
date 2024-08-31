import re
from datetime import datetime, timedelta

# Diccionarios para almacenar usuarios, artículos y préstamos
usuarios = {}
catalogo = {}
prestamos = {}
ejemplares_perdidos_danados = {}
reservas = {}

# Función para validar el correo electrónico
def validar_email(email):
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(patron, email) is not None

# Función para validar el número celular
def validar_celular(celular):
    return celular.isdigit() and len(celular) == 10

# Función para verificar la unicidad de la identificación de usuario
def verificar_unicidad_id(identificacion):
    return identificacion not in usuarios

# Función para verificar la unicidad del ID de artículo
def verificar_unicidad_id_articulo(id_articulo):
    return id_articulo not in catalogo

# Función para registrar un usuario
def registrar_usuario():
    identificacion = input("Ingrese la identificación: ")
    if not verificar_unicidad_id(identificacion):
        print("La identificación ya está registrada.")
        return
    
    nombre_completo = input("Ingrese el nombre completo: ")
    direccion = input("Ingrese la dirección física: ")
    celular = input("Ingrese el número celular: ")
    if not validar_celular(celular):
        print("Número de celular inválido.")
        return
    
    email = input("Ingrese el correo electrónico: ")
    if not validar_email(email):
        print("Correo electrónico inválido.")
        return
    
    fecha_nacimiento = input("Ingrese la fecha de nacimiento (DD/MM/AAAA): ")
    ocupacion = input("Ingrese la ocupación o centro de estudios: ")

    usuarios[identificacion] = {
        "nombre_completo": nombre_completo,
        "direccion": direccion,
        "celular": celular,
        "email": email,
        "fecha_nacimiento": fecha_nacimiento,
        "ocupacion": ocupacion
    }

    print("Usuario registrado con éxito.")

# Función para registrar un artículo en el catálogo
def registrar_articulo():
    id_articulo = input("Ingrese el ID del artículo: ")
    if not verificar_unicidad_id_articulo(id_articulo):
        print("El ID del artículo ya está registrado.")
        return

    titulo = input("Ingrese el título completo: ")
    autor = input("Ingrese el autor(es): ")
    anio_publicacion = input("Ingrese el año de publicación: ")
    editorial = input("Ingrese la editorial: ")
    isbn = input("Ingrese el ISBN/ISSN: ")
    palabras_clave = input("Ingrese palabras clave (separadas por comas): ")
    categoria = input("Ingrese la categoría (libro, revista, DVD, etc.): ")
    cantidad_ejemplares = int(input("Ingrese la cantidad de ejemplares: "))

    catalogo[id_articulo] = {
        "titulo": titulo,
        "autor": autor,
        "anio_publicacion": anio_publicacion,
        "editorial": editorial,
        "isbn": isbn,
        "palabras_clave": palabras_clave.split(','),
        "categoria": categoria,
        "cantidad_ejemplares": cantidad_ejemplares
    }

    print("Artículo registrado con éxito.")

# Función para buscar artículos en el catálogo
def buscar_articulo():
    criterio = input("Ingrese el criterio de búsqueda (titulo, autor, categoria, palabras_clave): ")
    valor = input("Ingrese el valor para el criterio de búsqueda: ")
    
    resultados = []
    for id_articulo, detalles in catalogo.items():
        if criterio in detalles:
            if valor in detalles[criterio]:
                resultados.append((id_articulo, detalles))
    
    if resultados:
        print("Resultados de búsqueda:")
        for id_articulo, detalles in resultados:
            print(f"ID: {id_articulo}, Título: {detalles['titulo']}, Autor: {detalles['autor']}, Categoría: {detalles['categoria']}")
    else:
        print("No se encontraron artículos que coincidan con los criterios de búsqueda.")

# Función para registrar un préstamo
def registrar_prestamo():
    identificacion_usuario = input("Ingrese la identificación del usuario: ")
    if identificacion_usuario not in usuarios:
        print("El usuario no está registrado.")
        return

    id_articulo = input("Ingrese el ID del artículo: ")
    if id_articulo not in catalogo:
        print("El artículo no está registrado.")
        return

    numero_ejemplar = input("Ingrese el número de ejemplar: ")
    fecha_prestamo = datetime.now().date()
    fecha_devolucion_estimada = fecha_prestamo + timedelta(days=14)  # Ejemplo de 2 semanas de préstamo

    prestamos[(identificacion_usuario, id_articulo, numero_ejemplar)] = {
        "fecha_prestamo": fecha_prestamo,
        "fecha_devolucion_estimada": fecha_devolucion_estimada
    }

    print("Préstamo registrado con éxito.")

# Función para registrar una devolución
def registrar_devolucion():
    identificacion_usuario = input("Ingrese la identificación del usuario: ")
    id_articulo = input("Ingrese el ID del artículo: ")
    numero_ejemplar = input("Ingrese el número de ejemplar: ")

    clave_prestamo = (identificacion_usuario, id_articulo, numero_ejemplar)
    if clave_prestamo in prestamos:
        fecha_devolucion = datetime.now().date()
        prestamos[clave_prestamo]["fecha_devolucion"] = fecha_devolucion

        # Verificar retraso y calcular multa
        fecha_devolucion_estimada = prestamos[clave_prestamo]["fecha_devolucion_estimada"]
        if fecha_devolucion > fecha_devolucion_estimada:
            dias_retraso = (fecha_devolucion - fecha_devolucion_estimada).days
            multa = dias_retraso * 1.0  # Ejemplo de $1 por día de retraso
            print(f"Multa por retraso: ${multa:.2f}")

        print("Devolución registrada con éxito.")
        del prestamos[clave_prestamo]  # Eliminar el préstamo después de registrar la devolución
    else:
        print("No se encontró el préstamo.")

# Función para marcar ejemplares como perdidos o dañados
def marcar_ejemplar_perdido_danado():
    id_articulo = input("Ingrese el ID del artículo: ")
    numero_ejemplar = input("Ingrese el número de ejemplar: ")
    clave = (id_articulo, numero_ejemplar)
    if clave not in ejemplares_perdidos_danados:
        ejemplares_perdidos_danados[clave] = True
        print("Ejemplar marcado como perdido o dañado.")
    else:
        print("El ejemplar ya está marcado.")

# Función para permitir reservas de artículos
def reservar_articulo():
    identificacion_usuario = input("Ingrese la identificación del usuario: ")
    if identificacion_usuario not in usuarios:
        print("El usuario no está registrado.")
        return

    id_articulo = input("Ingrese el ID del artículo: ")
    if id_articulo not in catalogo:
        print("El artículo no está registrado.")
        return

    reservas[(identificacion_usuario, id_articulo)] = True
    print("Reserva realizada con éxito.")

# Función para generar reportes
def generar_reportes():
    print("\nReportes disponibles:")
    print("1. Artículos más prestados")
    print("2. Usuarios que más utilizan la biblioteca")
    print("3. Artículos perdidos o dañados")
    print("4. Ingresos generados por multas")
    reporte = input("Seleccione el tipo de reporte: ")

    if reporte == "1":
        # Reporte de artículos más prestados (simple conteo de préstamos)
        conteo_articulos = {}
        for (usuario, articulo, _), datos in prestamos.items():
            if articulo in conteo_articulos:
                conteo_articulos[articulo] += 1
            else:
                conteo_articulos[articulo] = 1
        print("Artículos más prestados:")
        for articulo, conteo in sorted(conteo_articulos.items(), key=lambda x: x[1], reverse=True):
            print(f"ID: {articulo}, Cantidad: {conteo}")

    elif reporte == "2":
        # Reporte de usuarios que más utilizan la biblioteca
        conteo_usuarios = {}
        for (usuario, _, _), _ in prestamos.items():
            if usuario in conteo_usuarios:
                conteo_usuarios[usuario] += 1
            else:
                conteo_usuarios[usuario] = 1
        print("Usuarios que más utilizan la biblioteca:")
        for usuario, conteo in sorted(conteo_usuarios.items(), key=lambda x: x[1], reverse=True):
            print(f"ID: {usuario}, Cantidad de préstamos: {conteo}")

    elif reporte == "3":
        # Reporte de artículos perdidos o dañados
        print("Artículos perdidos o dañados:")
        for (articulo, ejemplar), estado in ejemplares_perdidos_danados.items():
            print(f"ID Artículo: {articulo}, Número Ejemplar: {ejemplar}, Estado: {'Perdido/Dañado'}")

    elif reporte == "4":
        # Reporte de ingresos generados por multas
        ingresos_multas = sum(dias_retraso * 1.0 for (usuario, articulo, _), datos in prestamos.items()
                              if 'fecha_devolucion' in datos and datos['fecha_devolucion'] > datos['fecha_devolucion_estimada']
                              for dias_retraso in [(datos['fecha_devolucion'] - datos['fecha_devolucion_estimada']).days])
        print(f"Ingresos generados por multas: ${ingresos_multas:.2f}")

    else:
        print("Reporte no disponible.")

# Función principal
def main():
    while True:
        print("\n1. Registrar un nuevo usuario")
        print("2. Registrar un nuevo artículo en el catálogo")
        print("3. Buscar artículos en el catálogo")
        print("4. Registrar un préstamo")
        print("5. Registrar una devolución")
        print("6. Marcar ejemplar como perdido o dañado")
        print("7. Reservar un artículo")
        print("8. Generar reportes")
        print("9. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registrar_usuario()
        elif opcion == "2":
            registrar_articulo()
        elif opcion == "3":
            buscar_articulo()
        elif opcion == "4":
            registrar_prestamo()
        elif opcion == "5":
            registrar_devolucion()
        elif opcion == "6":
            marcar_ejemplar_perdido_danado()
        elif opcion == "7":
            reservar_articulo()
        elif opcion == "8":
            generar_reportes()
        elif opcion == "9":
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    main()
