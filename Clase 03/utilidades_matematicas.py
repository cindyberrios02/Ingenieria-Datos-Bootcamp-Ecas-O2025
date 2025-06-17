import math


def area_circulo(radio):
    """
    Calcula el área de un círculo dado su radio.
    
    Fórmula: π * r²
    
    Args:
        radio (float): Radio del círculo (debe ser positivo)
        
    Returns:
        float: Área del círculo
        
    Raises:
        ValueError: Si el radio es negativo
        TypeError: Si el radio no es un número
        
    Example:
        >>> area_circulo(5)
        78.53981633974483
    """
    try:
        radio = float(radio)
        if radio < 0:
            raise ValueError("El radio no puede ser negativo")
        return math.pi * radio ** 2
    except (ValueError, TypeError) as e:
        if "could not convert" in str(e):
            raise TypeError("El radio debe ser un número")
        raise


def area_rectangulo(ancho, alto):
    """
    Calcula el área de un rectángulo dado su ancho y alto.
    
    Fórmula: ancho * alto
    
    Args:
        ancho (float): Ancho del rectángulo (debe ser positivo)
        alto (float): Alto del rectángulo (debe ser positivo)
        
    Returns:
        float: Área del rectángulo
        
    Raises:
        ValueError: Si el ancho o alto son negativos
        TypeError: Si el ancho o alto no son números
        
    Example:
        >>> area_rectangulo(4, 6)
        24
    """
    try:
        ancho = float(ancho)
        alto = float(alto)
        
        if ancho < 0 or alto < 0:
            raise ValueError("El ancho y alto deben ser positivos")
            
        return ancho * alto
        
    except (ValueError, TypeError) as e:
        if "could not convert" in str(e):
            raise TypeError("El ancho y alto deben ser números")
        raise


def area_triangulo(base, altura):
    """
    Calcula el área de un triángulo dado su base y altura.
    
    Fórmula: (base * altura) / 2
    
    Args:
        base (float): Base del triángulo (debe ser positiva)
        altura (float): Altura del triángulo (debe ser positiva)
        
    Returns:
        float: Área del triángulo
        
    Raises:
        ValueError: Si la base o altura son negativos
        TypeError: Si la base o altura no son números
        
    Example:
        >>> area_triangulo(10, 8)
        40.0
    """
    try:
        base = float(base)
        altura = float(altura)
        
        if base < 0 or altura < 0:
            raise ValueError("La base y altura deben ser positivos")
            
        return (base * altura) / 2
        
    except (ValueError, TypeError) as e:
        if "could not convert" in str(e):
            raise TypeError("La base y altura deben ser números")
        raise


def factorial(numero):
    """
    Calcula el factorial de un número entero no negativo.
    
    Fórmula: n! = n * (n-1) * (n-2) * ... * 1
    
    Args:
        numero (int): Número entero no negativo
        
    Returns:
        int: Factorial del número
        
    Raises:
        ValueError: Si el número es negativo
        TypeError: Si el número no es entero
        
    Example:
        >>> factorial(5)
        120
        >>> factorial(0)
        1
    """
    try:
        numero = int(numero)
        if numero < 0:
            raise ValueError("El factorial no está definido para números negativos")
            
        if numero == 0 or numero == 1:
            return 1
        
        resultado = 1
        for i in range(2, numero + 1):
            resultado *= i
            
        return resultado
        
    except (ValueError, TypeError) as e:
        if "invalid literal" in str(e):
            raise TypeError("El número debe ser un entero")
        raise


def es_primo(numero):
    """
    Determina si un número es primo.
    
    Un número primo es un entero mayor que 1 que no tiene divisores
    positivos distintos a 1 y él mismo.
    
    Args:
        numero (int): Número entero a verificar
        
    Returns:
        bool: True si el número es primo, False en caso contrario
        
    Raises:
        TypeError: Si el número no es entero
        
    Example:
        >>> es_primo(17)
        True
        >>> es_primo(15)
        False
    """
    try:
        numero = int(numero)
        
        # Los números menores a 2 no son primos
        if numero < 2:
            return False
            
        # 2 es primo
        if numero == 2:
            return True
            
        # Los números pares mayores a 2 no son primos
        if numero % 2 == 0:
            return False
            
        # Verificar divisibilidad desde 3 hasta la raíz cuadrada del número
        # Solo verificamos números impares
        for i in range(3, int(math.sqrt(numero)) + 1, 2):
            if numero % i == 0:
                return False
                
        return True
        
    except (ValueError, TypeError):
        raise TypeError("El número debe ser un entero")


