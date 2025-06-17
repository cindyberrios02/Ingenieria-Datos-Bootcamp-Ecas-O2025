def ejercicio_listas():
    """Ejercicios básicos con listas."""
    print("🔢 EJERCICIOS CON LISTAS")
    print("=" * 30)
    
    # Lista de estudiantes del bootcamp
    estudiantes = ["Ana", "Carlos", "María", "Pedro", "Lucia"]
    print(f"Estudiantes originales: {estudiantes}")
    
    # Agregar nuevos estudiantes
    estudiantes.append("Diego")
    estudiantes.extend(["Sofía", "Miguel"])
    print(f"Después de agregar: {estudiantes}")
    
    # Eliminar un estudiante
    estudiantes.remove("Pedro")
    print(f"Después de eliminar a Pedro: {estudiantes}")
    
    # Operaciones útiles
    print(f"Total de estudiantes: {len(estudiantes)}")
    print(f"Primer estudiante: {estudiantes[0]}")
    print(f"Último estudiante: {estudiantes[-1]}")
    print(f"Estudiantes ordenados: {sorted(estudiantes)}")
    
    return estudiantes

def ejercicio_diccionarios():
    """Ejercicios básicos con diccionarios."""
    print("\n📚 EJERCICIOS CON DICCIONARIOS")
    print("=" * 35)
    
    # Diccionario de un estudiante del bootcamp
    estudiante = {
        "nombre": "Ana García",
        "edad": 25,
        "especialidad": "Ingeniería de Datos",
        "skills": ["Python", "SQL", "Pandas"],
        "activo": True
    }
    
    print("Información del estudiante:")
    for clave, valor in estudiante.items():
        print(f"  {clave}: {valor}")
    
    # Agregar nueva información
    estudiante["universidad"] = "Universidad Nacional"
    estudiante["promedio"] = 8.7
    
    # Modificar skills
    estudiante["skills"].append("Machine Learning")
    
    print(f"\nSkills actualizadas: {estudiante['skills']}")
    print(f"Promedio: {estudiante['promedio']}")
    
    return estudiante

def ejercicio_combinado():
    """Combinando listas y diccionarios."""
    print("\n🔄 COMBINANDO ESTRUCTURAS")
    print("=" * 30)
    
    # Lista de diccionarios - Base de datos de estudiantes
    bootcamp_students = [
        {"nombre": "Ana", "edad": 25, "especialidad": "Data Engineering", "promedio": 8.7},
        {"nombre": "Carlos", "edad": 28, "especialidad": "Data Science", "promedio": 9.1},
        {"nombre": "María", "edad": 24, "especialidad": "Data Analytics", "promedio": 8.9},
        {"nombre": "Pedro", "edad": 26, "especialidad": "Data Engineering", "promedio": 8.5}
    ]
    
    # Análisis de datos básico
    total_estudiantes = len(bootcamp_students)
    suma_edades = sum(est["edad"] for est in bootcamp_students)
    promedio_edad = suma_edades / total_estudiantes
    
    suma_promedios = sum(est["promedio"] for est in bootcamp_students)
    promedio_general = suma_promedios / total_estudiantes
    
    print(f"📊 ESTADÍSTICAS DEL BOOTCAMP")
    print(f"Total de estudiantes: {total_estudiantes}")
    print(f"Edad promedio: {promedio_edad:.1f} años")
    print(f"Promedio general: {promedio_general:.2f}")
    
    # Filtrar por especialidad
    data_engineers = [est for est in bootcamp_students if est["especialidad"] == "Data Engineering"]
    print(f"\nEstudiantes de Data Engineering: {len(data_engineers)}")
    for eng in data_engineers:
        print(f"  - {eng['nombre']} (Promedio: {eng['promedio']})")
    
    return bootcamp_students

def main():
    """Función principal."""
    print("🎓 BOOTCAMP INGENIERÍA DE DATOS - EJERCICIO 02")
    print("=" * 50)
    
    estudiantes = ejercicio_listas()
    estudiante = ejercicio_diccionarios()
    bootcamp_data = ejercicio_combinado()
    
    print(f"\n✅ ¡Ejercicio completado exitosamente!")

if __name__ == "__main__":
    main()