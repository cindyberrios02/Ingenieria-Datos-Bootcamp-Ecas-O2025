# Ejercicio: Directorio de empleados con diccionarios y diccionarios anidados
# Bootcamp Ingeniería de Datos - Estructuras de Datos Avanzadas

def crear_directorio_empleados():
    """
    Función principal que crea y analiza un directorio de empleados
    siguiendo los pasos especificados en la consigna.
    """
    print("👥 DIRECTORIO DE EMPLEADOS")
    print("=" * 40)
    print("Gestión de empleados usando diccionarios y diccionarios anidados")
    print("Análisis por edad y generación de reportes.\n")
    
    # Paso 1: Crear un diccionario con al menos 5 empleados
    print("📝 Paso 1: Creando directorio con empleados")
    
    empleados = {
        'emp1': {'nombre': 'Ana', 'edad': 28},
        'emp2': {'nombre': 'Luis', 'edad': 35},
        'emp3': {'nombre': 'Carmen', 'edad': 42},
        'emp4': {'nombre': 'Diego', 'edad': 26},
        'emp5': {'nombre': 'Sofía', 'edad': 31},
        'emp6': {'nombre': 'Roberto', 'edad': 45},
        'emp7': {'nombre': 'María', 'edad': 29},
        'emp8': {'nombre': 'Carlos', 'edad': 38}
    }
    
    print("Directorio creado con los siguientes empleados:")
    for emp_id, datos in empleados.items():
        print(f"  {emp_id}: {datos['nombre']}, {datos['edad']} años")
    
    print(f"\nTotal de empleados registrados: {len(empleados)}")
    
    # Paso 2: Usar for y .items() para recorrer cada empleado
    print(f"\n🔍 Paso 2: Recorriendo empleados con for y .items()")
    print("Análisis detallado de cada empleado:")
    
    for emp_id, datos in empleados.items():
        nombre = datos['nombre']
        edad = datos['edad']
        
        # Clasificar por generación
        if edad < 30:
            generacion = "Joven"
        elif edad < 40:
            generacion = "Adulto Joven"
        else:
            generacion = "Adulto"
        
        print(f"  📋 ID: {emp_id}")
        print(f"      Nombre: {nombre}")
        print(f"      Edad: {edad} años")
        print(f"      Generación: {generacion}")
        print(f"      {'✅ Mayor de 30' if edad > 30 else '🔹 30 años o menor'}")
        print("-" * 30)
    
    # Paso 3: Aplicar condición para filtrar según la edad
    print(f"\n🎯 Paso 3: Filtrando empleados mayores de 30 años")
    
    empleados_mayores_30 = []
    empleados_menores_30 = []
    
    print("Aplicando filtro de edad:")
    for emp_id, datos in empleados.items():
        nombre = datos['nombre']
        edad = datos['edad']
        
        if edad > 30:
            empleados_mayores_30.append(nombre)
            estado = "✅ INCLUIDO (Mayor de 30)"
        else:
            empleados_menores_30.append(nombre)
            estado = "❌ EXCLUIDO (30 años o menor)"
        
        print(f"  {nombre} ({edad} años) → {estado}")
    
    # Paso 4: Guardar en lista y contar empleados
    print(f"\n📊 Paso 4: Resultados del análisis")
    
    print("EMPLEADOS MAYORES DE 30 AÑOS:")
    print(f"📋 Lista: {empleados_mayores_30}")
    print(f"📈 Cantidad: {len(empleados_mayores_30)}")
    
    print(f"\nEMPLEADOS DE 30 AÑOS O MENORES:")
    print(f"📋 Lista: {empleados_menores_30}")
    print(f"📈 Cantidad: {len(empleados_menores_30)}")
    
    print(f"\n📊 ESTADÍSTICAS GENERALES:")
    total_empleados = len(empleados)
    porcentaje_mayores = (len(empleados_mayores_30) / total_empleados) * 100
    porcentaje_menores = (len(empleados_menores_30) / total_empleados) * 100
    
    print(f"👥 Total de empleados: {total_empleados}")
    print(f"📈 Mayores de 30: {len(empleados_mayores_30)} ({porcentaje_mayores:.1f}%)")
    print(f"📉 30 años o menor: {len(empleados_menores_30)} ({porcentaje_menores:.1f}%)")
    
    return {
        'empleados': empleados,
        'mayores_30': empleados_mayores_30,
        'menores_30': empleados_menores_30,
        'total': total_empleados
    }


