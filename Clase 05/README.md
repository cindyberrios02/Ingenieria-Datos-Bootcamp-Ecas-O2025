# 👥 Clase 05: Sistema de Gestión de Personas (POO)

## 📝 Descripción

Sistema completo de gestión de personas desarrollado como parte del **Bootcamp de Ingeniería de Datos - Clase 05**. Este proyecto implementa los conceptos fundamentales de **Programación Orientada a Objetos (POO)** en Python, incluyendo validaciones robustas, expresiones regulares y funcionalidades avanzadas.

## 🎯 Objetivos Cumplidos

### ✅ Requisitos Básicos
- [x] **Clase Persona** con atributos `nombre`, `edad`, `correo_electronico`
- [x] **Método mostrar_datos()** - Mostrar información en formato amigable
- [x] **Validación de correo** con expresiones regulares
- [x] **Método actualizar_datos()** - Actualizar información de la persona
- [x] **Método es_mayor_de_edad()** - Verificar mayoría de edad

### ⭐ Ejercicio PLUS
- [x] **Función comparar_edad_con()** - Comparar edad entre dos personas
- [x] **Método de clase comparar_dos_personas()** - Versión alternativa

### 🚀 Características Adicionales
- [x] **Validaciones robustas** con manejo completo de errores
- [x] **Métodos especiales** (`__str__`, `__repr__`, `__eq__`, `__lt__`)
- [x] **Sistema de estadísticas** de clase con contador automático
- [x] **Serialización JSON** para persistencia de datos
- [x] **Suite de testing** con 25+ pruebas automatizadas
- [x] **Interfaz interactiva** con menú completo
- [x] **Funcionalidades adicionales** (generaciones, categorías de edad, etc.)

## 📁 Estructura del Proyecto

```
Clase05-POO-SistemaPersonas/
├── clase_persona.py           # 🏗️ Clase principal con toda la funcionalidad
├── test_clase_persona.py      # 🧪 Suite completa de tests unitarios
└── README.md                  # 📖 Esta documentación
```

## 🛠️ Instalación y Uso

### Prerrequisitos
- Python 3.6 o superior
- Módulos estándar: `re`, `datetime`, `json`, `unittest`

### Ejecución Rápida

#### 1. **Sistema Completo (Recomendado)**
```bash
python clase_persona.py
```

#### 2. **Demo Automática**
```python
from clase_persona import demo_clase_persona
demo_clase_persona()
```

#### 3. **Crear Persona Simple**
```python
from clase_persona import Persona

# Crear persona
persona = Persona("Ana García", 25, "ana@email.com")
persona.mostrar_datos()
```

#### 4. **Ejecutar Tests**
```bash
python test_clase_persona.py
```

## 🔧 Funcionalidades de la Clase Persona

### 📦 Atributos

| Atributo | Tipo | Descripción | Validación |
|----------|------|-------------|------------|
| `nombre` | `str` | Nombre completo | Solo letras y espacios, 2-100 caracteres |
| `edad` | `int` | Edad en años | Entero entre 0-150 |
| `correo_electronico` | `str` | Email válido | Regex RFC + validaciones adicionales |
| `id_persona` | `int` | ID único autoincremental | Asignado automáticamente |
| `fecha_creacion` | `datetime` | Timestamp de creación | Automático |

### 🔧 Métodos Principales

#### **Métodos Básicos (Requeridos)**

| Método | Descripción | Parámetros | Retorno |
|---------|-------------|------------|---------|
| `__init__()` | Constructor con validaciones | `nombre, edad, correo_electronico` | `None` |
| `mostrar_datos()` | Muestra información formateada | - | `None` |
| `validar_correo()` | Valida email con regex | - | `bool` |
| `actualizar_datos()` | Actualiza datos selectivamente | `nombre=None, edad=None, correo_electronico=None` | `dict` |
| `es_mayor_de_edad()` | Verifica mayoría de edad | - | `bool` |

#### **Métodos del Ejercicio PLUS**

