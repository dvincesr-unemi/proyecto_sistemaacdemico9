from shared.herramientas import (
    imprimir_titulo, imprimir_exito, imprimir_error, imprimir_info, confirmar
)
# 1. Importamos PrerrequisitoController junto a los demas controladores
from views import (
    EstudianteController, MateriaController, PrerrequisitoController, MatriculaController
)

# ---------------------------------------------------------------------
# INYECCION DE DEPENDENCIAS
# ---------------------------------------------------------------------
estudiantes = EstudianteController()
materias = MateriaController()

# Prerrequisitos necesita conocer las materias para validar que existan
prerrequisitos = PrerrequisitoController(materias)

# Matriculas recibe estudiantes, materias y PRERREQUISITOS (para bloqueo academico)
matriculas = MatriculaController(estudiantes, materias, prerrequisitos)


# ---------------------------------------------------------------------
# AYUDAS DE PANTALLA
# ---------------------------------------------------------------------

def pausa() -> None:
    """
    Detiene la ejecucion hasta que el usuario presione Enter.
    """
    input("\nPresione Enter para continuar...")


def pedir_entero(etiqueta: str) -> int:
    """
    Devuelve un entero o None si el usuario escribio otra cosa.
    """
    try:
        return int(input(etiqueta))
    except ValueError:
        return None


def mostrar_resultado(exito: bool, mensaje: str) -> None:
    """
    Imprime en color verde si es exito o rojo si es error.
    """
    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)


def mostrar_lista(objetos: list, vacio: str = "No hay registros todavia.") -> None:
    """
    Sirve para todos los modelos usando polimorfismo en su metodo __str__.
    """
    if not objetos:
        imprimir_info(vacio)
        return
    for objeto in objetos:
        print(f"  {objeto}")
    imprimir_info(f"Total: {len(objetos)}")


def mostrar_detalle(objeto: object) -> None:
    """
    Muestra los campos internos de un objeto a partir de su diccionario.
    """
    for clave, valor in objeto.a_diccionario().items():
        print(f"  {str(clave).replace('_', ' ').capitalize():<16}: {valor}")


# ---------------------------------------------------------------------
# MENU DE MALLA CURRICULAR (PRERREQUISITOS)
# ---------------------------------------------------------------------

def crear_prerrequisito() -> None:
    """Crea una regla de bloqueo academico entre dos materias."""
    imprimir_titulo("NUEVO PRERREQUISITO")
    imprimir_info("Materias registradas:")
    mostrar_lista(materias.leer(), "No hay materias en el sistema.")

    datos = {
        "materia_id": pedir_entero("\nId de la materia a cursar: "),
        "materia_requisito_id": pedir_entero("Id de la materia que debe estar aprobada previamente: ")
    }
    
    if datos["materia_id"] is None or datos["materia_requisito_id"] is None:
        imprimir_error("Los IDs deben ser numeros enteros.")
        return pausa()

    mostrar_resultado(*prerrequisitos.crear(datos))
    pausa()


def listar_prerrequisitos() -> None:
    """Lista todas las reglas de la malla curricular."""
    imprimir_titulo("MALLA CURRICULAR (REGLAS DE BLOQUEO)")
    mostrar_lista(prerrequisitos.leer(), "No hay prerrequisitos registrados.")
    pausa()


def ver_prerrequisito() -> None:
    """Muestra el detalle y resuelve los nombres de las materias involucradas."""
    imprimir_titulo("VER REGLA POR ID")
    id_regla = pedir_entero("Id de la regla: ")
    if id_regla is None:
        imprimir_error("Debe ingresar un numero.")
        return pausa()

    regla = prerrequisitos.obtener(id_regla)
    if regla is None:
        imprimir_error("No encontrado")
    else:
        mostrar_detalle(regla)
        mat_destino = materias.obtener(regla.materia_id)
        mat_req = materias.obtener(regla.materia_requisito_id)
        
        n_destino = mat_destino.nombre if mat_destino else "Materia Eliminada"
        n_req = mat_req.nombre if mat_req else "Materia Eliminada"
        
        print(f"\n  Resumen: Para ver '{n_destino}', se debe aprobar primero '{n_req}'")
    pausa()


