# Ejercicio: Análisis de calificaciones con listas, bucles y lógica condicional
# Bootcamp Ingeniería de Datos - Estructuras de Datos y Bucles

def analizar_calificaciones():
    """
    Función principal que ejecuta el análisis completo de calificaciones
    siguiendo los pasos especificados en la consigna.
    """
    print("📚 ANÁLISIS DE CALIFICACIONES")
    print("=" * 40)
    print("Este programa analiza una lista de calificaciones (0-100)")
    print("y proporciona estadísticas básicas y análisis de aprobación.\n")
    
    # Paso 1: Definir una lista con al menos 8 calificaciones
    print("📝 Paso 1: Lista de calificaciones definida")
    calificaciones = [85, 92, 67, 78, 95, 54, 88, 76, 82, 45, 91, 73]
    print(f"Calificaciones ingresadas: {calificaciones}")
    print(f"Total de estudiantes: {len(calificaciones)}")
    
    # Paso 2: Usar un for para recorrer las calificaciones y calcular el total acumulado
    print(f"\n🔢 Paso 2: Calculando total acumulado con bucle for")
    total_acumulado = 0
    
    print("Proceso de acumulación:")
    for i, calificacion in enumerate(calificaciones, 1):
        total_acumulado += calificacion
        print(f"  Estudiante {i}: {calificacion} puntos → Total acumulado: {total_acumulado}")
    
    print(f"Total final acumulado: {total_acumulado} puntos")
    
    # Calcular el promedio general
    promedio_general = total_acumulado / len(calificaciones)
    print(f"Promedio general: {promedio_general:.2f}")
    
    # Paso 3: Sumar condición (if) para contar aprobados y guardar sus notas
    print(f"\n✅ Paso 3: Identificando estudiantes aprobados (nota ≥ 60)")
    aprobados = []
    contador_aprobados = 0
    
    print("Análisis de aprobación:")
    for i, calificacion in enumerate(calificaciones, 1):
        if calificacion >= 60:
            aprobados.append(calificacion)
            contador_aprobados += 1
            estado = "✅ APROBADO"
        else:
            estado = "❌ REPROBADO"
        
        print(f"  Estudiante {i}: {calificacion} puntos → {estado}")
    
    print(f"\nEstudiantes aprobados: {contador_aprobados}")
    print(f"Calificaciones de aprobados: {aprobados}")
    
    # Paso 4: Calcular promedio final y mostrar junto con cantidad de aprobados
    print(f"\n📊 Paso 4: Estadísticas finales")
    promedio_aprobados = sum(aprobados) / len(aprobados) if aprobados else 0
    porcentaje_aprobacion = (contador_aprobados / len(calificaciones)) * 100
    
    print("RESUMEN ESTADÍSTICO:")
    print("-" * 30)
    print(f"📈 Promedio general: {promedio_general:.2f}")
    print(f"✅ Estudiantes aprobados: {contador_aprobados} de {len(calificaciones)}")
    print(f"📋 Lista de notas aprobadas: {aprobados}")
    print(f"🎯 Promedio de aprobados: {promedio_aprobados:.2f}")
    print(f"📊 Porcentaje de aprobación: {porcentaje_aprobacion:.1f}%")
    
    return {
        'calificaciones_originales': calificaciones,
        'total_acumulado': total_acumulado,
        'promedio_general': promedio_general,
        'aprobados': aprobados,
        'contador_aprobados': contador_aprobados,
        'promedio_aprobados': promedio_aprobados,
        'porcentaje_aprobacion': porcentaje_aprobacion
    }


