def procesar_ventas():
    """Simula el procesamiento de datos de ventas."""
    print("💰 PROCESAMIENTO DE DATOS DE VENTAS")
    print("=" * 40)
    
    # Datos simulados de ventas
    ventas_mensuales = {
        "enero": [1200, 1500, 1100, 1800, 1300],
        "febrero": [1400, 1600, 1200, 1900, 1500],
        "marzo": [1300, 1700, 1400, 2000, 1600],
        "abril": [1500, 1800, 1300, 2100, 1700]
    }
    
    # Análisis por mes
    for mes, ventas in ventas_mensuales.items():
        total = sum(ventas)
        promedio = total / len(ventas)
        maximo = max(ventas)
        minimo = min(ventas)
        
        print(f"\n📅 {mes.upper()}")
        print(f"  Total: ${total:,}")
        print(f"  Promedio: ${promedio:,.2f}")
        print(f"  Máximo: ${maximo:,}")
        print(f"  Mínimo: ${minimo:,}")
    
    # Análisis general
    todas_ventas = []
    for ventas in ventas_mensuales.values():
        todas_ventas.extend(ventas)
    
    total_general = sum(todas_ventas)
    promedio_general = total_general / len(todas_ventas)
    
    print(f"\n📊 RESUMEN GENERAL")
    print(f"Total de ventas: ${total_general:,}")
    print(f"Promedio por venta: ${promedio_general:,.2f}")
    print(f"Número de transacciones: {len(todas_ventas)}")
    
    return ventas_mensuales

def analizar_productos():
    """Analiza datos de productos."""
    print("\n🛍️ ANÁLISIS DE PRODUCTOS")
    print("=" * 30)
    
    # Inventario de productos
    productos = [
        {"nombre": "Laptop", "precio": 1200, "stock": 15, "categoria": "Tecnología"},
        {"nombre": "Mouse", "precio": 25, "stock": 50, "categoria": "Tecnología"},
        {"nombre": "Teclado", "precio": 80, "stock": 30, "categoria": "Tecnología"},
        {"nombre": "Monitor", "precio": 300, "stock": 20, "categoria": "Tecnología"},
        {"nombre": "Silla", "precio": 150, "stock": 25, "categoria": "Muebles"}
    ]
    
    # Valor total del inventario
    valor_total = sum(prod["precio"] * prod["stock"] for prod in productos)
    print(f"Valor total del inventario: ${valor_total:,}")
    
    # Producto más caro y más barato
    mas_caro = max(productos, key=lambda p: p["precio"])
    mas_barato = min(productos, key=lambda p: p["precio"])
    
    print(f"Producto más caro: {mas_caro['nombre']} (${mas_caro['precio']})")
    print(f"Producto más barato: {mas_barato['nombre']} (${mas_barato['precio']})")
    
    # Productos con poco stock (menos de 20)
    poco_stock = [p for p in productos if p["stock"] < 20]
    if poco_stock:
        print(f"\n⚠️ Productos con poco stock:")
        for prod in poco_stock:
            print(f"  - {prod['nombre']}: {prod['stock']} unidades")
    
    return productos

def transformar_datos():
    """Demuestra transformaciones de datos."""
    print("\n🔄 TRANSFORMACIÓN DE DATOS")
    print("=" * 35)
    
    # Datos en bruto (simulando CSV)
    datos_brutos = [
        "Ana,25,Engineer,75000",
        "Carlos,28,Data Scientist,85000",
        "María,24,Analyst,65000",
        "Pedro,26,Engineer,78000"
    ]
    
    # Transformar a estructura útil
    empleados = []
    for linea in datos_brutos:
        nombre, edad, puesto, salario = linea.split(",")
        empleado = {
            "nombre": nombre,
            "edad": int(edad),
            "puesto": puesto,
            "salario": int(salario)
        }
        empleados.append(empleado)
    
    print("📋 Datos transformados:")
    for emp in empleados:
        print(f"  {emp['nombre']}: {emp['puesto']} - ${emp['salario']:,}")
    
    # Análisis de salarios
    salario_promedio = sum(emp["salario"] for emp in empleados) / len(empleados)
    print(f"\n💰 Salario promedio: ${salario_promedio:,.2f}")
    
    return empleados

def main():
    """Función principal."""
    print("🔧 MANIPULACIÓN AVANZADA DE DATOS")
    print("=" * 45)
    
    ventas = procesar_ventas()
    productos = analizar_productos()
    empleados = transformar_datos()
    
    print(f"\n✅ Análisis de datos completado!")

if __name__ == "__main__":
    main()