def actualizar_prerrequisito() -> None:
    """Permite cambiar las IDs asociadas a la regla."""
    imprimir_titulo("ACTUALIZAR REGLA")
    id_regla = pedir_entero("Id de la regla: ")
    if id_regla is None:
        return pausa()

    regla = prerrequisitos.obtener(id_regla)
    if regla is None:
        imprimir_error("No encontrado")
        return pausa()

    imprimir_info(f"Editando: {regla.etiqueta()}")
    
    cambios = {}
    materia_id = pedir_entero(f"Nuevo Id materia a cursar [{regla.materia_id}] (0 para no cambiar): ")
    req_id = pedir_entero(f"Nuevo Id materia previa [{regla.materia_requisito_id}] (0 para no cambiar): ")
    
    if materia_id: 
        cambios["materia_id"] = materia_id
    if req_id: 
        cambios["materia_requisito_id"] = req_id

    mostrar_resultado(*prerrequisitos.actualizar(id_regla, cambios))
    pausa()


def eliminar_prerrequisito() -> None:
    """Elimina la regla y libera la inscripcion para esa materia."""
    imprimir_titulo("ELIMINAR REGLA CURRICULAR")
    id_regla = pedir_entero("Id de la regla: ")
    if id_regla is None:
        return pausa()

    regla = prerrequisitos.obtener(id_regla)
    if regla is None:
        imprimir_error("No encontrado")
        return pausa()

    imprimir_info(f"Se eliminara: {regla.etiqueta()}")
    if confirmar("¿Confirma anular esta regla?"):
        mostrar_resultado(*prerrequisitos.eliminar(id_regla))
    else:
        imprimir_info("Operacion cancelada")
    pausa()


# ---------------------------------------------------------------------
# MENU DE ESTUDIANTES
# ---------------------------------------------------------------------

def crear_estudiante() -> None:
    imprimir_titulo("CREAR ESTUDIANTE")
    datos = {
        "nombre": input("Nombre: "),
        "apellido": input("Apellido: "),
        "email": input("Email: "),
        "carnet": input("Carnet: "),
        "carrera": input("Carrera: "),
    }
    mostrar_resultado(*estudiantes.crear(datos))
    pausa()

def listar_estudiantes() -> None:
    imprimir_titulo("ESTUDIANTES")
    mostrar_lista(estudiantes.leer(), "Todavia no hay estudiantes registrados.")
    pausa()

def buscar_estudiante() -> None:
    imprimir_titulo("BUSCAR ESTUDIANTE")
    termino = input("Nombre, apellido, email, carnet o carrera: ")
    encontrados = estudiantes.buscar(termino)
    mostrar_lista(encontrados, f"Ningun estudiante coincide con '{termino}'.")
    pausa()

def ver_estudiante() -> None:
    imprimir_titulo("VER ESTUDIANTE POR ID")
    estudiante = estudiantes.obtener(pedir_entero("Id: "))
    if estudiante is None:
        imprimir_error("No encontrado")
    else:
        mostrar_detalle(estudiante)
    pausa()

def actualizar_estudiante() -> None:
    imprimir_titulo("ACTUALIZAR ESTUDIANTE")
    id_estudiante = pedir_entero("Id: ")
    if id_estudiante is None:
        return pausa()

    estudiante = estudiantes.obtener(id_estudiante)
    if estudiante is None:
        imprimir_error("No encontrado")
        return pausa()

    imprimir_info(f"Editando: {estudiante.etiqueta()}")
    print("Deje en blanco lo que no quiera cambiar.\n")

    cambios = {}
    for campo in ("nombre", "apellido", "email", "carnet", "carrera"):
        actual = getattr(estudiante, campo)
        nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()
        if nuevo:
            cambios[campo] = nuevo

    mostrar_resultado(*estudiantes.actualizar(id_estudiante, cambios))
    pausa()

def eliminar_estudiante() -> None:
    imprimir_titulo("ELIMINAR ESTUDIANTE")
    id_estudiante = pedir_entero("Id: ")
    if id_estudiante is None:
        return pausa()

    estudiante = estudiantes.obtener(id_estudiante)
    if estudiante is None:
        imprimir_error("No encontrado")
        return pausa()

    imprimir_info(f"Se eliminara: {estudiante.etiqueta()}")
    if confirmar("¿Confirma?"):
        mostrar_resultado(*estudiantes.eliminar(id_estudiante))
    else:
        imprimir_info("Operacion cancelada")
    pausa()


# ---------------------------------------------------------------------
# MENU DE MATERIAS
# ---------------------------------------------------------------------

