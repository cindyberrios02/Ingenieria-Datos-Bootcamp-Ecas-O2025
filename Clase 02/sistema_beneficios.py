def obtener_datos_usuario():
    """
    Función para recopilar los datos del usuario con validaciones.
    """
    print("🏛️ SISTEMA DE BENEFICIOS GUBERNAMENTALES")
    print("=" * 45)
    print("Por favor, ingresa los siguientes datos:\n")
    
    # Obtener nombre con validación
    while True:
        nombre = input("👤 Ingresa tu nombre completo: ").strip()
        if nombre and not nombre.isdigit():
            nombre = nombre.title()  # Capitalizar nombre
            break
        print("❌ Por favor, ingresa un nombre válido.")
    
    # Obtener edad con validación
    while True:
        try:
            edad = int(input("🎂 Ingresa tu edad: "))
            if 0 <= edad <= 120:
                break
            print("❌ Por favor, ingresa una edad válida (0-120 años).")
        except ValueError:
            print("❌ Por favor, ingresa un número válido.")
    
    # Obtener país de residencia
    paises_validos = ["argentina", "chile", "colombia"]
    print("\n🌎 Países disponibles: Argentina, Chile, Colombia")
    
    while True:
        pais = input("🏠 Ingresa tu país de residencia: ").strip().lower()
        if pais in paises_validos:
            pais = pais.capitalize()
            break
        print("❌ País no válido. Solo Argentina, Chile o Colombia.")
    
    return nombre, edad, pais

def verificar_elegibilidad(edad, pais):
    """
    Verifica si la persona es elegible para el beneficio.
    Condiciones: Mayor de 18 años Y vive en Argentina, Chile o Colombia
    """
    es_mayor_edad = edad >= 18
    pais_elegible = pais.lower() in ["argentina", "chile", "colombia"]
    
    return es_mayor_edad and pais_elegible

def calcular_beneficio(edad, pais):
    """
    Calcula el monto del beneficio basado en edad y país.
    """
    # Monto base por país (en USD)
    montos_base = {
        "argentina": 300,
        "chile": 350,
        "colombia": 280
    }
    
    monto_base = montos_base[pais.lower()]
    
    # Bonificaciones por edad
    if edad >= 65:
        bonificacion = monto_base * 0.50  # 50% extra para adultos mayores
        categoria = "Adulto Mayor"
    elif edad >= 45:
        bonificacion = monto_base * 0.25  # 25% extra para adultos de mediana edad
        categoria = "Adulto de Mediana Edad"
    elif edad >= 25:
        bonificacion = monto_base * 0.10  # 10% extra para adultos jóvenes
        categoria = "Adulto Joven"
    else:
        bonificacion = 0
        categoria = "Joven Adulto"
    
    monto_total = monto_base + bonificacion
    
    return monto_total, monto_base, bonificacion, categoria

def mostrar_resultado(nombre, edad, pais, es_elegible):
    """
    Muestra el resultado final del proceso.
    """
    print("\n" + "="*50)
    print("📋 RESULTADO DE LA EVALUACIÓN")
    print("="*50)
    
    print(f"👤 Nombre: {nombre}")
    print(f"🎂 Edad: {edad} años")
    print(f"🏠 País: {pais}")
    print(f"📅 Fecha de evaluación: {obtener_fecha_actual()}")
    
    if es_elegible:
        print("\n✅ ¡FELICITACIONES! Eres elegible para el beneficio.")
        
        # Calcular beneficio
        monto_total, monto_base, bonificacion, categoria = calcular_beneficio(edad, pais)
        
        print(f"\n💰 DETALLES DEL BENEFICIO:")
        print(f"  📊 Categoría: {categoria}")
        print(f"  💵 Monto base ({pais}): ${monto_base:,.2f} USD")
        
        if bonificacion > 0:
            porcentaje = (bonificacion / monto_base) * 100
            print(f"  🎁 Bonificación por edad: ${bonificacion:,.2f} USD (+{porcentaje:.0f}%)")
        else:
            print(f"  🎁 Bonificación por edad: $0.00 USD")
        
        print(f"  🏆 MONTO TOTAL: ${monto_total:,.2f} USD")
        
        # Información adicional según la edad
        mostrar_info_adicional(edad, categoria)
        
    else:
        print("\n❌ Lo sentimos, no cumples con los requisitos para el beneficio.")
        print("\n📋 REQUISITOS:")
        print("  ✓ Ser mayor de 18 años")
        print("  ✓ Residir en Argentina, Chile o Colombia")
        
        # Mostrar qué requisito no cumple
        if edad < 18:
            años_faltantes = 18 - edad
            print(f"\n⏰ Te faltan {años_faltantes} año(s) para ser elegible.")
        
        if pais.lower() not in ["argentina", "chile", "colombia"]:
            print(f"\n🌎 Tu país de residencia ({pais}) no está en la lista de países elegibles.")