| Método | Descripción | Parámetros | Retorno |
|---------|-------------|------------|---------|
| `comparar_edad_con()` | Compara edad con otra persona | `otra_persona: Persona` | `str` |
| `comparar_dos_personas()` | Método de clase para comparar | `persona1, persona2` | `str` |

#### **Métodos Adicionales**

| Método | Descripción | Retorno |
|---------|-------------|---------|
| `obtener_categoria_edad()` | Categoría por edad | `str` |
| `calcular_año_nacimiento()` | Año aproximado de nacimiento | `int` |
| `obtener_generacion()` | Generación (Z, Millennial, etc.) | `str` |
| `dias_hasta_cumpleanos()` | Días hasta próximo cumpleaños | `int` |
| `to_dict()` | Convierte a diccionario | `dict` |
| `from_dict()` | Crea desde diccionario | `Persona` |

### 🏷️ Métodos de Clase

| Método | Descripción | Retorno |
|---------|-------------|---------|
| `obtener_estadisticas_generales()` | Estadísticas de todas las personas | `dict` |
| `comparar_dos_personas()` | Compara dos instancias | `str` |

## 💡 Ejemplos de Uso

### Ejemplo 1: Uso Básico
```python
from clase_persona import Persona

# Crear persona
persona = Persona("María González", 28, "maria@email.com")

# Mostrar datos
persona.mostrar_datos()

# Validar correo
if persona.validar_correo():
    print("✅ Correo válido")

# Verificar mayoría de edad
if persona.es_mayor_de_edad():
    print("✅ Es mayor de edad")
```

### Ejemplo 2: Actualización de Datos
```python
# Actualizar información
cambios = persona.actualizar_datos(
    nombre="María González López",
    edad=29,
    correo_electronico="maria.nueva@email.com"
)

print(f"Cambios realizados: {cambios}")
```

### Ejemplo 3: Comparación de Edades (PLUS)
```python
persona1 = Persona("Ana García", 25, "ana@email.com")
persona2 = Persona("Carlos Pérez", 30, "carlos@email.com")

# Método de instancia
resultado = persona1.comparar_edad_con(persona2)
print(resultado)  # "Carlos Pérez es mayor que Ana García por 5 año(s)"

# Método de clase
resultado = Persona.comparar_dos_personas(persona1, persona2)
print(resultado)
```

### Ejemplo 4: Funcionalidades Avanzadas
```python
# Información adicional
print(f"Categoría: {persona.obtener_categoria_edad()}")
print(f"Generación: {persona.obtener_generacion()}")
print(f"Año nacimiento: {persona.calcular_año_nacimiento()}")

# Serialización
datos = persona.to_dict()
print(f"Datos JSON: {datos}")

# Estadísticas generales
stats = Persona.obtener_estadisticas_generales()
print(f"Total personas: {stats['total_personas']}")
```

## 🧪 Sistema de Testing

### Suite de Pruebas Completa

El proyecto incluye **25+ tests unitarios** que cubren:

#### **Tests de Validación**
- ✅ Creación de personas válidas
- ✅ Validación de nombres (caracteres, longitud)
- ✅ Validación de edades (rangos, tipos)
- ✅ Validación de correos (regex, casos edge)

#### **Tests de Funcionalidad**
- ✅ Mostrar datos correctamente
- ✅ Actualización de información
- ✅ Verificación de mayoría de edad
- ✅ Comparación de edades (PLUS)

#### **Tests de Métodos Adicionales**
- ✅ Categorización por edad
- ✅ Cálculo de año de nacimiento
- ✅ Determinación de generación
- ✅ Serialización JSON

#### **Tests de Casos Especiales**
- ✅ Nombres con caracteres especiales
- ✅ Edades en los límites (0, 150)
- ✅ Correos casos límite
- ✅ Métodos especiales (`__eq__`, `__lt__`)

### Ejecutar Tests
```bash
# Ejecutar todos los tests
python test_clase_persona.py

# Resultado esperado: 25+ tests ✅ PASSED
```

## 🔒 Validaciones Implementadas

### **Validación de Nombres**
```python
# ✅ Válidos
"Ana García"
"José María Pérez"
"Sofía"

# ❌ Inválidos
""              # Vacío
"A"             # Muy corto
"Ana123"        # Con números
"Ana@García"    # Con símbolos
```

