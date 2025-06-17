# 🧮 Ejercicio Clase 03: Módulo de Utilidades Matemáticas

## 📝 Descripción

Este proyecto implementa un módulo completo de utilidades matemáticas como parte del **Bootcamp de Ingeniería de Datos - Clase 03**. El ejercicio se enfoca en la creación de funciones, módulos personalizados y manejo de errores.

## 🎯 Objetivos Cumplidos

### ✅ Requisitos Básicos
- [x] Calcular área de círculo dado su radio
- [x] Calcular área de rectángulo dado ancho y alto  
- [x] Calcular área de triángulo dado base y altura
- [x] Calcular factorial de un número
- [x] Determinar si un número es primo

### ⭐ Ejercicio PLUS
- [x] Calcular área de polígono regular dado número de lados y longitud

### 🚀 Características Adicionales
- [x] Validación completa de entrada de datos
- [x] Manejo robusto de errores y excepciones
- [x] Documentación con docstrings
- [x] Programa interactivo con menú
- [x] Funciones matemáticas adicionales
- [x] Sistema de pruebas automáticas

## 📁 Estructura del Proyecto

```
ejercicio-03-funciones-modulos/
├── utilidades_matematicas.py    # 📦 Módulo principal con todas las funciones
├── programa_calculadora.py      # 🖥️ Programa interactivo principal
└── README.md                    # 📖 Esta documentación
```

## 🛠️ Instalación y Uso

### Prerrequisitos
- Python 3.6 o superior
- Módulo `math` (incluido en Python estándar)

### Ejecución

1. **Clonar o descargar los archivos**
2. **Ejecutar el programa principal:**
   ```bash
   python programa_calculadora.py
   ```
3. **O usar el módulo directamente:**
   ```bash
   python utilidades_matematicas.py
   ```

### Uso como Módulo

```python
import utilidades_matematicas as util_math

# Calcular área de círculo
area = util_math.area_circulo(5)
print(f"Área: {area}")

# Verificar número primo
es_primo = util_math.es_primo(17)
print(f"17 es primo: {es_primo}")

# Calcular factorial
factorial = util_math.factorial(5)
print(f"5! = {factorial}")
```

## 🔧 Funciones Disponibles

### 📐 Funciones de Área

| Función | Descripción | Parámetros | Retorno |
|---------|-------------|------------|---------|
| `area_circulo(radio)` | Calcula área de círculo | `radio: float` | `float` |
| `area_rectangulo(ancho, alto)` | Calcula área de rectángulo | `ancho: float, alto: float` | `float` |
| `area_triangulo(base, altura)` | Calcula área de triángulo | `base: float, altura: float` | `float` |
| `area_poligono_regular(lados, longitud)` | Área de polígono regular | `lados: int, longitud: float` | `float` |

### 🔢 Funciones Numéricas

| Función | Descripción | Parámetros | Retorno |
|---------|-------------|------------|---------|
| `factorial(numero)` | Calcula factorial | `numero: int` | `int` |
| `es_primo(numero)` | Verifica si es primo | `numero: int` | `bool` |
| `lista_primos(limite)` | Lista primos hasta límite | `limite: int` | `list[int]` |

### 📏 Funciones Adicionales

| Función | Descripción | Parámetros | Retorno |
|---------|-------------|------------|---------|
| `calcular_hipotenusa(c1, c2)` | Calcula hipotenusa | `c1: float, c2: float` | `float` |
| `obtener_info_circulo(radio)` | Info completa círculo | `radio: float` | `dict` |

## 💡 Ejemplos de Uso

### Ejemplo 1: Cálculos Básicos
```python
import utilidades_matematicas as util

# Geometría
area_circ = util.area_circulo(5)          # 78.54
area_rect = util.area_rectangulo(4, 6)    # 24
area_tri = util.area_triangulo(10, 8)     # 40.0

# Números
fact_5 = util.factorial(5)                # 120
primo_17 = util.es_primo(17)              # True
primo_20 = util.es_primo(20)              # False
```

### Ejemplo 2: Polígono Regular (PLUS)
```python
# Hexágono regular con lado de 5 unidades
area_hex = util.area_poligono_regular(6, 5)
print(f"Área del hexágono: {area_hex:.2f}")  # 64.95
```

### Ejemplo 3: Información Completa
```python
info = util.obtener_info_circulo(3)
print(f"Radio: {info['radio']}")
print(f"Área: {info['area']:.2f}")
print(f"Perímetro: {info['perimetro']:.2f}")
print(f"Diámetro: {info['diametro']}")
```

## 🧪 Sistema de Pruebas

El módulo incluye un sistema de pruebas automáticas:

```python
# Ejecutar todas las pruebas
python utilidades_matematicas.py
```

O desde el programa principal, seleccionar opción 11.

## ⚠️ Manejo de Errores

Todas las funciones incluyen validación robusta:

```python
try:
    area = util.area_circulo(-5)  # ValueError: El radio no puede ser negativo
except ValueError as e:
    print(f"Error: {e}")

try:
    factorial = util.factorial("abc")  # TypeError: El número debe ser un entero
except TypeError as e:
    print(f"Error: {e}")
```

## 🔢 Constantes Matemáticas

El módulo incluye constantes útiles:

- `PI` = 3.141592653589793
- `E` = 2.718281828459045  
- `PHI` = 1.618033988749895 (Proporción áurea)

## 📊 Funcionalidades del Programa Interactivo

El programa `programa_calculadora.py` ofrece:

1. **Menú interactivo** con 11 opciones
2. **Validación de entrada** robusta
3. **Cálculos en tiempo real** 
4. **Información adicional** para cada resultado
5. **Sistema de pruebas** integrado
6. **Interfaz amigable** con emojis y formateo

## 🎓 Conceptos Aplicados

### Programación
- ✅ Funciones con parámetros y retorno
- ✅ Módulos personalizados e imports
- ✅ Manejo de excepciones (try/except)
- ✅ Validación de tipos de datos
- ✅ Documentación con docstrings

### Matemáticas
- ✅ Geometría: áreas de figuras
- ✅ Trigonometría: polígonos regulares
- ✅ Teoría de números: primos y factoriales
- ✅ Teorema de Pitágoras

### Ingeniería de Software
- ✅ Separación de responsabilidades
- ✅ Reutilización de código
- ✅ Testing automatizado
- ✅ Documentación técnica

## 🏆 Resultados de Aprendizaje

Al completar este ejercicio, has demostrado dominio en:

- **Creación de módulos** personalizados en Python
- **Diseño de funciones** con validación robusta
- **Manejo de errores** y excepciones
- **Documentación** profesional de código
- **Testing** y verificación de funcionalidad
- **Aplicación práctica** de conceptos matemáticos

## 📈 Métricas del Proyecto

- **Líneas de código:** ~400+ líneas
- **Funciones implementadas:** 10+ funciones
- **Casos de prueba:** 8 pruebas automáticas
- **Validaciones:** 100% de funciones validadas
- **Documentación:** Docstrings completos

## 🔄 Posibles Extensiones

Ideas para expandir el proyecto:

1. **Más figuras geométricas:** elipse, trapecio, rombo
2. **Conversiones de unidades:** metros, pies, pulgadas
3. **Estadísticas básicas:** media, mediana, desviación
4. **Trigonometría:** seno, coseno, tangente
5. **Exportar resultados:** guardar en CSV/JSON

## 👨‍💻 Autor

**Bootcamp de Ingeniería de Datos**
- Clase 03: Funciones y Módulos
- Ejercicio: Sistema de Utilidades Matemáticas

