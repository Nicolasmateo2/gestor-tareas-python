import json
import os

TASKS_FILE = "tasks.json"

# Función para cargar tareas desde JSON
def cargar_tareas():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r") as file:
        return json.load(file)

# Función para guardar tareas en JSON
def guardar_tareas(tareas):
    with open(TASKS_FILE, "w") as file:
        json.dump(tareas, file, indent=4)

# Función para agregar tareas
def agregar_tarea(nombre, prioridad):
    tareas = cargar_tareas()
    nueva_tarea = {"id": len(tareas) + 1, "nombre": nombre, "prioridad": prioridad, "completada": False}
    tareas.append(nueva_tarea)
    guardar_tareas(tareas)
    print(f"✅ Tarea '{nombre}' agregada con prioridad {prioridad}.")

# Función para mostrar todas las tareas
def listar_tareas():
    tareas = cargar_tareas()
    if not tareas:
        print("📭 No hay tareas registradas.")
        return
    
    print("\n📋 Lista de tareas:")
    for tarea in tareas:
        estado = "✔️" if tarea["completada"] else "❌"
        print(f"{tarea['id']}. {tarea['nombre']} - Prioridad: {tarea['prioridad']} - Estado: {estado}")

# Función para eliminar una tarea y reorganizar los IDs
def eliminar_tarea(id_tarea):
    tareas = cargar_tareas()
    tarea_encontrada = False

    # Filtrar la tarea a eliminar
    nuevas_tareas = [tarea for tarea in tareas if tarea["id"] != id_tarea]

    if len(nuevas_tareas) < len(tareas):
        tarea_encontrada = True
        print(f"🗑️ Tarea con ID {id_tarea} eliminada correctamente.")

        # Reasignar IDs para que sean consecutivos
        for index, tarea in enumerate(nuevas_tareas, start=1):
            tarea["id"] = index  # Nuevo ID ordenado

        guardar_tareas(nuevas_tareas)  # Guardar cambios
    else:
        print(f"⚠️ No se encontró ninguna tarea con ID {id_tarea}.")


# Función para editar una tarea (nombre y prioridad)
def editar_tarea(id_tarea):
    tareas = cargar_tareas()
    tarea_encontrada = False

    for tarea in tareas:
        if tarea["id"] == id_tarea:
            print(f"\n📝 Editando tarea: {tarea['nombre']} (Prioridad: {tarea['prioridad']})")

            # Solicitar nuevo nombre (o dejar el mismo si se presiona Enter)
            nuevo_nombre = input("Nuevo nombre de la tarea (Enter para mantener el actual): ").strip()
            if nuevo_nombre:
                tarea["nombre"] = nuevo_nombre

            # Solicitar nueva prioridad
            nueva_prioridad = input("Nueva prioridad (Alta/Media/Baja, Enter para mantener la actual): ").strip().capitalize()
            if nueva_prioridad in ["Alta", "Media", "Baja"]:
                tarea["prioridad"] = nueva_prioridad

            print(f"✅ Tarea actualizada: {tarea['nombre']} (Prioridad: {tarea['prioridad']})")
            tarea_encontrada = True
            break

    if not tarea_encontrada:
        print(f"⚠️ No se encontró ninguna tarea con ID {id_tarea}.")
    else:
        guardar_tareas(tareas)  # Guardamos los cambios en el archivo JSON


# Función para cambiar el estado de una tarea
def cambiar_estado_tarea(id_tarea):
    tareas = cargar_tareas()
    tarea_encontrada = False

    for tarea in tareas:
        if tarea["id"] == id_tarea:
            tarea["completada"] = not tarea["completada"]  # Alternar estado
            estado = "✅ Completada" if tarea["completada"] else "❌ Pendiente"
            print(f"🔄 Estado de la tarea '{tarea['nombre']}' cambiado a: {estado}")
            tarea_encontrada = True
            break

    if not tarea_encontrada:
        print(f"⚠️ No se encontró ninguna tarea con ID {id_tarea}.")
    else:
        guardar_tareas(tareas)  # Guardamos los cambios en el archivo JSON


# Función principal
def main():
    tareas = cargar_tareas()
    while True:
        print("\nGestor de Tareas - Opciones:")
        print("1. Agregar tarea")
        print("2. Cambiar el estado de una tarea")
        print("3. Listar tareas")
        print("4. Editar tarea")
        print("5. Eliminar tarea")
        print("6. Salir")
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            nombre = input("Nombre de la tarea: ")
            prioridad = input("Prioridad (Alta/Media/Baja): ")
            agregar_tarea(nombre, prioridad)
        elif opcion == "2":
            listar_tareas()
            try:
                id_tarea = int(input("Ingrese el ID de la tarea para cambiar su estado: "))
                cambiar_estado_tarea(id_tarea)
            except ValueError:
                print("⚠️ Error: Ingresa un número válido.")
        elif opcion == "3":
            listar_tareas()
        elif opcion == "4":
            listar_tareas()
            try:
                id_tarea = int(input("Ingrese el ID de la tarea a editar: "))
                editar_tarea(id_tarea)
            except ValueError:
                print("⚠️ Error: Ingresa un número válido.")
        elif opcion == "5":
            listar_tareas()  # Mostrar tareas antes de eliminar
            try:
                id_tarea = int(input("Ingrese el ID de la tarea a eliminar: "))
                eliminar_tarea(id_tarea)
            except ValueError:
                print("⚠️ Error: Ingresa un número válido.")
        elif opcion == "6":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Inténtalo de nuevo.")

if __name__ == "__main__":
    main()