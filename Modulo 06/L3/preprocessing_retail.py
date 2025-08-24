"""
Análisis de Caso: Preprocesamiento y escalamiento de datos
RetailData Analytics - Bootcamp de Ingeniería de Datos

Fecha: Agosto 2025
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler, MinMaxScaler
from sklearn.impute import SimpleImputer
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

print("="*60)
print("RETAILDATA ANALYTICS - PREPROCESAMIENTO DE DATOS")
print("="*60)

# 1. CREACIÓN DEL DATASET INICIAL
print("\n1. DATOS INICIALES")
print("-" * 30)

# Crear el dataframe con los datos proporcionados
data = {
    'ID': [1, 2, 3, 4],
    'Edad': [25, 45, 30, 40],
    'Ciudad': ['Madrid', 'Sevilla', 'Madrid', 'Barcelona'],
    'Ingresos(USD)': [30000, 50000, np.nan, 40000]
}

df_original = pd.DataFrame(data)
print("Datos originales:")
print(df_original)
print(f"\nInformación del dataset:")
print(f"Forma: {df_original.shape}")
print(f"Valores nulos por columna:")
print(df_original.isnull().sum())

# 2. IMPUTACIÓN DE VALORES FALTANTES
print("\n\n2. IMPUTACIÓN DE VALORES FALTANTES")
print("-" * 40)

df_processed = df_original.copy()

# Imputer para valores faltantes usando la media
imputer = SimpleImputer(strategy='mean')
df_processed['Ingresos(USD)'] = imputer.fit_transform(df_processed[['Ingresos(USD)']])

print("Después de imputar valores faltantes:")
print(df_processed)

media_ingresos = df_original['Ingresos(USD)'].mean()
print(f"\nMedia de ingresos utilizada para imputación: ${media_ingresos:,.2f}")

# 3. CODIFICACIÓN DE VARIABLES CATEGÓRICAS
print("\n\n3. CODIFICACIÓN DE VARIABLES CATEGÓRICAS")
print("-" * 45)

# 3.1 Label Encoding
print("\n3.1 Label Encoding:")
le = LabelEncoder()
df_processed['Ciudad_LabelEncoded'] = le.fit_transform(df_processed['Ciudad'])

print("Mapeo de Label Encoding:")
for i, ciudad in enumerate(le.classes_):
    print(f"  {ciudad} -> {i}")

print(f"\nDataframe con Label Encoding:")
print(df_processed[['Ciudad', 'Ciudad_LabelEncoded']])

# 3.2 One-Hot Encoding
print("\n3.2 One-Hot Encoding:")
df_onehot = pd.get_dummies(df_processed, columns=['Ciudad'], prefix='Ciudad')
print("DataFrame con One-Hot Encoding:")
print(df_onehot)

# 3.3 Variables Dummy (similar a One-Hot pero eliminando una categoría)
print("\n3.3 Variables Dummy:")
df_dummy = pd.get_dummies(df_processed, columns=['Ciudad'], prefix='Ciudad', drop_first=True)
print("DataFrame con Variables Dummy:")
print(df_dummy)

# 4. ESCALAMIENTO DE VARIABLES NUMÉRICAS
print("\n\n4. ESCALAMIENTO DE VARIABLES NUMÉRICAS")
print("-" * 45)

# Preparar datos para escalamiento
numerical_cols = ['Edad', 'Ingresos(USD)']
df_scaling = df_processed[['ID'] + numerical_cols].copy()

print("Datos antes del escalamiento:")
print(df_scaling)
print(f"\nEstadísticas descriptivas:")
print(df_scaling[numerical_cols].describe())

# 4.1 Normalización Min-Max
print("\n4.1 Normalización Min-Max (0-1):")
scaler_minmax = MinMaxScaler()
df_minmax = df_scaling.copy()
df_minmax[numerical_cols] = scaler_minmax.fit_transform(df_scaling[numerical_cols])

print("Datos normalizados (Min-Max):")
print(df_minmax)
print(f"\nRangos después de Min-Max:")
for col in numerical_cols:
    print(f"  {col}: [{df_minmax[col].min():.3f}, {df_minmax[col].max():.3f}]")

# 4.2 Estandarización Z-Score
print("\n4.2 Estandarización Z-Score:")
scaler_standard = StandardScaler()
df_standardized = df_scaling.copy()
df_standardized[numerical_cols] = scaler_standard.fit_transform(df_scaling[numerical_cols])

print("Datos estandarizados (Z-Score):")
print(df_standardized)
print(f"\nMedia y desviación estándar después de Z-Score:")
for col in numerical_cols:
    print(f"  {col}: μ={df_standardized[col].mean():.3f}, σ={df_standardized[col].std():.3f}")

# 5. COMPARACIÓN VISUAL DE LOS MÉTODOS DE ESCALAMIENTO
print("\n\n5. COMPARACIÓN VISUAL")
print("-" * 25)

plt.figure(figsize=(15, 10))

# Configurar el estilo
plt.style.use('default')
sns.set_palette("husl")

# Subplot 1: Datos originales
plt.subplot(2, 3, 1)
plt.scatter(df_scaling['Edad'], df_scaling['Ingresos(USD)'], s=100, alpha=0.7)
plt.title('Datos Originales', fontsize=12, fontweight='bold')
plt.xlabel('Edad')
plt.ylabel('Ingresos (USD)')
plt.grid(True, alpha=0.3)

# Subplot 2: Normalización Min-Max
plt.subplot(2, 3, 2)
plt.scatter(df_minmax['Edad'], df_minmax['Ingresos(USD)'], s=100, alpha=0.7, color='orange')
plt.title('Normalización Min-Max', fontsize=12, fontweight='bold')
plt.xlabel('Edad (normalizada)')
plt.ylabel('Ingresos (normalizados)')
plt.grid(True, alpha=0.3)

# Subplot 3: Estandarización Z-Score
plt.subplot(2, 3, 3)
plt.scatter(df_standardized['Edad'], df_standardized['Ingresos(USD)'], s=100, alpha=0.7, color='green')
plt.title('Estandarización Z-Score', fontsize=12, fontweight='bold')
plt.xlabel('Edad (estandarizada)')
plt.ylabel('Ingresos (estandarizados)')
plt.grid(True, alpha=0.3)

# Histogramas comparativos
plt.subplot(2, 3, 4)
plt.hist(df_scaling['Edad'], alpha=0.7, label='Original', bins=3)
plt.hist(df_minmax['Edad'], alpha=0.7, label='Min-Max', bins=3)
plt.hist(df_standardized['Edad'], alpha=0.7, label='Z-Score', bins=3)
plt.title('Distribución de Edad', fontsize=12, fontweight='bold')
plt.legend()
plt.grid(True, alpha=0.3)

plt.subplot(2, 3, 5)
plt.hist(df_scaling['Ingresos(USD)'], alpha=0.7, label='Original', bins=3)
plt.hist(df_minmax['Ingresos(USD)'], alpha=0.7, label='Min-Max', bins=3)
plt.hist(df_standardized['Ingresos(USD)'], alpha=0.7, label='Z-Score', bins=3)
plt.title('Distribución de Ingresos', fontsize=12, fontweight='bold')
plt.legend()
plt.grid(True, alpha=0.3)

# Boxplots comparativos
plt.subplot(2, 3, 6)
data_comparison = pd.DataFrame({
    'Edad_Original': df_scaling['Edad'],
    'Edad_MinMax': df_minmax['Edad'],
    'Edad_ZScore': df_standardized['Edad'],
    'Ingresos_Original': df_scaling['Ingresos(USD)']/10000,  # Escalar para visualización
    'Ingresos_MinMax': df_minmax['Ingresos(USD)'],
    'Ingresos_ZScore': df_standardized['Ingresos(USD)']
})
plt.boxplot([data_comparison['Edad_Original'], data_comparison['Edad_MinMax'], 
             data_comparison['Edad_ZScore']], 
           labels=['Original', 'Min-Max', 'Z-Score'])
plt.title('Comparación Edad', fontsize=12, fontweight='bold')
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# 6. DATASET FINAL TRANSFORMADO
print("\n\n6. DATASET FINAL TRANSFORMADO")
print("-" * 35)

# Crear el dataset final combinando todas las transformaciones
df_final = pd.DataFrame({
    'ID': df_processed['ID'],
    'Edad_Original': df_processed['Edad'],
    'Ingresos_Original': df_processed['Ingresos(USD)'],
    'Ciudad_Original': df_processed['Ciudad'],
    'Ciudad_LabelEncoded': df_processed['Ciudad_LabelEncoded'],
    'Edad_MinMax': df_minmax['Edad'],
    'Ingresos_MinMax': df_minmax['Ingresos(USD)'],
    'Edad_ZScore': df_standardized['Edad'],
    'Ingresos_ZScore': df_standardized['Ingresos(USD)']
})

# Agregar columnas de One-Hot Encoding
for col in df_onehot.columns:
    if col.startswith('Ciudad_'):
        df_final[col] = df_onehot[col].values

print("Dataset final con todas las transformaciones:")
print(df_final)

# Guardar el dataset transformado
df_final.to_csv('retail_data_transformado.csv', index=False)
df_final.to_excel('retail_data_transformado.xlsx', index=False)

print(f"\n✅ Archivos guardados:")
print(f"   - retail_data_transformado.csv")
print(f"   - retail_data_transformado.xlsx")

# 7. RESUMEN DE TRANSFORMACIONES APLICADAS
print("\n\n7. RESUMEN DE TRANSFORMACIONES")
print("-" * 40)

transformaciones = {
    "Imputación": "Se reemplazó el valor faltante en Ingresos con la media ($40,000)",
    "Label Encoding": "Barcelona=0, Madrid=1, Sevilla=2",
    "One-Hot Encoding": "3 columnas binarias: Ciudad_Barcelona, Ciudad_Madrid, Ciudad_Sevilla",
    "Variables Dummy": "2 columnas binarias eliminando la primera categoría",
    "Min-Max Scaling": "Normalización al rango [0,1] para Edad e Ingresos",
    "Z-Score Scaling": "Estandarización con media=0 y desviación=1"
}

for i, (metodo, descripcion) in enumerate(transformaciones.items(), 1):
    print(f"{i}. {metodo}: {descripcion}")

print("\n" + "="*60)
print("PREPROCESAMIENTO COMPLETADO EXITOSAMENTE")
print("="*60)