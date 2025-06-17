# 📦 Clase 04: Sistema de Gestión de Inventario

## 📝 Descripción

Sistema completo de gestión de inventario desarrollado como parte del **Bootcamp de Ingeniería de Datos - Clase 04**. Este proyecto implementa estructuras de datos avanzadas en Python para manejar un inventario de productos con funcionalidades profesionales.

## 🎯 Objetivos Cumplidos

### ✅ Requisitos Básicos
- [x] Diccionario principal para representar inventario
- [x] Función `agregar_producto()` - Agregar productos al inventario
- [x] Función `eliminar_producto()` - Eliminar productos del inventario  
- [x] Función `actualizar_producto()` - Actualizar cantidad y precio
- [x] Función `listar_por_categoria()` - Listar productos por categoría
- [x] Función `calcular_valor_total()` - Calcular valor total del inventario

### ⭐ Ejercicio PLUS
- [x] Función `exportar_inventario_csv()` - Exportar a archivo CSV

### 🚀 Características Adicionales Implementadas
- [x] **Validación robusta** de todos los datos de entrada
- [x] **Manejo completo de errores** con try/catch
- [x] **Interfaz de usuario interactiva** con menú completo
- [x] **Búsqueda avanzada** por nombre o categoría
- [x] **Sistema de historial** de todos los movimientos
- [x] **Exportación múltiple** (CSV y JSON)
- [x] **Importación desde CSV** para carga masiva
- [x] **Alertas de stock bajo** configurables
- [x] **Estadísticas por categoría** detalladas
- [x] **Datos de prueba** para testing rápido

## 📁 Estructura del Proyecto

```
ejercicio-04-sistema-inventario/
├── sistema_inventario.py           # 🏗️ Clase principal del sistema
├── programa_inventario_interactivo.py  # 🖥️ Interfaz de usuario
├── demo_inventario.csv             # 📄 Archivo de ejemplo CSV
├── demo_inventario.json            # 📄 Archivo de ejemplo JSON
└── README.md                       # 📖 Esta documentación
```

## 🛠️ Instalación y Uso

### Prerrequisitos
- Python 3.6 o superior
- Módulos estándar: `csv`, `json`, `datetime`, `os`

### Ejecución Rápida

#### 1. **Programa Interactivo (Recomendado)**
```bash
python programa_inventario_interactivo.py
```

#### 2. **Demo Automática**
```bash
python sistema_inventario.py
```

#### 3. **Como Módulo**
```python
from sistema_inventario import SistemaInventario

# Crear instancia
inventario = SistemaInventario()

# Usar funciones
inventario.agregar_producto("Laptop", 10, 800.0, "Electrónica")
inventario.calcular_valor_total()
```

## 🔧 Funcionalidades Principales

### 📦 Gestión de Productos

| Función | Descripción | Parámetros |
|---------|-------------|------------|
| `agregar_producto()` | Agrega nuevo producto | `nombre, cantidad, precio, categoria` |
| `eliminar_producto()` | Elimina producto existente | `nombre` |
| `actualizar_producto()` | Actualiza datos del producto | `nombre, cantidad*, precio*, categoria*` |

*Parámetros opcionales

### 📊 Consultas y Reportes

| Función | Descripción | Retorno |
|---------|-------------|---------|
| `listar_por_categoria()` | Lista productos por categoría | `list` |
| `calcular_valor_total()` | Calcula valor total inventario | `float` |
| `buscar_producto()` | Busca por nombre/categoría | `list` |
| `obtener_productos_bajo_stock()` | Productos con stock bajo | `list` |
| `mostrar_resumen_categorias()` | Estadísticas por categoría | `None` |

### 💾 Import/Export

| Función | Descripción | Formato |
|---------|-------------|---------|
| `exportar_inventario_csv()` | Exporta a CSV | `.csv` |
| `exportar_inventario_json()` | Exporta a JSON | `.json` |
| `importar_inventario_csv()` | Importa desde CSV | `.csv` |

### 📋 Historial y Auditoría

| Función | Descripción |
|---------|-------------|
| `mostrar_historial_movimientos()` | Muestra historial de cambios |
| `_registrar_movimiento()` | Registra automáticamente todos los cambios |

## 💡 Ejemplos de Uso

