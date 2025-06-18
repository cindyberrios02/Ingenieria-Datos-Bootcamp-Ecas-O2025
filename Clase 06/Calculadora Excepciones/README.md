# 🧮 Clase 06: Calculadora con Manejo de Excepciones

## 📝 Descripción

Sistema completo de calculadora desarrollado como parte del **Bootcamp de Ingeniería de Datos - Clase 06**. Este proyecto implementa el **manejo robusto de excepciones** en Python usando `try`, `except`, `else`, y `finally`, junto con funcionalidades avanzadas de logging, historial y análisis estadístico.

## 🎯 Objetivos Cumplidos

### ✅ Requisitos Básicos
- [x] **Solicitar dos números y operación** al usuario
- [x] **Realizar operación matemática** (+, -, *, /)
- [x] **Mostrar resultado** de forma clara
- [x] **Manejo de excepciones** para:
  - [x] División por cero (`ZeroDivisionError`)
  - [x] Entrada no válida (`ValueError`)
  - [x] Operador no válido (`ValueError`)

### ⭐ Ejercicio PLUS
- [x] **Opción de repetir operaciones** hasta que el usuario decida salir

### 🚀 Características Adicionales
- [x] **Operaciones avanzadas** (potencia, módulo, raíz, logaritmo)
- [x] **Sistema de historial** con timestamps
- [x] **Logging completo** de operaciones y errores
- [x] **Validación robusta** de entrada de datos
- [x] **Interfaz de usuario** intuitiva con menús
- [x] **Estadísticas de uso** y análisis de operaciones
- [x] **Exportación de historial** a archivos
- [x] **Suite de testing** con 30+ pruebas automatizadas

## 📁 Estructura del Proyecto

```
Clase06-ManejoExcepciones-Calculadora/
├── calculadora_excepciones.py    # 🏗️ Sistema principal completo
├── test_calculadora_excepciones.py # 🧪 Suite completa de tests
├── calculadora.log               # 📋 Log automático de operaciones
├── historial_calculadora.txt     # 💾 Historial exportado
└── README.md                     # 📖 Esta documentación
```

## 🛠️ Instalación y Uso

### Prerrequisitos
- Python 3.6 o superior
- Módulos estándar: `math`, `logging`, `datetime`, `typing`, `unittest`

### Ejecución Rápida

#### 1. **Sistema Completo (Recomendado)**
```bash
python calculadora_excepciones.py
```

#### 2. **Calculadora Básica Directa**
```python
from calculadora_excepciones import CalculadoraAvanzada

calc = CalculadoraAvanzada()
calc.calculadora_basica()
```

#### 3. **Calculadora con Repetición (PLUS)**
```python
calc = CalculadoraAvanzada()
calc.calculadora_con_repeticion()
```

#### 4. **Ejecutar Tests**
```bash
python test_calculadora_excepciones.py
```

## 🔧 Funcionalidades Principales

### 📊 Operadores Soportados

| Operador | Descripción | Ejemplo | Validaciones |
|----------|-------------|---------|--------------|
| `+` | Suma | `5 + 3 = 8` | - |
| `-` | Resta | `5 - 3 = 2` | - |
| `*` | Multiplicación | `5 * 3 = 15` | - |
| `/` | División | `6 / 3 = 2` | ❌ División por cero |
| `^` | Potencia | `2 ^ 3 = 8` | ❌ Neg^decimal, 0^negativo |
| `%` | Módulo | `7 % 3 = 1` | ❌ Módulo por cero |
| `//` | División entera | `7 // 3 = 2` | ❌ División por cero |
| `sqrt` | Raíz cuadrada | `sqrt(9) = 3` | ❌ Raíz de negativo |
| `log` | Logaritmo natural | `ln(e) = 1` | ❌ Log de ≤0 |

### 🛡️ Excepciones Manejadas

#### **ZeroDivisionError**
```python
# Casos que generan esta excepción:
10 / 0          # División por cero
10 % 0          # Módulo por cero  
10 // 0         # División entera por cero
0 ^ -1          # Cero elevado a potencia negativa
```

#### **ValueError**
```python
# Casos que generan esta excepción:
sqrt(-4)        # Raíz cuadrada de negativo
log(-1)         # Logaritmo de negativo o cero
(-2) ^ 0.5      # Potencia decimal de negativo
"abc"           # Entrada no numérica
"&"             # Operador inválido
```

#### **OverflowError**
```python
# Casos que generan esta excepción:
resultado = float('inf')    # Resultado infinito
resultado muy grande        # Desbordamiento numérico
```

## 💡 Ejemplos de Uso

### Ejemplo 1: Uso Básico
```python
from calculadora_excepciones import CalculadoraAvanzada

calc = CalculadoraAvanzada()

# Operación simple
resultado = calc.realizar_operacion(10, 5, "+")
print(resultado)  # 15.0

# Operación con manejo de error
try:
    resultado = calc.realizar_operacion(10, 0, "/")
except ZeroDivisionError as e:
    print(f"Error: {e}")  # "No se puede dividir por cero"
```

### Ejemplo 2: Operaciones Avanzadas
```python
# Raíz cuadrada
resultado = calc.realizar_operacion(16, 0, "sqrt")
print(resultado)  # 4.0

# Logaritmo natural
resultado = calc.realizar_operacion(2.71828, 0, "log")
print(resultado)  # ≈ 1.0

# Potencia
resultado = calc.realizar_operacion(2, 10, "^")
print(resultado)  # 1024.0
```