### **Validación de Edades**
```python
# ✅ Válidas
0, 18, 25, 65, 150

# ❌ Inválidas
-1              # Negativa
151             # Muy grande
"25"            # String
25.5            # Float
```

### **Validación de Correos**
```python
# ✅ Válidos
"test@ejemplo.com"
"usuario.nombre@dominio.org"
"test+tag@ejemplo.net"

# ❌ Inválidos
"correo_sin_arroba"
"correo@"
"@dominio.com"
"correo@@ejemplo.com"
```

## 📱 Menú Interactivo

El sistema incluye un menú completo con **9 opciones**:

```
👥 SISTEMA DE GESTIÓN DE PERSONAS
══════════════════════════════════════════════════════════
1. 🎬 Demo completa de la clase Persona
2. ➕ Crear nueva persona
3. 👁️ Mostrar todas las personas
4. 🔍 Buscar persona por nombre
5. 🔄 Actualizar datos de una persona
6. ⚖️ Comparar edades de dos personas
7. 📊 Ver estadísticas generales
8. 💾 Exportar personas a JSON
9. 📥 Importar personas desde JSON
0. 🚪 Salir
```

### Funcionalidades del Menú

#### **Opción 1: Demo Completa**
- Demostración automática de todas las funcionalidades
- Creación de personas de ejemplo
- Validaciones en tiempo real
- Comparaciones y estadísticas

#### **Opción 2-5: Gestión CRUD**
- **Crear:** Nueva persona con validaciones
- **Leer:** Mostrar todas las personas registradas
- **Buscar:** Filtrar por nombre
- **Actualizar:** Modificar datos existentes

#### **Opción 6: Ejercicio PLUS**
- Comparación interactiva entre dos personas
- Resultado detallado con diferencia de años

#### **Opción 7: Estadísticas**
- Total de personas creadas
- Edad promedio, mínima y máxima
- Porcentaje de correos válidos
- Porcentaje de mayores de edad

#### **Opción 8-9: Persistencia**
- Exportar todas las personas a archivo JSON
- Importar personas desde archivo JSON

## 📊 Estadísticas y Análisis

### Datos Tracked Automáticamente
```python
{
    'total_personas': 5,
    'edad_promedio': 28.4,
    'edad_minima': 17,
    'edad_maxima': 45,
    'correos_validos': 5,
    'porcentaje_correos_validos': 100.0,
    'mayores_de_edad': 4,
    'porcentaje_mayores_edad': 80.0
}
```

### Categorías de Edad
- **Niño/a:** < 13 años
- **Adolescente:** 13-17 años
- **Joven Adulto:** 18-29 años
- **Adulto:** 30-59 años
- **Adulto Mayor:** ≥ 60 años

### Generaciones
- **Generación Z:** Nacidos después de 1997
- **Millennial:** 1981-1996
- **Generación X:** 1965-1980
- **Baby Boomer:** 1946-1964
- **Generación Silenciosa:** Antes de 1946

## 💾 Persistencia de Datos

### Formato JSON
```json
{
  "id": 1,
  "nombre": "Ana García",
  "edad": 25,
  "correo_electronico": "ana@email.com",
  "es_mayor_de_edad": true,
  "categoria_edad": "Joven Adulto",
  "año_nacimiento": 1999,
  "generacion": "Generación Z",
  "fecha_creacion": "2024-06-17T15:30:00"
}
```

### Métodos de Serialización
```python
# Exportar
datos = persona.to_dict()
with open("personas.json", "w") as f:
    json.dump(datos, f, indent=2)

# Importar
with open("personas.json", "r") as f:
    datos = json.load(f)
persona = Persona.from_dict(datos)
```

## 🔧 Conceptos de POO Aplicados

### **Encapsulación**
- Atributos privados con validación (`_validar_nombre`, `_validar_edad`)
- Métodos públicos para interactuar con los datos
- Control de acceso a través de métodos

### **Abstracción**
- Interfaz simple para operaciones complejas
- Métodos que ocultan la complejidad de validación
- API limpia y fácil de usar

