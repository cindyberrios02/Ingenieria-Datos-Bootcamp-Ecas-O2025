import utilidades_matematicas as util_math
import math


def mostrar_menu():
    """Muestra el menú principal de opciones."""
    print("\n🧮 CALCULADORA MATEMÁTICA AVANZADA")
    print("=" * 40)
    print("Selecciona una opción:")
    print("1. 📐 Calcular área de círculo")
    print("2. 📱 Calcular área de rectángulo") 
    print("3. 📐 Calcular área de triángulo")
    print("4. 🔢 Calcular factorial")
    print("5. 🔍 Verificar si un número es primo")
    print("6. 🔶 Calcular área de polígono regular (PLUS)")
    print("7. 📊 Información completa de círculo")
    print("8. 📋 Lista de números primos")
    print("9. 📏 Calcular hipotenusa")
    print("10. 🔢 Mostrar constantes matemáticas")
    print("11. 🧪 Ejecutar todas las pruebas")
    print("0. ❌ Salir")
    print("-" * 40)


def obtener_numero(mensaje, tipo=float, minimo=None):
    """
    Obtiene un número del usuario con validación.
    
    Args:
        mensaje (str): Mensaje a mostrar al usuario
        tipo (type): Tipo de dato esperado (int o float)
        minimo (float): Valor mínimo permitido
        
    Returns:
        number: Número validado del tipo especificado
    """
    while True:
        try:
            valor = tipo(input(mensaje))
            if minimo is not None and valor < minimo:
                print(f"❌ El valor debe ser mayor o igual a {minimo}")
                continue
            return valor
        except ValueError:
            tipo_nombre = "entero" if tipo == int else "número"
            print(f"❌ Por favor, ingresa un {tipo_nombre} válido.")