def mostrar_info_adicional(edad, categoria):
    """
    Muestra información adicional según la categoría de edad.
    """
    print(f"\n📖 INFORMACIÓN ADICIONAL PARA {categoria.upper()}:")
    
    if edad >= 65:
        print("  🏥 Acceso prioritario a servicios de salud")
        print("  🚌 Descuentos en transporte público")
        print("  🎓 Programas educativos para adultos mayores")
    elif edad >= 45:
        print("  💼 Programas de capacitación laboral")
        print("  🏥 Chequeos médicos preventivos")
        print("  💰 Asesoría financiera gratuita")
    elif edad >= 25:
        print("  🎯 Programas de desarrollo profesional")
        print("  🏠 Asesoría para compra de vivienda")
        print("  👶 Beneficios familiares disponibles")
    else:
        print("  🎓 Becas de estudio disponibles")
        print("  💼 Programas de primer empleo")
        print("  🌟 Mentorías profesionales")

def obtener_fecha_actual():
    """
    Obtiene la fecha actual en formato legible.
    """
    from datetime import datetime
    return datetime.now().strftime("%d/%m/%Y %H:%M")

def mostrar_estadisticas():
    """
    Muestra estadísticas simuladas del programa.
    """
    print("\n📊 ESTADÍSTICAS DEL PROGRAMA (2024)")
    print("-" * 40)
    print("🇦🇷 Argentina: 2,547 beneficiarios")
    print("🇨🇱 Chile: 1,892 beneficiarios") 
    print("🇨🇴 Colombia: 3,156 beneficiarios")
    print("💰 Inversión total: $2,847,350 USD")
    print("📈 Satisfacción promedio: 94.2%")

def continuar_programa():
    """
    Pregunta si el usuario quiere evaluar a otra persona.
    """
    while True:
        respuesta = input("\n🔄 ¿Deseas evaluar a otra persona? (s/n): ").strip().lower()
        if respuesta in ['s', 'si', 'sí', 'y', 'yes']:
            return True
        elif respuesta in ['n', 'no']:
            return False
        print("❌ Por favor, responde 's' para sí o 'n' para no.")

def main():
    """
    Función principal del programa.
    """
    print("🌟 BIENVENIDO AL SISTEMA DE BENEFICIOS GUBERNAMENTALES")
    print("🎯 Verificaremos tu elegibilidad para recibir apoyo económico")
    print("⚡ Desarrollado para el Bootcamp de Ingeniería de Datos\n")
    
    # Contador de evaluaciones
    total_evaluaciones = 0
    elegibles = 0
    no_elegibles = 0
    
    while True:
        # Obtener datos del usuario
        nombre, edad, pais = obtener_datos_usuario()
        
        # Verificar elegibilidad
        es_elegible = verificar_elegibilidad(edad, pais)
        
        # Mostrar resultado
        mostrar_resultado(nombre, edad, pais, es_elegible)
        
        # Actualizar contadores
        total_evaluaciones += 1
        if es_elegible:
            elegibles += 1
        else:
            no_elegibles += 1
        
        # Preguntar si continuar
        if not continuar_programa():
            break
        
        print("\n" + "="*60 + "\n")
    
    # Mostrar resumen de la sesión
    print("\n🎯 RESUMEN DE LA SESIÓN")
    print("=" * 30)
    print(f"📊 Total de evaluaciones: {total_evaluaciones}")
    print(f"✅ Personas elegibles: {elegibles}")
    print(f"❌ Personas no elegibles: {no_elegibles}")
    
    if total_evaluaciones > 0:
        porcentaje_elegibles = (elegibles / total_evaluaciones) * 100
        print(f"📈 Porcentaje de elegibilidad: {porcentaje_elegibles:.1f}%")
    
    # Mostrar estadísticas generales
    mostrar_estadisticas()
    
    print(f"\n🙏 ¡Gracias por usar el Sistema de Beneficios!")
    print(f"💡 Ejercicio completado - Clase 02 del Bootcamp")
   

if __name__ == "__main__":
    main()