### Ejemplo 3: Manejo de Errores Completo
```python
try:
    # Intentar operación problemática
    resultado = calc.realizar_operacion(-4, 0, "sqrt")
except ValueError as e:
    print(f"Error de valor: {e}")
except ZeroDivisionError as e:
    print(f"Error de división: {e}")
except Exception as e:
    print(f"Error inesperado: {e}")
finally:
    print("Operación finalizada")
```

### Ejemplo 4: Uso del Historial
```python
# Realizar operaciones
calc.realizar_operacion(10, 5, "+")
calc.realizar_operacion(20, 4, "/")

# Agregar al historial
calc.agregar_al_historial("10 + 5", 15)
calc.agregar_al_historial("20 / 4", 5)

# Mostrar historial
calc.mostrar_historial()
```

## 🧪 Sistema de Testing

### Suite de Pruebas Completa

El proyecto incluye **30+ tests automatizados** organizados en 3 categorías:

#### **TestCalculadoraExcepciones** (Tests Principales)
- ✅ Operaciones básicas válidas (+, -, *, /, ^, %, //)
- ✅ Operaciones unarias (sqrt, log)
- ✅ Manejo de división por cero
- ✅ Manejo de valores inválidos
- ✅ Casos especiales de potencias
- ✅ Sistema de historial
- ✅ Formateo de resultados
- ✅ Validación de entrada

#### **TestCasosEspeciales** (Edge Cases)
- ✅ Operaciones con cero
- ✅ Números muy grandes y pequeños
- ✅ Números negativos
- ✅ Precisión decimal
- ✅ Casos límite de operadores

#### **TestIntegracion** (Flujos Completos)
- ✅ Flujo completo de operación válida
- ✅ Flujo completo con errores
- ✅ Integración de entrada/salida
- ✅ Manejo de cancelaciones

### Ejecutar Tests
```bash
# Ejecutar todos los tests
python test_calculadora_excepciones.py

# Resultado esperado: 30+ tests ✅ PASSED
```

## 🎮 Menú Interactivo

El sistema incluye un menú completo con **8 opciones**:

```
🧮 SISTEMA DE CALCULADORA AVANZADA
══════════════════════════════════════════════════════════
1. 🔢 Calculadora básica (requisitos mínimos)
2. 🔄 Calculadora con repetición (PLUS)
3. 🧠 Evaluador de expresiones (avanzado)
4. 📋 Ver historial de operaciones
5. 📊 Mostrar estadísticas de uso
6. 🗑️ Limpiar historial
7. 🎓 Demo de manejo de excepciones
8. 💾 Exportar historial a archivo
0. 🚪 Salir
```

### Funcionalidades del Menú

#### **Opción 1: Calculadora Básica**
- Cumple exactamente los requisitos de la consigna
- Solicita dos números y operador
- Maneja todas las excepciones requeridas
- Muestra resultado formateado

#### **Opción 2: Calculadora con Repetición (PLUS)**
- Permite múltiples operaciones consecutivas
- Menú interno con opciones adicionales
- Gestión de historial integrada
- Opción de salir cuando el usuario decida

#### **Opción 3: Evaluador de Expresiones**
- Evalúa expresiones matemáticas completas
- Ejemplo: `(5 + 3) * 2`, `10 / (2 + 3)`
- Validación de caracteres permitidos
- Manejo de errores de sintaxis

#### **Opción 4-6: Gestión de Historial**
- Ver todas las operaciones realizadas
- Estadísticas detalladas de uso
- Limpieza de historial

#### **Opción 7: Demo Educativa**
- Demostración de diferentes tipos de errores
- Ejemplos de manejo de excepciones
- Casos de uso educativos

#### **Opción 8: Persistencia**
- Exporta historial a archivo de texto
- Formato legible y organizado
- Timestamps incluidos

## 📊 Sistema de Logging

### Configuración Automática
```python
# Logging configurado automáticamente
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('calculadora.log'),
        logging.StreamHandler()
    ]
)
```

### Tipos de Logs Registrados
- **INFO:** Operaciones exitosas, entrada de datos válida
- **ERROR:** Errores de operación (división por cero, valores inválidos)
- **CRITICAL:** Errores críticos del sistema

### Ejemplo de Archivo de Log
```
2024-06-17 15:30:15,123 - INFO - Número válido ingresado: 10.0
2024-06-17 15:30:18,456 - INFO - Operador válido seleccionado: +
2024-06-17 15:30:20,789 - INFO - Operación exitosa: 10.0 + 5.0 = 15.0
2024-06-17 15:30:25,012 - ERROR - Error en operación: 10.0 / 0.0 - No se puede dividir por cero
```

## 📈 Sistema de Historial y Estadísticas

### Estructura del Historial
```python
{
    'timestamp': datetime.now(),
    'operacion': '10.0 + 5.0',
    'resultado': 15.0
}
```

### Estadísticas Generadas
- **Total de operaciones** realizadas
- **Promedio de resultados** obtenidos
- **Resultado máximo y mínimo**
- **Operadores más utilizados**
- **Distribución temporal** de uso

### Límites y Gestión
- **Máximo 50 operaciones** en memoria
- **Rotación automática** del historial
- **Exportación** a archivos externos
- **Limpieza manual** disponible

## 🔒 Validaciones Implementadas

### **Entrada de Números**
```python
# ✅ Válidos
"42", "3.14", "-5"