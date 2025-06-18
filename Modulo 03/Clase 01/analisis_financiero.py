"""
ANÁLISIS DE CASO: Aplicación de NumPy en el Análisis de Datos Financieros
Módulo 3 - Obtención y Preparación de Datos
Bootcamp de Ingeniería de Datos
Fecha: Junio 2025
"""

import numpy as np
import time
import pandas as pd
from typing import Tuple, List

# Configuración para reproducibilidad
np.random.seed(42)

print("="*80)
print("ANÁLISIS FINANCIERO CON NUMPY")
print("Optimización de Datos para Empresa de Análisis Financiero")
print("="*80)

# ============================================================================
# 1. CARGA Y ESTRUCTURACIÓN DE DATOS
# ============================================================================

def crear_datos_financieros() -> Tuple[np.ndarray, List[str], List[str]]:
    """
    Crea datos financieros simulados para 5 acciones durante 5 días.
    
    Returns:
        Tuple con matriz de precios, nombres de acciones y fechas
    """
    print("\n1. CARGA Y ESTRUCTURACIÓN DE DATOS")
    print("-" * 50)
    
    # Nombres de las acciones
    acciones = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA']
    fechas = ['2025-06-13', '2025-06-14', '2025-06-16', '2025-06-17', '2025-06-18']
    
    # Precios base simulados (valores realistas)
    precios_base = np.array([150.0, 2800.0, 350.0, 3200.0, 800.0])
    
    # Crear matriz 5x5 con variaciones diarias realistas
    # Cada fila = acción, cada columna = día
    variaciones = np.random.normal(0, 0.02, (5, 5))  # Variaciones de ±2% promedio
    precios_matriz = precios_base.reshape(-1, 1) * (1 + variaciones)
    
    print(f"✓ Datos creados: Matriz {precios_matriz.shape}")
    print(f"✓ Acciones: {acciones}")
    print(f"✓ Período: {fechas[0]} a {fechas[-1]}")
    
    # Mostrar la matriz de precios
    print(f"\n📊 Matriz de Precios (Acciones x Días):")
    print("Acciones\\Días", end="")
    for i, fecha in enumerate(fechas):
        print(f"{fecha:>12}", end="")
    print()
    
    for i, accion in enumerate(acciones):
        print(f"{accion:>12}", end="")
        for j in range(5):
            print(f"{precios_matriz[i, j]:>12.2f}", end="")
        print()
    
    return precios_matriz, acciones, fechas

# ============================================================================
# 2. ANÁLISIS Y TRANSFORMACIÓN DE DATOS
# ============================================================================

def analisis_estadistico(precios: np.ndarray, acciones: List[str]) -> dict:
    """
    Realiza análisis estadístico básico de los datos.
    
    Args:
        precios: Matriz de precios (acciones x días)
        acciones: Lista de nombres de acciones
        
    Returns:
        Diccionario con estadísticas calculadas
    """
    print("\n2. ANÁLISIS Y TRANSFORMACIÓN DE DATOS")
    print("-" * 50)
    
    # Estadísticas básicas por acción (a lo largo del tiempo)
    promedios = np.mean(precios, axis=1)
    maximos = np.max(precios, axis=1)
    minimos = np.min(precios, axis=1)
    desviaciones = np.std(precios, axis=1)
    
    print("📈 ESTADÍSTICAS POR ACCIÓN:")
    print(f"{'Acción':<8} {'Promedio':<12} {'Máximo':<12} {'Mínimo':<12} {'Desv.Est':<12}")
    print("-" * 60)
    
    for i, accion in enumerate(acciones):
        print(f"{accion:<8} {promedios[i]:<12.2f} {maximos[i]:<12.2f} "
              f"{minimos[i]:<12.2f} {desviaciones[i]:<12.2f}")
    
    return {
        'promedios': promedios,
        'maximos': maximos,
        'minimos': minimos,
        'desviaciones': desviaciones
    }

