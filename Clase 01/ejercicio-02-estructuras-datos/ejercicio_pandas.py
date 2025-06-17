import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def crear_dataset_ventas():
    """Crea un dataset simulado de ventas."""
    print("📊 CREANDO DATASET DE VENTAS")
    print("=" * 35)
    
    # Generar datos simulados
    np.random.seed(42)  # Para reproducibilidad
    
    fechas = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
    productos = ['Laptop', 'Mouse', 'Teclado', 'Monitor', 'Tablet']
    regiones = ['Norte', 'Sur', 'Este', 'Oeste', 'Centro']
    
    # Crear dataset
    data = []
    for fecha in fechas:
        for _ in range(np.random.randint(1, 6)):  # 1-5 ventas por día
            data.append({
                'fecha': fecha,
                'producto': np.random.choice(productos),
                'region': np.random.choice(regiones),
                'cantidad': np.random.randint(1, 10),
                'precio_unitario': np.random.randint(50, 1500),
                'vendedor': f"Vendedor_{np.random.randint(1, 11)}"
            })
    
    df = pd.DataFrame(data)
    df['total_venta'] = df['cantidad'] * df['precio_unitario']
    
    print(f"Dataset creado con {len(df)} registros")
    print(f"Período: {df['fecha'].min()} a {df['fecha'].max()}")
    
    return df

def analisis_basico_pandas(df):
    """Análisis básico con Pandas."""
    print("\n🔍 ANÁLISIS BÁSICO CON PANDAS")
    print("=" * 35)
    
    # Información general
    print("📋 Información del dataset:")
    print(f"  Filas: {df.shape[0]}")
    print(f"  Columnas: {df.shape[1]}")
    print(f"  Memoria utilizada: {df.memory_usage(deep=True).sum() / 1024:.2f} KB")
    
    print(f"\n📈 Primeras 5 filas:")
    print(df.head())
    
    print(f"\n📊 Estadísticas descriptivas:")
    print(df.describe())
    
    # Análisis por categorías
    print(f"\n🏷️ Ventas por producto:")
    ventas_por_producto = df.groupby('producto')['total_venta'].sum().sort_values(ascending=False)
    for producto, total in ventas_por_producto.items():
        print(f"  {producto}: ${total:,.2f}")
    
    print(f"\n🌍 Ventas por región:")
    ventas_por_region = df.groupby('region')['total_venta'].sum().sort_values(ascending=False)
    for region, total in ventas_por_region.items():
        print(f"  {region}: ${total:,.2f}")

def analisis_temporal(df):
    """Análisis temporal de ventas."""
    print("\n📅 ANÁLISIS TEMPORAL")
    print("=" * 25)
    
    # Ventas por mes
    df['mes'] = df['fecha'].dt.month
    df['año'] = df['fecha'].dt.year
    
    ventas_mensuales = df.groupby('mes')['total_venta'].sum()
    
    print("💰 Ventas por mes:")
    meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 
             'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
    
    for mes, total in ventas_mensuales.items():
        print(f"  {meses[mes-1]}: ${total:,.2f}")
    
    # Tendencias
    mejor_mes = ventas_mensuales.idxmax()
    peor_mes = ventas_mensuales.idxmin()
    
    print(f"\n📈 Mejor mes: {meses[mejor_mes-1]} (${ventas_mensuales[mejor_mes]:,.2f})")
    print(f"📉 Peor mes: {meses[peor_mes-1]} (${ventas_mensuales[peor_mes]:,.2f})")

def analisis_avanzado(df):
    """Análisis avanzado con Pandas."""
    print("\n🧠 ANÁLISIS AVANZADO")
    print("=" * 25)
    
    # Top vendedores
    print("🏆 Top 5 vendedores:")
    top_vendedores = df.groupby('vendedor')['total_venta'].sum().sort_values(ascending=False).head(5)
    for i, (vendedor, total) in enumerate(top_vendedores.items(), 1):
        print(f"  {i}. {vendedor}: ${total:,.2f}")
    
    # Producto más popular por región
    print(f"\n🎯 Producto más vendido por región:")
    for region in df['region'].unique():
        df_region = df[df['region'] == region]
        producto_top = df_region.groupby('producto')['cantidad'].sum().idxmax()
        cantidad_top = df_region.groupby('producto')['cantidad'].sum().max()
        print(f"  {region}: {producto_top} ({cantidad_top} unidades)")
    
    # Análisis de correlación
    print(f"\n🔗 Correlación entre cantidad y precio:")
    correlacion = df['cantidad'].corr(df['precio_unitario'])
    print(f"  Correlación: {correlacion:.3f}")
    
    if correlacion > 0.1:
        print("  ↗️ Correlación positiva débil")
    elif correlacion < -0.1:
        print("  ↘️ Correlación negativa débil")
    else:
        print("  ↔️ Sin correlación significativa")

def ejercicio_filtrado(df):
    """Ejercicios de filtrado y consultas."""
    print("\n🔍 EJERCICIOS DE FILTRADO")
    print("=" * 30)
    
    # Ventas grandes (>$5000)
    ventas_grandes = df[df['total_venta'] > 5000]
    print(f"Ventas mayores a $5,000: {len(ventas_grandes)} registros")
    
    # Ventas en región Norte de Laptops
    laptops_norte = df[(df['producto'] == 'Laptop') & (df['region'] == 'Norte')]
    total_laptops_norte = laptops_norte['total_venta'].sum()
    print(f"Ventas de Laptops en región Norte: ${total_laptops_norte:,.2f}")
    
    # Ventas del último trimestre
    ultimo_trimestre = df[df['fecha'] >= '2024-10-01']
    total_q4 = ultimo_trimestre['total_venta'].sum()
    print(f"Ventas del último trimestre: ${total_q4:,.2f}")
    
    # Top 3 días con más ventas
    ventas_por_dia = df.groupby('fecha')['total_venta'].sum().sort_values(ascending=False).head(3)
    print(f"\nTop 3 días con más ventas:")
    for fecha, total in ventas_por_dia.items():
        print(f"  {fecha.strftime('%Y-%m-%d')}: ${total:,.2f}")

def main():
    """Función principal."""
    print("🐼 BOOTCAMP INGENIERÍA DE DATOS - PANDAS")
    print("=" * 45)
    
    # Crear y analizar dataset
    df_ventas = crear_dataset_ventas()
    analisis_basico_pandas(df_ventas)
    analisis_temporal(df_ventas)
    analisis_avanzado(df_ventas)
    ejercicio_filtrado(df_ventas)
    
    print(f"\n✅ ¡Ejercicio de Pandas completado!")
    print(f"📚 Has aprendido: DataFrames, groupby, filtrado, análisis temporal")

if __name__ == "__main__":
    main()