def crear_materia() -> None:
    imprimir_titulo("CREAR MATERIA")
    datos = {
        "nombre": input("Nombre: "),
        "codigo": input("Codigo: "),
        "creditos": input("Creditos: "),
        "cupos": input("Cupos iniciales [Enter = 30]: "),
    }
    mostrar_resultado(*materias.crear(datos))
    pausa()

def listar_materias() -> None:
    imprimir_titulo("MATERIAS")
    mostrar_lista(materias.leer(), "Todavia no hay materias creadas.")
    pausa()

def buscar_materia() -> None:
    imprimir_titulo("BUSCAR MATERIA")
    termino = input("Nombre o codigo: ")
    mostrar_lista(materias.buscar(termino), "Sin coincidencias.")
    pausa()

def ver_materia() -> None:
    imprimir_titulo("VER MATERIA POR ID")
    materia = materias.obtener(pedir_entero("Id: "))
    if materia is None:
        imprimir_error("No encontrado")
    else:
        mostrar_detalle(materia)
    pausa()

def actualizar_materia() -> None:
    imprimir_titulo("ACTUALIZAR MATERIA")
    id_materia = pedir_entero("Id: ")
    if id_materia is None:
        return pausa()

    materia = materias.obtener(id_materia)
    if materia is None:
        imprimir_error("No encontrado")
        return pausa()

    imprimir_info(f"Editando: {materia.etiqueta()}")
    print("Deje en blanco lo que no quiera cambiar.\n")

    cambios = {}
    for campo in ("nombre", "codigo", "creditos", "cupos"):
        actual = getattr(materia, campo)
        nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()
        if nuevo:
            cambios[campo] = nuevo

    mostrar_resultado(*materias.actualizar(id_materia, cambios))
    pausa()

def eliminar_materia() -> None:
    imprimir_titulo("ELIMINAR MATERIA")
    id_materia = pedir_entero("Id: ")
    if id_materia is None:
        return pausa()

    materia = materias.obtener(id_materia)
    if materia is None:
        imprimir_error("No encontrado")
        return pausa()

    imprimir_info(f"Se eliminara: {materia.etiqueta()}")
    if confirmar("¿Confirma?"):
        mostrar_resultado(*materias.eliminar(id_materia))
    else:
        imprimir_info("Operacion cancelada")
    pausa()


# ---------------------------------------------------------------------
# MENU DE MATRICULAS (BLOQUEO POR MALLA CURRICULAR INCLUIDO)
# ---------------------------------------------------------------------

def registrar_matricula() -> None:
    imprimir_titulo("REGISTRAR MATRICULA")
    imprimir_info("Estudiantes:")
    mostrar_lista(estudiantes.leer())
    imprimir_info("Materias:")
    mostrar_lista(materias.leer())

    datos = {
        "estudiante_id": pedir_entero("\nId del estudiante: "),
        "materia_id": pedir_entero("Id de la materia a inscribir: "),
        "periodo": input("Periodo (ej. 2026-1): "),
    }
    
    if datos["estudiante_id"] is None or datos["materia_id"] is None:
        imprimir_error("Los IDs deben ser numeros enteros")
        return pausa()

    # Aqui el controlador validara la regla del prerrequisito automaticamente
    mostrar_resultado(*matriculas.crear(datos))
    pausa()


def listar_matriculas() -> None:
    imprimir_titulo("MATRICULAS ACTIVAS")
    mostrar_lista(matriculas.leer(), "Todavia no hay inscripciones.")
    pausa()


def asentar_calificacion() -> None:
    imprimir_titulo("ASENTAR CALIFICACION")
    id_matricula = pedir_entero("Id de la matricula: ")
    if not id_matricula:
        return pausa()
        
    nota = input("Ingrese la nota (0 a 20): ")
    mostrar_resultado(*matriculas.actualizar(id_matricula, {"nota": nota}))
    pausa()


def ver_reporte() -> None:
    imprimir_titulo("REPORTE ACADEMICO")
    texto = matriculas.reporte_academico(pedir_entero("Id del estudiante: "))
    if texto is None:
        imprimir_error("El estudiante no existe.")
    else:
        print(texto)
    pausa()