def calcular_variaciones_porcentuales(precios: np.ndarray, acciones: List[str]) -> np.ndarray:
    """
    Calcula la variación porcentual diaria de cada acción.
    
    Args:
        precios: Matriz de precios
        acciones: Lista de nombres de acciones
        
    Returns:
        Matriz de variaciones porcentuales
    """
    print("\n💹 VARIACIONES PORCENTUALES DIARIAS:")
    
    # Calcular variaciones usando operaciones vectorizadas
    # Variación = (precio_actual - precio_anterior) / precio_anterior * 100
    variaciones = np.zeros((precios.shape[0], precios.shape[1] - 1))
    
    for i in range(1, precios.shape[1]):
        variaciones[:, i-1] = ((precios[:, i] - precios[:, i-1]) / precios[:, i-1]) * 100
    
    print(f"{'Acción':<8} {'Día 1→2':<10} {'Día 2→3':<10} {'Día 3→4':<10} {'Día 4→5':<10}")
    print("-" * 50)
    
    for i, accion in enumerate(acciones):
        print(f"{accion:<8}", end="")
        for j in range(4):
            print(f"{variaciones[i, j]:>9.2f}%", end=" ")
        print()
    
    return variaciones

def aplicar_transformaciones_matematicas(precios: np.ndarray) -> dict:
    """
    Aplica transformaciones matemáticas a los datos.
    
    Args:
        precios: Matriz de precios
        
    Returns:
        Diccionario con transformaciones aplicadas
    """
    print("\n🔢 TRANSFORMACIONES MATEMÁTICAS:")
    
    # Aplicar logaritmo natural (útil para rendimientos)
    log_precios = np.log(precios)
    
    # Aplicar normalización Z-score por acción
    precios_normalizados = (precios - np.mean(precios, axis=1, keepdims=True)) / \
                          np.std(precios, axis=1, keepdims=True)
    
    # Aplicar exponencial (para simulación de crecimiento)
    exp_factor = np.exp(precios / 1000)  # Dividir por 1000 para evitar overflow
    
    print(f"✓ Logaritmo natural aplicado - Rango: [{np.min(log_precios):.2f}, {np.max(log_precios):.2f}]")
    print(f"✓ Normalización Z-score aplicada - Media: {np.mean(precios_normalizados):.2f}")
    print(f"✓ Factor exponencial calculado - Rango: [{np.min(exp_factor):.2f}, {np.max(exp_factor):.2f}]")
    
    return {
        'log_precios': log_precios,
        'precios_normalizados': precios_normalizados,
        'exp_factor': exp_factor
    }

# ============================================================================
# 3. OPTIMIZACIÓN Y SELECCIÓN DE DATOS
# ============================================================================

def indexacion_avanzada(precios: np.ndarray, acciones: List[str], fechas: List[str]):
    """
    Demuestra técnicas de indexación avanzada.
    
    Args:
        precios: Matriz de precios
        acciones: Lista de nombres de acciones
        fechas: Lista de fechas
    """
    print("\n3. OPTIMIZACIÓN Y SELECCIÓN DE DATOS")
    print("-" * 50)
    
    print("🎯 INDEXACIÓN AVANZADA:")
    
    # Selección específica: AAPL en el día 3
    precio_especifico = precios[0, 2]  # AAPL (índice 0), día 3 (índice 2)
    print(f"✓ Precio de {acciones[0]} el {fechas[2]}: ${precio_especifico:.2f}")
    
    # Selección de múltiples acciones en un día específico
    precios_dia_1 = precios[:, 0]
    print(f"✓ Precios del primer día ({fechas[0]}):")
    for i, accion in enumerate(acciones):
        print(f"  {accion}: ${precios_dia_1[i]:.2f}")
    
    # Selección usando máscaras booleanas
    # Encontrar acciones con precio > 1000
    mask_alto_precio = precios[:, 0] > 1000
    acciones_alto_precio = np.array(acciones)[mask_alto_precio]
    print(f"✓ Acciones con precio inicial > $1000: {list(acciones_alto_precio)}")
    
    # Indexación fancy: seleccionar acciones específicas en días específicos
    indices_acciones = [0, 2, 4]  # AAPL, MSFT, TSLA
    indices_dias = [0, 2, 4]      # Días 1, 3, 5
    seleccion_fancy = precios[np.ix_(indices_acciones, indices_dias)]
    print(f"✓ Selección fancy (3x3): Forma {seleccion_fancy.shape}")