def area_poligono_regular(num_lados, longitud_lado):
    """
    Calcula el área de un polígono regular dado su número de lados y longitud de cada lado.
    
    Fórmula: (n * s²) / (4 * tan(π/n))
    donde n = número de lados, s = longitud del lado
    
    Args:
        num_lados (int): Número de lados del polígono (debe ser >= 3)
        longitud_lado (float): Longitud de cada lado (debe ser positiva)
        
    Returns:
        float: Área del polígono regular
        
    Raises:
        ValueError: Si el número de lados es menor a 3 o la longitud es negativa
        TypeError: Si los parámetros no son números
        
    Example:
        >>> area_poligono_regular(6, 5)  # Hexágono regular
        64.95190528383289
    """
    try:
        num_lados = int(num_lados)
        longitud_lado = float(longitud_lado)
        
        if num_lados < 3:
            raise ValueError("Un polígono debe tener al menos 3 lados")
            
        if longitud_lado < 0:
            raise ValueError("La longitud del lado debe ser positiva")
            
        # Fórmula para el área de un polígono regular
        area = (num_lados * longitud_lado ** 2) / (4 * math.tan(math.pi / num_lados))
        
        return area
        
    except (ValueError, TypeError) as e:
        if "invalid literal" in str(e) or "could not convert" in str(e):
            raise TypeError("Los parámetros deben ser números válidos")
        raise


def obtener_info_circulo(radio):
    """
    Función adicional: Obtiene información completa de un círculo.
    
    Args:
        radio (float): Radio del círculo
        
    Returns:
        dict: Diccionario con área, perímetro y diámetro
    """
    try:
        radio = float(radio)
        if radio < 0:
            raise ValueError("El radio no puede ser negativo")
            
        return {
            'radio': radio,
            'area': area_circulo(radio),
            'perimetro': 2 * math.pi * radio,
            'diametro': 2 * radio
        }
    except (ValueError, TypeError) as e:
        if "could not convert" in str(e):
            raise TypeError("El radio debe ser un número")
        raise


def lista_primos(limite):
    """
    Función adicional: Genera una lista de números primos hasta un límite.
    
    Args:
        limite (int): Límite superior para buscar primos
        
    Returns:
        list: Lista de números primos hasta el límite
    """
    try:
        limite = int(limite)
        if limite < 2:
            return []
            
        primos = []
        for num in range(2, limite + 1):
            if es_primo(num):
                primos.append(num)
                
        return primos
        
    except (ValueError, TypeError):
        raise TypeError("El límite debe ser un entero")


def calcular_hipotenusa(cateto1, cateto2):
    """
    Función adicional: Calcula la hipotenusa de un triángulo rectángulo.
    
    Fórmula: √(cateto1² + cateto2²)
    
    Args:
        cateto1 (float): Primer cateto
        cateto2 (float): Segundo cateto
        
    Returns:
        float: Longitud de la hipotenusa
    """
    try:
        cateto1 = float(cateto1)
        cateto2 = float(cateto2)
        
        if cateto1 < 0 or cateto2 < 0:
            raise ValueError("Los catetos deben ser positivos")
            
        return math.sqrt(cateto1**2 + cateto2**2)
        
    except (ValueError, TypeError) as e:
        if "could not convert" in str(e):
            raise TypeError("Los catetos deben ser números")
        raise


# Constantes matemáticas útiles
PI = math.pi
E = math.e
PHI = (1 + math.sqrt(5)) / 2  # Proporción áurea


def mostrar_constantes():
    """
    Muestra las constantes matemáticas disponibles en el módulo.
    """
    print("🔢 CONSTANTES MATEMÁTICAS DISPONIBLES:")
    print(f"  π (PI): {PI:.10f}")
    print(f"  e (E): {E:.10f}")
    print(f"  φ (PHI - Proporción áurea): {PHI:.10f}")


if __name__ == "__main__":
    # Pruebas del módulo cuando se ejecuta directamente
    print("🧮 MÓDULO DE UTILIDADES MATEMÁTICAS")
    print("=" * 40)
    print("Ejecutando pruebas del módulo...\n")
    
    try:
        # Pruebas de áreas
        print("📐 PRUEBAS DE ÁREAS:")
        print(f"Área círculo (r=5): {area_circulo(5):.2f}")
        print(f"Área rectángulo (4x6): {area_rectangulo(4, 6)}")
        print(f"Área triángulo (b=10, h=8): {area_triangulo(10, 8)}")
        print(f"Área hexágono regular (l=5): {area_poligono_regular(6, 5):.2f}")
        
        # Pruebas de números
        print(f"\n🔢 PRUEBAS NUMÉRICAS:")
        print(f"Factorial de 5: {factorial(5)}")
        print(f"¿Es 17 primo?: {es_primo(17)}")
        print(f"¿Es 15 primo?: {es_primo(15)}")
        
        # Pruebas adicionales
        print(f"\n➕ FUNCIONES ADICIONALES:")
        print(f"Hipotenusa (3,4): {calcular_hipotenusa(3, 4):.2f}")
        print(f"Primos hasta 20: {lista_primos(20)}")
        
        mostrar_constantes()
        
        print(f"\n✅ ¡Todas las pruebas completadas exitosamente!")
        
    except Exception as e:
        print(f"❌ Error en las pruebas: {e}")