import datetime

def obtener_nombre():
    """Función para obtener y validar el nombre del usuario."""
    while True:
        nombre = input("¿Cuál es tu nombre? ").strip()
        if nombre and not nombre.isdigit():
            return nombre.title()
        print("❌ Por favor, ingresa un nombre válido.")

def obtener_edad():
    """Función para obtener y validar la edad del usuario."""
    while True:
        try:
            edad = int(input("¿Qué edad tienes? "))
            if 0 <= edad <= 120:
                return edad
            print("❌ Por favor, ingresa una edad válida (0-120).")
        except ValueError:
            print("❌ Por favor, ingresa un número válido.")

def clasificar_por_edad(edad):
    """Clasifica al usuario según su edad."""
    if edad < 13:
        return "niño/a"
    elif edad < 18:
        return "adolescente"
    elif edad < 65:
        return "adulto/a"
    else:
        return "adulto/a mayor"

def main():
    """Función principal del programa."""
    print("🐍 ¡Bienvenido al mundo de Python! 🐍")
    print("=" * 40)
    
    # Obtener datos del usuario
    nombre = obtener_nombre()
    edad = obtener_edad()
    
    # Clasificar por edad
    categoria = clasificar_por_edad(edad)
    
    # Mostrar resultado personalizado
    print(f"\n🎉 ¡Hola, {nombre}!")
    print(f"📅 Tienes {edad} años")
    print(f"👤 Eres {categoria}")
    
    # Verificar mayoría de edad
    if edad >= 18:
        print("✅ Eres mayor de edad")
        print("🎓 ¡Perfecto para aprender ingeniería de datos!")
    else:
        print("📚 Eres menor de edad")
        print("🌟 ¡Nunca es demasiado temprano para empezar a programar!")
    
    # Calcular año de nacimiento aproximado
    año_actual = datetime.datetime.now().year
    año_nacimiento = año_actual - edad
    print(f"🗓️ Naciste aproximadamente en {año_nacimiento}")
    
    print("\n🚀 ¡Que disfrutes tu journey en el bootcamp!")

if __name__ == "__main__":
    main()