def demostracion_broadcasting(precios: np.ndarray):
    """
    Demuestra el uso de broadcasting para operaciones eficientes.
    
    Args:
        precios: Matriz de precios
    """
    print("\n⚡ BROADCASTING Y OPERACIONES VECTORIZADAS:")
    
    # Calcular porcentaje de cambio respecto al primer día usando broadcasting
    inicio = time.time()
    
    # Método con broadcasting (eficiente)
    primer_dia = precios[:, 0:1]  # Mantener dimensión para broadcasting
    cambio_porcentual = ((precios - primer_dia) / primer_dia) * 100
    
    tiempo_numpy = time.time() - inicio
    
    print(f"✓ Broadcasting completado en {tiempo_numpy:.6f} segundos")
    print(f"✓ Cambio porcentual respecto al primer día:")
    print(f"  Forma de la matriz resultado: {cambio_porcentual.shape}")
    print(f"  Rango de cambios: [{np.min(cambio_porcentual):.2f}%, {np.max(cambio_porcentual):.2f}%]")
    
    # Aplicar operación matemática a toda la matriz usando broadcasting
    factor_ajuste = np.array([1.02, 1.01, 1.03, 1.015, 1.025]).reshape(-1, 1)
    precios_ajustados = precios * factor_ajuste
    
    print(f"✓ Precios ajustados con factores específicos por acción aplicados")
    print(f"  Diferencia promedio: ${np.mean(precios_ajustados - precios):.2f}")

# ============================================================================
# 4. COMPARACIÓN CON OTROS MÉTODOS
# ============================================================================

def comparacion_metodos(precios: np.ndarray):
    """
    Compara la eficiencia de NumPy vs métodos tradicionales.
    
    Args:
        precios: Matriz de precios
    """
    print("\n4. COMPARACIÓN CON OTROS MÉTODOS")
    print("-" * 50)
    
    print("⏱️ COMPARACIÓN DE RENDIMIENTO:")
    
    # Crear datos más grandes para la comparación
    datos_grandes = np.random.rand(1000, 1000) * 100 + 50
    
    # Método con NumPy (vectorizado)
    inicio = time.time()
    promedio_numpy = np.mean(datos_grandes, axis=1)
    tiempo_numpy = time.time() - inicio
    
    # Método tradicional con bucles (simulado)
    inicio = time.time()
    promedio_bucles = []
    for fila in datos_grandes:
        suma = 0
        for valor in fila:
            suma += valor
        promedio_bucles.append(suma / len(fila))
    tiempo_bucles = time.time() - inicio
    
    print(f"✓ NumPy (vectorizado): {tiempo_numpy:.6f} segundos")
    print(f"✓ Bucles tradicionales: {tiempo_bucles:.6f} segundos")
    print(f"✓ NumPy es {tiempo_bucles/tiempo_numpy:.1f}x más rápido")
    
    # Comparación de uso de memoria
    print(f"\n💾 USO DE MEMORIA:")
    print(f"✓ NumPy array: {datos_grandes.nbytes / 1024:.1f} KB")
    print(f"✓ Lista Python equivalente: ~{datos_grandes.size * 28 / 1024:.1f} KB")
    print(f"✓ NumPy usa ~{28 / 8:.1f}x menos memoria")

def analisis_codigo_legibilidad():
    """
    Analiza la legibilidad y mantenibilidad del código.
    """
    print(f"\n📝 ANÁLISIS DE LEGIBILIDAD DEL CÓDIGO:")
    
    print("✓ SIN NUMPY (método tradicional):")
    print("""
    # Calcular promedio de cada fila
    promedios = []
    for i in range(len(datos)):
        suma = 0
        for j in range(len(datos[i])):
            suma += datos[i][j]
        promedios.append(suma / len(datos[i]))
    """)
    
    print("✓ CON NUMPY (método optimizado):")
    print("""
    # Calcular promedio de cada fila
    promedios = np.mean(datos, axis=1)
    """)
    
    print("👍 VENTAJAS DE NUMPY:")
    print("  • Código más conciso y legible")
    print("  • Menor posibilidad de errores")
    print("  • Mejor rendimiento computacional")
    print("  • Operaciones vectorizadas automáticas")

# ============================================================================
# 5. FUNCIÓN PRINCIPAL Y ANÁLISIS COMPLETO
# ============================================================================