### Ejemplo 1: Uso Básico
```python
from sistema_inventario import SistemaInventario

# Crear sistema
inventario = SistemaInventario()

# Agregar productos
inventario.agregar_producto("Laptop Dell", 15, 750.00, "Electrónica")
inventario.agregar_producto("Mouse", 50, 25.99, "Electrónica")

# Consultar valor total
valor = inventario.calcular_valor_total()
print(f"Valor total: ${valor:.2f}")

# Listar por categoría
inventario.listar_por_categoria("Electrónica")
```

### Ejemplo 2: Operaciones Avanzadas
```python
# Buscar productos
inventario.buscar_producto("laptop")

# Verificar stock bajo
productos_bajo_stock = inventario.obtener_productos_bajo_stock(10)

# Exportar datos
inventario.exportar_inventario_csv("mi_inventario.csv")
inventario.exportar_inventario_json("mi_inventario.json")

# Ver historial
inventario.mostrar_historial_movimientos(5)
```

### Ejemplo 3: Carga Masiva
```python
# Importar productos desde CSV
inventario.importar_inventario_csv("productos_iniciales.csv")

# Ver resumen por categorías
inventario.mostrar_resumen_categorias()
```

## 📱 Menú Interactivo

El programa principal ofrece un menú completo con 15 opciones:

```
📦 SISTEMA DE GESTIÓN DE INVENTARIO
════════════════════════════════════════════════════════════
1.  ➕ Agregar producto
2.  ❌ Eliminar producto  
3.  🔄 Actualizar producto
4.  📋 Listar por categoría
5.  💰 Calcular valor total
6.  🔍 Buscar productos
7.  📦 Mostrar inventario completo
8.  ⚠️  Productos con stock bajo
9.  📊 Resumen por categorías
10. 📋 Historial de movimientos
11. 💾 Exportar a CSV
12. 💾 Exportar a JSON
13. 📥 Importar desde CSV
14. 🧪 Cargar datos de prueba
15. 🗑️  Limpiar inventario
0.  🚪 Salir
```

## 🔒 Validaciones Implementadas

### Validación de Productos
- ✅ Nombres no vacíos y únicos
- ✅ Cantidades enteras no negativas
- ✅ Precios numéricos positivos
- ✅ Categorías válidas no vacías

### Validación de Operaciones
- ✅ Existencia de productos antes de eliminar/actualizar
- ✅ Formato correcto de archivos CSV/JSON
- ✅ Manejo de errores de E/O de archivos
- ✅ Validación de entrada del usuario

## 📊 Estructura de Datos

### Diccionario Principal
```python
inventario = {
    "Laptop Dell": {
        "cantidad": 15,
        "precio": 750.00,
        "categoria": "Electrónica",
        "fecha_agregado": "2024-06-17T15:30:00"
    },
    "Mouse Inalámbrico": {
        "cantidad": 50,
        "precio": 25.99,
        "categoria": "Electrónica", 
        "fecha_agregado": "2024-06-17T15:31:00"
    }
}
```

### Historial de Movimientos
```python
historial_movimientos = [
    {
        "timestamp": "2024-06-17T15:30:00",
        "tipo": "AGREGAR",
        "producto": "Laptop Dell",
        "cantidad": 15,
        "descripcion": "Producto agregado: 15 unidades a $750.00"
    }
]
```

## 📄 Formato de Archivos

### CSV Export
```csv
Producto,Cantidad,Precio,Categoría,Valor_Total,Fecha_Agregado
Laptop Dell,15,750.0,Electrónica,11250.0,2024-06-17T15:30:00
Mouse Inalámbrico,50,25.99,Electrónica,1299.5,2024-06-17T15:31:00
```

### JSON Export
```json
{
  "inventario": {
    "Laptop Dell": {
      "cantidad": 15,
      "precio": 750.0,
      "categoria": "Electrónica",
      "fecha_agregado": "2024-06-17T15:30:00"
    }
  },
  "historial_movimientos": [...],
  "fecha_exportacion": "2024-06-17T16:00:00",
  "total_productos": 2,
  "valor_total": 12549.5
}
```

## 🧪 Testing y Datos de Prueba

### Datos de Prueba Incluidos
- **Electrónica:** Laptops