def analisis_avanzado(resultados):
    """
    Función adicional que proporciona análisis estadístico más avanzado.
    
    Args:
        resultados (dict): Resultados del análisis básico
    """
    print(f"\n📈 ANÁLISIS ESTADÍSTICO AVANZADO")
    print("=" * 45)
    
    calificaciones = resultados['calificaciones_originales']
    
    # Estadísticas adicionales
    calificacion_maxima = max(calificaciones)
    calificacion_minima = min(calificaciones)
    rango = calificacion_maxima - calificacion_minima
    
    # Clasificación por rangos
    excelente = [c for c in calificaciones if c >= 90]
    bueno = [c for c in calificaciones if 80 <= c < 90]
    regular = [c for c in calificaciones if 70 <= c < 80]
    deficiente = [c for c in calificaciones if 60 <= c < 70]
    reprobado = [c for c in calificaciones if c < 60]
    
    print("📊 DISTRIBUCIÓN POR RANGOS:")
    print(f"🌟 Excelente (90-100): {len(excelente)} estudiantes → {excelente}")
    print(f"👍 Bueno (80-89): {len(bueno)} estudiantes → {bueno}")
    print(f"😐 Regular (70-79): {len(regular)} estudiantes → {regular}")
    print(f"😕 Deficiente (60-69): {len(deficiente)} estudiantes → {deficiente}")
    print(f"❌ Reprobado (<60): {len(reprobado)} estudiantes → {reprobado}")
    
    print(f"\n📏 ESTADÍSTICAS DESCRIPTIVAS:")
    print(f"🔝 Calificación máxima: {calificacion_maxima}")
    print(f"🔻 Calificación mínima: {calificacion_minima}")
    print(f"📐 Rango: {rango} puntos")
    
    # Mediana
    calificaciones_ordenadas = sorted(calificaciones)
    n = len(calificaciones_ordenadas)
    if n % 2 == 0:
        mediana = (calificaciones_ordenadas[n//2 - 1] + calificaciones_ordenadas[n//2]) / 2
    else:
        mediana = calificaciones_ordenadas[n//2]
    
    print(f"📊 Mediana: {mediana}")
    print(f"📋 Calificaciones ordenadas: {calificaciones_ordenadas}")


def simulacion_interactiva():
    """
    Función que permite al usuario ingresar sus propias calificaciones
    para hacer el análisis de forma interactiva.
    """
    print(f"\n🎮 MODO INTERACTIVO")
    print("=" * 30)
    print("Ingresa tus propias calificaciones para analizar")
    
    calificaciones_usuario = []
    
    print(f"Ingresa al menos 8 calificaciones (0-100). Escribe 'fin' para terminar.")
    
    while len(calificaciones_usuario) < 8 or True:
        try:
            entrada = input(f"Calificación {len(calificaciones_usuario) + 1}: ")
            
            if entrada.lower() == 'fin':
                if len(calificaciones_usuario) >= 8:
                    break
                else:
                    print(f"❌ Necesitas al menos 8 calificaciones. Tienes {len(calificaciones_usuario)}")
                    continue
            
            calificacion = float(entrada)
            
            if 0 <= calificacion <= 100:
                calificaciones_usuario.append(calificacion)
                print(f"✅ Calificación {calificacion} agregada")
            else:
                print("❌ La calificación debe estar entre 0 y 100")
                
        except ValueError:
            print("❌ Por favor ingresa un número válido o 'fin' para terminar")
        except KeyboardInterrupt:
            print(f"\n⏹️ Análisis cancelado")
            return
    
    # Ejecutar análisis con datos del usuario
    print(f"\n🔄 Analizando tus calificaciones...")
    
    # Simular el mismo análisis pero con datos del usuario
    print(f"📝 Calificaciones ingresadas: {calificaciones_usuario}")
    
    # Calcular estadísticas
    total = sum(calificaciones_usuario)
    promedio = total / len(calificaciones_usuario)
    aprobados = [c for c in calificaciones_usuario if c >= 60]
    
    print(f"📊 RESULTADOS:")
    print(f"   Total estudiantes: {len(calificaciones_usuario)}")
    print(f"   Promedio: {promedio:.2f}")
    print(f"   Aprobados: {len(aprobados)} ({(len(aprobados)/len(calificaciones_usuario)*100):.1f}%)")
    print(f"   Calificaciones de aprobados: {aprobados}")


def demo_con_datasets_grandes():
    """
    Función que demuestra el análisis con datasets más grandes
    para simular situaciones reales en ingeniería de datos.
    """
    print(f"\n🏭 DEMO CON DATASETS GRANDES")
    print("=" * 40)
    print("Simulando análisis de calificaciones a escala universitaria")
    
    import random
    
    # Simular calificaciones de una universidad
    print(f"🎓 Generando calificaciones para 1000 estudiantes...")
    
    # Generar datos realistas (distribución normal aproximada)
    calificaciones_universidad = []
    for _ in range(1000):
        # Simular distribución realista de calificaciones
        base = random.choice([
            random.randint(85, 100),  # 20% excelentes
            random.randint(75, 89),   # 30% buenos
            random.randint(65, 79),   # 30% regulares
            random.randint(50, 69),   # 15% deficientes
            random.randint(20, 59)    # 5% reprobados
        ])
        calificaciones_universidad.append(base)
    
    # Análisis rápido con bucles eficientes
    total_universidad = 0
    aprobados_universidad = []
    
    print(f"📊 Procesando {len(calificaciones_universidad)} calificaciones...")
    
    for calificacion in calificaciones_universidad:
        total_universidad += calificacion
        if calificacion >= 60:
            aprobados_universidad.append(calificacion)
    
    promedio_universidad = total_universidad / len(calificaciones_universidad)
    tasa_aprobacion = (len(aprobados_universidad) / len(calificaciones_universidad)) * 100
    
    print(f"✅ RESULTADOS UNIVERSITARIOS:")
    print(f"   📈 Promedio general: {promedio_universidad:.2f}")
    print(f"   ✅ Estudiantes aprobados: {len(aprobados_universidad):,}")
    print(f"   📊 Tasa de aprobación: {tasa_aprobacion:.1f}%")
    print(f"   🔝 Calificación máxima: {max(calificaciones_universidad)}")
    print(f"   🔻 Calificación mínima: {min(calificaciones_universidad)}")
    
    # Análisis por rangos rápido
    rangos = {
        'Excelente (90-100)': len([c for c in calificaciones_universidad if c >= 90]),
        'Bueno (80-89)': len([c for c in calificaciones_universidad if 80 <= c < 90]),
        'Regular (70-79)': len([c for c in calificaciones_universidad if 70 <= c < 80]),
        'Deficiente (60-69)': len([c for c in calificaciones_universidad if 60 <= c < 70]),
        'Reprobado (<60)': len([c for c in calificaciones_universidad if c < 60])
    }
    
    print(f"\n📊 DISTRIBUCIÓN POR RANGOS:")
    for rango, cantidad in rangos.items():
        porcentaje = (cantidad / len(calificaciones_universidad)) * 100
        print(f"   {rango}: {cantidad:,} estudiantes ({porcentaje:.1f}%)")


def menu_principal():
    """
    Menú principal para ejecutar diferentes opciones del análisis de calificaciones.
    """
    while True:
        print(f"\n" + "="*50)
        print("📚 SISTEMA DE ANÁLISIS DE CALIFICACIONES")
        print("="*50)
        print("Selecciona una opción:")
        print("1. 📊 Análisis básico (siguiendo la consigna)")
        print("2. 📈 Análisis avanzado")
        print("3. 🎮 Modo interactivo (ingresa tus calificaciones)")
        print("4. 🏭 Demo con datasets grandes")
        print("5. 🔄 Ejecutar análisis completo")
        print("0. 🚪 Salir")
        print("-" * 50)
        
        try:
            opcion = input("👉 Ingresa tu opción (0-5): ").strip()
            
            if opcion == "0":
                print("👋 ¡Gracias por usar el analizador de calificaciones!")
                break
            elif opcion == "1":
                resultados = analizar_calificaciones()
            elif opcion == "2":
                if 'resultados' not in locals():
                    print("⚠️ Primero ejecuta el análisis básico (opción 1)")
                    resultados = analizar_calificaciones()
                analisis_avanzado(resultados)
            elif opcion == "3":
                simulacion_interactiva()
            elif opcion == "4":
                demo_con_datasets_grandes()
            elif opcion == "5":
                print("🔄 Ejecutando análisis completo...")
                resultados = analizar_calificaciones()
                analisis_avanzado(resultados)
                demo_con_datasets_grandes()
            else:
                print("❌ Opción no válida. Selecciona un número del 0 al 5.")
            
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
    print("📚 Ejercicio: Análisis de Calificaciones")
    print("🔍 Uso de listas, bucles for y lógica condicional")
    
    menu_principal()