def calcular_area_circulo():
    """Función para calcular el área de un círculo."""
    print("\n📐 CÁLCULO DE ÁREA DE CÍRCULO")
    print("-" * 30)
    
    try:
        radio = obtener_numero("🔸 Ingresa el radio del círculo: ", float, 0)
        area = util_math.area_circulo(radio)
        
        print(f"\n✅ RESULTADO:")
        print(f"   Radio: {radio}")
        print(f"   Área: {area:.4f} unidades²")
        print(f"   Área (redondeada): {area:.2f} unidades²")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def calcular_area_rectangulo():
    """Función para calcular el área de un rectángulo."""
    print("\n📱 CÁLCULO DE ÁREA DE RECTÁNGULO")
    print("-" * 35)
    
    try:
        ancho = obtener_numero("🔸 Ingresa el ancho: ", float, 0)
        alto = obtener_numero("🔸 Ingresa el alto: ", float, 0)
        area = util_math.area_rectangulo(ancho, alto)
        
        print(f"\n✅ RESULTADO:")
        print(f"   Ancho: {ancho}")
        print(f"   Alto: {alto}")
        print(f"   Área: {area} unidades²")
        
        # Información adicional
        perimetro = 2 * (ancho + alto)
        print(f"   Perímetro: {perimetro} unidades")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def calcular_area_triangulo():
    """Función para calcular el área de un triángulo."""
    print("\n📐 CÁLCULO DE ÁREA DE TRIÁNGULO")
    print("-" * 32)
    
    try:
        base = obtener_numero("🔸 Ingresa la base: ", float, 0)
        altura = obtener_numero("🔸 Ingresa la altura: ", float, 0)
        area = util_math.area_triangulo(base, altura)
        
        print(f"\n✅ RESULTADO:")
        print(f"   Base: {base}")
        print(f"   Altura: {altura}")
        print(f"   Área: {area} unidades²")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def calcular_factorial():
    """Función para calcular el factorial de un número."""
    print("\n🔢 CÁLCULO DE FACTORIAL")
    print("-" * 23)
    
    try:
        numero = obtener_numero("🔸 Ingresa un número entero: ", int, 0)
        
        if numero > 20:
            print("⚠️ Advertencia: Números muy grandes pueden tomar tiempo...")
        
        resultado = util_math.factorial(numero)
        
        print(f"\n✅ RESULTADO:")
        print(f"   {numero}! = {resultado}")
        
        # Información adicional para números pequeños
        if numero <= 10:
            print(f"   Cálculo: ", end="")
            if numero == 0 or numero == 1:
                print("1 (por definición)")
            else:
                calculo = " × ".join(str(i) for i in range(1, numero + 1))
                print(f"{calculo} = {resultado}")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def verificar_primo():
    """Función para verificar si un número es primo."""
    print("\n🔍 VERIFICACIÓN DE NÚMERO PRIMO")
    print("-" * 33)
    
    try:
        numero = obtener_numero("🔸 Ingresa un número entero: ", int)
        
        es_primo = util_math.es_primo(numero)
        
        print(f"\n✅ RESULTADO:")
        print(f"   Número: {numero}")
        
        if es_primo:
            print(f"   🎯 {numero} ES un número primo")
            print(f"   📝 Solo es divisible por 1 y {numero}")
        else:
            print(f"   ❌ {numero} NO es un número primo")
            
            # Encontrar divisores para números no primos pequeños
            if 2 <= numero <= 100:
                divisores = []
                for i in range(2, numero):
                    if numero % i == 0:
                        divisores.append(i)
                        if len(divisores) >= 3:  # Limitar a los primeros 3
                            divisores.append("...")
                            break
                
                if divisores:
                    print(f"   📝 Algunos divisores: {divisores}")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def calcular_area_poligono():
    """Función para calcular el área de un polígono regular (ejercicio PLUS)."""
    print("\n🔶 CÁLCULO DE ÁREA DE POLÍGONO REGULAR")
    print("-" * 40)
    
    # Mostrar ejemplos de polígonos
    print("📋 Ejemplos de polígonos regulares:")
    print("   3 lados = Triángulo equilátero")
    print("   4 lados = Cuadrado")
    print("   5 lados = Pentágono")
    print("   6 lados = Hexágono")
    print("   8 lados = Octágono")
    
    try:
        num_lados = obtener_numero("\n🔸 Número de lados: ", int, 3)
        longitud_lado = obtener_numero("🔸 Longitud de cada lado: ", float, 0)
        
        area = util_math.area_poligono_regular(num_lados, longitud_lado)
        
        # Determinar el nombre del polígono
        nombres_poligonos = {
            3: "Triángulo equilátero",
            4: "Cuadrado", 
            5: "Pentágono",
            6: "Hexágono",
            7: "Heptágono",
            8: "Octágono",
            9: "Eneágono",
            10: "Decágono"
        }
        
        nombre = nombres_poligonos.get(num_lados, f"Polígono de {num_lados} lados")
        
        print(f"\n✅ RESULTADO:")
        print(f"   Polígono: {nombre}")
        print(f"   Número de lados: {num_lados}")
        print(f"   Longitud del lado: {longitud_lado}")
        print(f"   Área: {area:.4f} unidades²")
        
        # Información adicional
        perimetro = num_lados * longitud_lado
        print(f"   Perímetro: {perimetro} unidades")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def informacion_circulo():
    """Función para obtener información completa de un círculo."""
    print("\n📊 INFORMACIÓN COMPLETA DE CÍRCULO")
    print("-" * 35)
    
    try:
        radio = obtener_numero("🔸 Ingresa el radio del círculo: ", float, 0)
        info = util_math.obtener_info_circulo(radio)
        
        print(f"\n✅ INFORMACIÓN COMPLETA:")
        print(f"   Radio: {info['radio']}")
        print(f"   Diámetro: {info['diametro']}")
        print(f"   Área: {info['area']:.4f} unidades²")
        print(f"   Perímetro: {info['perimetro']:.4f} unidades")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def listar_primos():
    """Función para generar una lista de números primos."""
    print("\n📋 LISTA DE NÚMEROS PRIMOS")
    print("-" * 28)
    
    try:
        limite = obtener_numero("🔸 Hasta qué número buscar primos: ", int, 2)
        
        if limite > 1000:
            confirmar = input("⚠️ Esto puede tomar tiempo. ¿Continuar? (s/n): ")
            if confirmar.lower() not in ['s', 'si', 'sí']:
                return
        
        primos = util_math.lista_primos(limite)
        
        print(f"\n✅ NÚMEROS PRIMOS HASTA {limite}:")
        
        if len(primos) <= 50:
            # Mostrar todos si son pocos
            for i, primo in enumerate(primos, 1):
                print(f"{primo:4d}", end="  ")
                if i % 10 == 0:  # Nueva línea cada 10 números
                    print()
            print()  # Línea final
        else:
            # Mostrar solo los primeros y últimos si son muchos
            print("Primeros 20:", primos[:20])
            print("...")
            print("Últimos 20:", primos[-20:])
        
        print(f"\n📊 Total encontrados: {len(primos)} números primos")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def calcular_hipotenusa():
    """Función para calcular la hipotenusa de un triángulo rectángulo."""
    print("\n📏 CÁLCULO DE HIPOTENUSA")
    print("-" * 25)
    
    try:
        cateto1 = obtener_numero("🔸 Ingresa el primer cateto: ", float, 0)
        cateto2 = obtener_numero("🔸 Ingresa el segundo cateto: ", float, 0)
        
        hipotenusa = util_math.calcular_hipotenusa(cateto1, cateto2)
        
        print(f"\n✅ RESULTADO:")
        print(f"   Cateto 1: {cateto1}")
        print(f"   Cateto 2: {cateto2}")
        print(f"   Hipotenusa: {hipotenusa:.4f}")
        
        # Verificar si es un triángulo pitagórico conocido
        lados = sorted([cateto1, cateto2, hipotenusa])
        if all(x == int(x) for x in lados):
            print(f"   📐 Triángulo con lados enteros: {int(lados[0])}-{int(lados[1])}-{int(lados[2])}")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def ejecutar_pruebas():
    """Ejecuta todas las pruebas del módulo."""
    print("\n🧪 EJECUTANDO TODAS LAS PRUEBAS")
    print("=" * 35)
    
    pruebas = [
        ("Área círculo (r=5)", lambda: util_math.area_circulo(5)),
        ("Área rectángulo (4x6)", lambda: util_math.area_rectangulo(4, 6)),
        ("Área triángulo (10x8)", lambda: util_math.area_triangulo(10, 8)),
        ("Factorial de 5", lambda: util_math.factorial(5)),
        ("¿17 es primo?", lambda: util_math.es_primo(17)),
        ("¿20 es primo?", lambda: util_math.es_primo(20)),
        ("Área hexágono (l=5)", lambda: util_math.area_poligono_regular(6, 5)),
        ("Hipotenusa (3,4)", lambda: util_math.calcular_hipotenusa(3, 4)),
    ]
    
    print("Ejecutando pruebas...\n")
    
    for nombre, funcion in pruebas:
        try:
            resultado = funcion()
            print(f"✅ {nombre}: {resultado}")
        except Exception as e:
            print(f"❌ {nombre}: Error - {e}")
    
    print(f"\n📊 Pruebas completadas: {len(pruebas)} funciones probadas")