def anular_matricula() -> None:
    imprimir_titulo("ANULAR MATRICULA")
    id_matricula = pedir_entero("Id de la matricula: ")
    if id_matricula is None:
        return pausa()

    matricula = matriculas.obtener(id_matricula)
    if matricula is None:
        imprimir_error(f"No existe la matricula con ID {id_matricula}.")
        return pausa()

    imprimir_info(f"Se anulara: {matricula.etiqueta()}")
    if confirmar("Se liberara el cupo en la materia. ¿Confirma?"):
        mostrar_resultado(*matriculas.eliminar(id_matricula))
    else:
        imprimir_info("Operacion cancelada")
    pausa()


# ---------------------------------------------------------------------
# RESUMEN GENERAL
# ---------------------------------------------------------------------

def resumen() -> None:
    imprimir_titulo("RESUMEN GENERAL")
    print(f"  Estudiantes    : {len(estudiantes.leer())}")
    print(f"  Carreras       : {', '.join(estudiantes.carreras_registradas()) or '-'}")
    print(f"  Materias       : {len(materias.leer())}")
    
    llenas = [m for m in materias.leer() if not m.hay_cupo()]
    print(f"  Sin cupos      : {', '.join(m.codigo for m in llenas) or 'ninguna'}")
    
    print(f"  Prerrequisitos : {len(prerrequisitos.leer())} reglas activas")
    print(f"  Matriculas     : {len(matriculas.leer())}")
    pausa()


# ---------------------------------------------------------------------
# MENUS Y BUCLE PRINCIPAL
# ---------------------------------------------------------------------

MENU_ESTUDIANTES = {
    "1": ("Crear estudiante", crear_estudiante),
    "2": ("Ver todos", listar_estudiantes),
    "3": ("Buscar", buscar_estudiante),
    "4": ("Ver por id", ver_estudiante),
    "5": ("Actualizar", actualizar_estudiante),
    "6": ("Eliminar", eliminar_estudiante),
    "0": ("Volver", None),
}

MENU_MATERIAS = {
    "1": ("Crear materia", crear_materia),
    "2": ("Ver todas", listar_materias),
    "3": ("Buscar", buscar_materia),
    "4": ("Ver por id", ver_materia),
    "5": ("Actualizar", actualizar_materia),
    "6": ("Eliminar", eliminar_materia),
    "0": ("Volver", None),
}

MENU_MALLA = {
    "1": ("Crear regla de prerrequisito", crear_prerrequisito),
    "2": ("Ver todas las reglas", listar_prerrequisitos),
    "3": ("Ver detalle de regla por id", ver_prerrequisito),
    "4": ("Actualizar regla", actualizar_prerrequisito),
    "5": ("Eliminar regla", eliminar_prerrequisito),
    "0": ("Volver", None),
}

MENU_MATRICULAS = {
    "1": ("Inscribir estudiante", registrar_matricula),
    "2": ("Ver todas", listar_matriculas),
    "3": ("Asentar calificacion", asentar_calificacion),
    "4": ("Ver reporte academico", ver_reporte),
    "5": ("Anular matricula", anular_matricula),
    "0": ("Volver", None),
}


def ejecutar_menu(titulo: str, opciones: dict) -> None:
    while True:
        imprimir_titulo(titulo)
        for tecla, (texto, _funcion) in opciones.items():
            print(f"  {tecla}. {texto}")
        print()

        tecla = input("Opcion: ").strip()
        if tecla not in opciones:
            imprimir_error("Opcion no valida")
            pausa()
            continue

        _texto, funcion = opciones[tecla]
        if funcion is None:
            break
        funcion()


def main() -> None:
    while True:
        imprimir_titulo("SISTEMA ACADEMICO")
        print("  1. Estudiantes")
        print("  2. Materias")
        print("  3. Malla Curricular (Prerrequisitos)")  # <--- NUEVA OPCION
        print("  4. Matriculas")
        print("  5. Resumen")
        print("  0. Salir\n")

        tecla = input("Opcion: ").strip()
        if tecla == "1":
            ejecutar_menu("GESTION DE ESTUDIANTES", MENU_ESTUDIANTES)
        elif tecla == "2":
            ejecutar_menu("GESTION DE MATERIAS", MENU_MATERIAS)
        elif tecla == "3":
            ejecutar_menu("MALLA CURRICULAR", MENU_MALLA)
        elif tecla == "4":
            ejecutar_menu("GESTION DE MATRICULAS", MENU_MATRICULAS)
        elif tecla == "5":
            resumen()
        elif tecla == "0":
            imprimir_info("¡Hasta luego! 👋")
            break
        else:
            imprimir_error("Opcion no valida")
            pausa()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nPrograma interrumpido por el usuario.")