### **Métodos de Clase y Estáticos**
- `@classmethod` para operaciones a nivel de clase
- Contador automático de instancias
- Estadísticas globales

### **Métodos Especiales (Dunder Methods)**
- `__init__()` - Constructor personalizado
- `__str__()` - Representación legible
- `__repr__()` - Representación para debugging
- `__eq__()` - Comparación de igualdad
- `__lt__()` - Comparación menor que

## 🚨 Manejo de Errores

### Excepciones Personalizadas
```python
# Ejemplos de validaciones que lanzan ValueError
try:
    persona = Persona("", 25, "email@test.com")
except ValueError as e:
    print(f"Error: {e}")  # "El nombre no puede estar vacío"

try:
    persona = Persona("Ana", -5, "email@test.com")
except ValueError as e:
    print(f"Error: {e}")  # "La edad no puede ser negativa"
```

### Validación en Tiempo Real
- Correos inválidos revierten cambios automáticamente
- Nombres se formatean automáticamente
- Edades fuera de rango se rechazan

## 📈 Métricas del Proyecto

- **Líneas de código:** ~800 líneas
- **Métodos implementados:** 20+ métodos
- **Tests automatizados:** 25+ pruebas
- **Cobertura de funcionalidad:** 100%
- **Validaciones:** Completas en todos los campos
- **Manejo de errores:** Robusto y descriptivo

## 🎓 Conceptos de Ingeniería de Datos Aplicados

### **Validación de Datos**
- Limpieza automática de nombres
- Verificación de tipos de datos
- Validación de formatos (email con regex)

### **Estructuras de Datos**
- Uso eficiente de diccionarios para serialización
- Listas para tracking de instancias
- Manejo de timestamps

### **Análisis Estadístico**
- Cálculo de promedios y rangos
- Análisis demográfico (generaciones)
- Métricas de calidad de datos

### **Persistencia**
- Serialización JSON para intercambio de datos
- Esquemas de datos consistentes
- Import/Export para integración

## 🚀 Extensiones Futuras

### Ideas para Expandir el Proyecto
1. **Base de datos:** Integrar SQLite o PostgreSQL
2. **API REST:** Crear endpoints para CRUD operations
3. **Validaciones avanzadas:** Integrar con APIs de verificación
4. **Dashboard:** Crear interfaz web con Flask/Django
5. **Machine Learning:** Análisis predictivo de datos demográficos
6. **Exportación:** Soporte para CSV, Excel, XML
7. **Notificaciones:** Sistema de alertas por cumpleaños
8. **Búsqueda avanzada:** Filtros múltiples y ordenamiento

## 🤝 Contribución

### Cómo Contribuir
1. Fork el proyecto
2. Crear branch para nueva feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit los cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push al branch (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

### Standards de Código
- Seguir PEP 8 para estilo de código
- Incluir docstrings en todos los métodos
- Agregar tests para nuevas funcionalidades
- Mantener cobertura de tests al 100%

## 📚 Recursos Adicionales

### Documentación Relacionada
- [Python OOP Tutorial](https://docs.python.org/3/tutorial/classes.html)
- [Regular Expressions in Python](https://docs.python.org/3/library/re.html)
- [unittest Framework](https://docs.python.org/3/library/unittest.html)
- [JSON Handling](https://docs.python.org/3/library/json.html)

### Conceptos Clave Aprendidos
- **Programación Orientada a Objetos** en Python
- **Validación de datos** con regex y excepciones
- **Testing automatizado** con unittest
- **Serialización** y persistencia de objetos
- **Manejo de errores** robusto
- **Documentación** profesional de código

## 👨‍💻 Autor

**Bootcamp de Ingeniería de Datos**
- Clase 05: Programación Orientada a Objetos (POO)
- Proyecto: Sistema de Gestión de Personas
- Enfoque: Aplicación práctica de conceptos POO en ingeniería de datos

---

✅ **¡Proyecto completado exitosamente!** 🎉

*Este sistema demuestra la aplicación completa de POO en Python, incluyendo todas las características requeridas y funcionalidades avanzadas para un proyecto de ingeniería de datos profesional.*