def main():
    """Función principal del programa."""
    print("🎓 BOOTCAMP INGENIERÍA DE DATOS - CLASE 03")
    print("🧮 Calculadora Matemática con Módulos Personalizados")
    print("=" * 55)
    
    while True:
        try:
            mostrar_menu()
            opcion = input("👉 Selecciona una opción (0-11): ").strip()
            
            if opcion == "0":
                print("\n👋 ¡Gracias por usar la calculadora matemática!")
                print("🎓 Ejercicio de Clase 03 completado exitosamente")
                break
            elif opcion == "1":
                calcular_area_circulo()
            elif opcion == "2":
                calcular_area_rectangulo()
            elif opcion == "3":
                calcular_area_triangulo()
            elif opcion == "4":
                calcular_factorial()
            elif opcion == "5":
                verificar_primo()
            elif opcion == "6":
                calcular_area_poligono()
            elif opcion == "7":
                informacion_circulo()
            elif opcion == "8":
                listar_primos()
            elif opcion == "9":
                calcular_hipotenusa()
            elif opcion == "10":
                util_math.mostrar_constantes()
            elif opcion == "11":
                ejecutar_pruebas()
            else:
                print("❌ Opción no válida. Por favor, selecciona un número del 0 al 11.")
            
            # Pausa para que el usuario pueda leer el resultado
            input("\n⏸️ Presiona Enter para continuar...")
            
        except KeyboardInterrupt:
            print("\n\n👋 Programa interrumpido por el usuario. ¡Hasta luego!")
            break
        except Exception as e:
            print(f"\n❌ Error inesperado: {e}")
            input("⏸️ Presiona Enter para continuar...")


if __name__ == "__main__":
    main()