def main():
    """
    Función principal que ejecuta todo el análisis.
    """
    print("🚀 Iniciando análisis financiero con NumPy...")
    
    # 1. Crear y cargar datos
    precios_matriz, acciones, fechas = crear_datos_financieros()
    
    # 2. Análisis estadístico
    estadisticas = analisis_estadistico(precios_matriz, acciones)
    variaciones = calcular_variaciones_porcentuales(precios_matriz, acciones)
    transformaciones = aplicar_transformaciones_matematicas(precios_matriz)
    
    # 3. Optimización y selección
    indexacion_avanzada(precios_matriz, acciones, fechas)
    demostracion_broadcasting(precios_matriz)
    
    # 4. Comparación de métodos
    comparacion_metodos(precios_matriz)
    analisis_codigo_legibilidad()
    
    # 5. Conclusiones
    print("\n" + "="*80)
    print("CONCLUSIONES DEL ANÁLISIS")
    print("="*80)
    
    print("\n🎯 RESULTADOS CLAVE:")
    print(f"✓ Procesamiento de {precios_matriz.size} puntos de datos")
    print(f"✓ {len(acciones)} acciones analizadas durante {len(fechas)} días")
    print(f"✓ Variación promedio del mercado: {np.mean(np.abs(variaciones)):.2f}%")
    print(f"✓ Acción más volátil: {acciones[np.argmax(estadisticas['desviaciones'])]}")
    print(f"✓ Acción más estable: {acciones[np.argmin(estadisticas['desviaciones'])]}")
    
    print("\n🏆 VENTAJAS DE NUMPY DEMOSTRADAS:")
    print("✓ Rendimiento: Hasta 10-100x más rápido que bucles tradicionales")
    print("✓ Memoria: Uso eficiente de memoria (3-4x menos que listas)")
    print("✓ Código: Más conciso y menos propenso a errores")
    print("✓ Funcionalidad: Operaciones matemáticas avanzadas integradas")
    print("✓ Broadcasting: Operaciones automáticas sin bucles explícitos")
    
    print("\n📋 RECOMENDACIONES PARA LA EMPRESA:")
    print("1. Migrar todos los cálculos financieros a NumPy")
    print("2. Usar broadcasting para operaciones en lote")
    print("3. Implementar indexación avanzada para consultas específicas")
    print("4. Aprovechar funciones vectorizadas para análisis en tiempo real")
    print("5. Considerar integración con pandas para manejo de datos tabulares")
    
    print(f"\n✅ Análisis completado exitosamente!")
    print("="*80)

# ============================================================================
# EJECUCIÓN DEL PROGRAMA
# ============================================================================

if __name__ == "__main__":
    main()

# ============================================================================
# CÓDIGO ADICIONAL PARA EXPERIMENTACIÓN
# ============================================================================

def ejemplo_uso_avanzado():
    """
    Ejemplos adicionales de uso avanzado de NumPy para análisis financiero.
    """
    print("\n🔬 EJEMPLOS DE USO AVANZADO:")
    
    # Simulación Monte Carlo simple
    np.random.seed(123)
    n_simulaciones = 1000
    rendimientos_diarios = np.random.normal(0.001, 0.02, n_simulaciones)  # 0.1% promedio, 2% volatilidad
    precios_simulados = 100 * np.cumprod(1 + rendimientos_diarios)
    
    print(f"✓ Simulación Monte Carlo de {n_simulaciones} días")
    print(f"  Precio final promedio: ${np.mean(precios_simulados[-100:]):.2f}")
    print(f"  Volatilidad simulada: {np.std(rendimientos_diarios)*100:.2f}%")
    
    # Correlación entre acciones (matriz de correlación)
    datos_correlacion = np.random.multivariate_normal([0, 0, 0], [[1, 0.5, 0.3], [0.5, 1, 0.7], [0.3, 0.7, 1]], 100)
    matriz_correlacion = np.corrcoef(datos_correlacion.T)
    print(f"✓ Matriz de correlación calculada: {matriz_correlacion.shape}")
    
    # Cálculo de métricas de riesgo
    rendimientos = np.random.normal(0.05, 0.15, 252)  # Un año de rendimientos
    var_95 = np.percentile(rendimientos, 5)  # Value at Risk al 95%
    sharpe_ratio = np.mean(rendimientos) / np.std(rendimientos)
    
    print(f"✓ VaR 95%: {var_95:.2%}")
    print(f"✓ Ratio de Sharpe: {sharpe_ratio:.2f}")

# Descomentar para ejecutar ejemplos avanzados
# ejemplo_uso_avanzado()