def analisis_avanzado_empleados(datos):
    """
    Función que proporciona análisis estadístico avanzado del directorio.
    
    Args:
        datos (dict): Datos del análisis básico
    """
    print(f"\n📈 ANÁLISIS ESTADÍSTICO AVANZADO")
    print("=" * 45)
    
    empleados = datos['empleados']
    
    # Extraer todas las edades para análisis
    edades = [datos_emp['edad'] for datos_emp in empleados.values()]
    nombres = [datos_emp['nombre'] for datos_emp in empleados.values()]
    
    # Estadísticas básicas
    edad_promedio = sum(edades) / len(edades)
    edad_maxima = max(edades)
    edad_minima = min(edades)
    rango_edades = edad_maxima - edad_minima
    
    print("📊 ESTADÍSTICAS DE EDAD:")
    print(f"   📈 Edad promedio: {edad_promedio:.1f} años")
    print(f"   🔝 Empleado más mayor: {edad_maxima} años")
    print(f"   🔻 Empleado más joven: {edad_minima} años")
    print(f"   📐 Rango de edades: {rango_edades} años")
    
    # Encontrar empleados con edad máxima y mínima
    empleado_mayor = None
    empleado_menor = None
    
    for emp_id, datos_emp in empleados.items():
        if datos_emp['edad'] == edad_maxima:
            empleado_mayor = datos_emp['nombre']
        if datos_emp['edad'] == edad_minima:
            empleado_menor = datos_emp['nombre']
    
    print(f"   👑 Empleado de mayor edad: {empleado_mayor} ({edad_maxima} años)")
    print(f"   🌟 Empleado más joven: {empleado_menor} ({edad_minima} años)")
    
    # Análisis por rangos de edad
    print(f"\n🎯 DISTRIBUCIÓN POR RANGOS DE EDAD:")
    
    rangos = {
        'Jóvenes (20-29)': [],
        'Adultos Jóvenes (30-39)': [],
        'Adultos (40-49)': [],
        'Adultos Mayores (50+)': []
    }
    
    for emp_id, datos_emp in empleados.items():
        nombre = datos_emp['nombre']
        edad = datos_emp['edad']
        
        if 20 <= edad <= 29:
            rangos['Jóvenes (20-29)'].append(f"{nombre} ({edad})")
        elif 30 <= edad <= 39:
            rangos['Adultos Jóvenes (30-39)'].append(f"{nombre} ({edad})")
        elif 40 <= edad <= 49:
            rangos['Adultos (40-49)'].append(f"{nombre} ({edad})")
        else:
            rangos['Adultos Mayores (50+)'].append(f"{nombre} ({edad})")
    
    for rango, empleados_rango in rangos.items():
        cantidad = len(empleados_rango)
        porcentaje = (cantidad / len(empleados)) * 100
        print(f"   📂 {rango}: {cantidad} empleado(s) ({porcentaje:.1f}%)")
        if empleados_rango:
            print(f"      → {', '.join(empleados_rango)}")
    
    # Mediana de edad
    edades_ordenadas = sorted(edades)
    n = len(edades_ordenadas)
    if n % 2 == 0:
        mediana = (edades_ordenadas[n//2 - 1] + edades_ordenadas[n//2]) / 2
    else:
        mediana = edades_ordenadas[n//2]
    
    print(f"\n📊 MEDIANA DE EDAD: {mediana} años")
    print(f"📋 Edades ordenadas: {edades_ordenadas}")


def buscar_empleado(empleados):
    """
    Función para buscar empleados por diferentes criterios.
    
    Args:
        empleados (dict): Diccionario de empleados
    """
    print(f"\n🔍 BÚSQUEDA DE EMPLEADOS")
    print("=" * 30)
    
    while True:
        print(f"\nOpciones de búsqueda:")
        print("1. Buscar por nombre")
        print("2. Buscar por edad específica")
        print("3. Buscar por rango de edad")
        print("0. Volver al menú principal")
        
        try:
            opcion = input("\n👉 Selecciona una opción: ").strip()
            
            if opcion == "0":
                break
            elif opcion == "1":
                nombre_buscar = input("Ingresa el nombre a buscar: ").strip().lower()
                encontrados = []
                
                for emp_id, datos in empleados.items():
                    if nombre_buscar in datos['nombre'].lower():
                        encontrados.append((emp_id, datos))
                
                if encontrados:
                    print(f"✅ Empleados encontrados:")
                    for emp_id, datos in encontrados:
                        print(f"   {emp_id}: {datos['nombre']}, {datos['edad']} años")
                else:
                    print(f"❌ No se encontraron empleados con ese nombre")
            
            elif opcion == "2":
                edad_buscar = int(input("Ingresa la edad a buscar: "))
                encontrados = []
                
                for emp_id, datos in empleados.items():
                    if datos['edad'] == edad_buscar:
                        encontrados.append((emp_id, datos))
                
                if encontrados:
                    print(f"✅ Empleados de {edad_buscar} años:")
                    for emp_id, datos in encontrados:
                        print(f"   {emp_id}: {datos['nombre']}")
                else:
                    print(f"❌ No se encontraron empleados de {edad_buscar} años")
            
            elif opcion == "3":
                edad_min = int(input("Edad mínima: "))
                edad_max = int(input("Edad máxima: "))
                encontrados = []
                
                for emp_id, datos in empleados.items():
                    if edad_min <= datos['edad'] <= edad_max:
                        encontrados.append((emp_id, datos))
                
                if encontrados:
                    print(f"✅ Empleados entre {edad_min} y {edad_max} años:")
                    for emp_id, datos in encontrados:
                        print(f"   {emp_id}: {datos['nombre']}, {datos['edad']} años")
                else:
                    print(f"❌ No se encontraron empleados en ese rango")
            
            else:
                print("❌ Opción no válida")
        
        except ValueError:
            print("❌ Por favor ingresa un número válido")
        except Exception as e:
            print(f"❌ Error: {e}")


def agregar_empleado(empleados):
    """
    Función para agregar nuevos empleados al directorio.
    
    Args:
        empleados (dict): Diccionario de empleados
    """
    print(f"\n➕ AGREGAR NUEVO EMPLEADO")
    print("=" * 30)
    
    try:
        # Generar nuevo ID automáticamente
        ultimo_num = len(empleados)
        nuevo_id = f"emp{ultimo_num + 1}"
        
        nombre = input("Nombre del empleado: ").strip()
        if not nombre:
            print("❌ El nombre no puede estar vacío")
            return empleados
        
        edad = int(input("Edad del empleado: "))
        if edad < 18 or edad > 70:
            print("⚠️ Advertencia: Edad fuera del rango típico laboral (18-70)")
        
        # Agregar al diccionario
        empleados[nuevo_id] = {'nombre': nombre, 'edad': edad}
        
        print(f"✅ Empleado agregado exitosamente:")
        print(f"   ID: {nuevo_id}")
        print(f"   Nombre: {nombre}")
        print(f"   Edad: {edad} años")
        
    except ValueError:
        print("❌ Error: La edad debe ser un número")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
    
    return empleados


def generar_reporte(empleados):
    """
    Función para generar un reporte completo del directorio.
    
    Args:
        empleados (dict): Diccionario de empleados
    """
    print(f"\n📋 REPORTE COMPLETO DEL DIRECTORIO")
    print("=" * 45)
    
    # Información general
    total_empleados = len(empleados)
    edades = [datos['edad'] for datos in empleados.values()]
    
    if not edades:
        print("❌ No hay empleados en el directorio")
        return
    
    edad_promedio = sum(edades) / len(edades)
    
    print(f"📊 INFORMACIÓN GENERAL:")
    print(f"   👥 Total de empleados: {total_empleados}")
    print(f"   📈 Edad promedio: {edad_promedio:.1f} años")
    print(f"   🔝 Edad máxima: {max(edades)} años")
    print(f"   🔻 Edad mínima: {min(edades)} años")
    
    # Lista completa
    print(f"\n📋 LISTA COMPLETA DE EMPLEADOS:")
    empleados_ordenados = sorted(empleados.items(), key=lambda x: x[1]['nombre'])
    
    for i, (emp_id, datos) in enumerate(empleados_ordenados, 1):
        nombre = datos['nombre']
        edad = datos['edad']
        
        # Clasificar por edad
        if edad <= 30:
            categoria = "🔹 Joven"
        elif edad <= 40:
            categoria = "🔸 Adulto Joven"
        else:
            categoria = "🔶 Adulto"
        
        print(f"   {i:2d}. {nombre:<15} | {edad:2d} años | {categoria} | ID: {emp_id}")
    
    # Análisis por filtros
    mayores_30 = [datos['nombre'] for datos in empleados.values() if datos['edad'] > 30]
    menores_igual_30 = [datos['nombre'] for datos in empleados.values() if datos['edad'] <= 30]
    
    print(f"\n🎯 ANÁLISIS POR EDAD:")
    print(f"   ✅ Mayores de 30: {len(mayores_30)} empleados")
    if mayores_30:
        print(f"      → {', '.join(mayores_30)}")
    
    print(f"   🔹 30 años o menor: {len(menores_igual_30)} empleados")
    if menores_igual_30:
        print(f"      → {', '.join(menores_igual_30)}")
    
    # Guardar reporte en archivo (opcional)
    try:
        with open("reporte_empleados.txt", "w", encoding="utf-8") as archivo:
            archivo.write("REPORTE DE EMPLEADOS\n")
            archivo.write("=" * 50 + "\n\n")
            archivo.write(f"Total de empleados: {total_empleados}\n")
            archivo.write(f"Edad promedio: {edad_promedio:.1f} años\n\n")
            
            archivo.write("LISTA DE EMPLEADOS:\n")
            for emp_id, datos in empleados_ordenados:
                archivo.write(f"{datos['nombre']}, {datos['edad']} años (ID: {emp_id})\n")
        
        print(f"\n💾 Reporte guardado en 'reporte_empleados.txt'")
        
    except Exception as e:
        print(f"\n⚠️ No se pudo guardar el reporte: {e}")


def menu_principal():
    """
    Menú principal para gestionar el directorio de empleados.
    """
    empleados = None
    
    while True:
        print(f"\n" + "="*50)
        print("👥 SISTEMA DE DIRECTORIO DE EMPLEADOS")
        print("="*50)
        print("Selecciona una opción:")
        print("1. 📊 Crear directorio y análisis básico")
        print("2. 📈 Análisis estadístico avanzado")
        print("3. 🔍 Buscar empleados")
        print("4. ➕ Agregar nuevo empleado")
        print("5. 📋 Generar reporte completo")
        print("6. 👁️ Mostrar directorio actual")
        print("0. 🚪 Salir")
        print("-" * 50)
        
        try:
            opcion = input("👉 Ingresa tu opción (0-6): ").strip()
            
            if opcion == "0":
                print("👋 ¡Gracias por usar el directorio de empleados!")
                break
            elif opcion == "1":
                datos = crear_directorio_empleados()
                empleados = datos['empleados']
            elif opcion == "2":
                if empleados is None:
                    print("⚠️ Primero debes crear el directorio (opción 1)")
                    continue
                datos = {
                    'empleados': empleados,
                    'mayores_30': [datos['nombre'] for datos in empleados.values() if datos['edad'] > 30],
                    'menores_30': [datos['nombre'] for datos in empleados.values() if datos['edad'] <= 30],
                    'total': len(empleados)
                }
                analisis_avanzado_empleados(datos)
            elif opcion == "3":
                if empleados is None:
                    print("⚠️ Primero debes crear el directorio (opción 1)")
                    continue
                buscar_empleado(empleados)
            elif opcion == "4":
                if empleados is None:
                    print("⚠️ Primero debes crear el directorio (opción 1)")
                    continue
                empleados = agregar_empleado(empleados)
            elif opcion == "5":
                if empleados is None:
                    print("⚠️ Primero debes crear el directorio (opción 1)")
                    continue
                generar_reporte(empleados)
            elif opcion == "6":
                if empleados is None:
                    print("⚠️ Primero debes crear el directorio (opción 1)")
                    continue
                print(f"\n📋 DIRECTORIO ACTUAL:")
                for emp_id, datos in empleados.items():
                    print(f"   {emp_id}: {datos['nombre']}, {datos['edad']} años")
                print(f"Total: {len(empleados)} empleados")
            else:
                print("❌ Opción no válida. Selecciona un número del 0 al 6.")
            
            if opcion != "0":
                input("\n⏸️ Presiona Enter para continuar...")
                
        except KeyboardInterrupt:
            print("\n\n👋 ¡Hasta luego!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            input("\n⏸️ Presiona Enter para continuar...")


if __name__ == "__main__":
    print("🎓 BOOTCAMP INGENIERÍA DE DATOS")
    print("👥 Ejercicio: Directorio de Empleados")
    print("🔍 Uso de diccionarios y diccionarios anidados")
    
    menu_principal()