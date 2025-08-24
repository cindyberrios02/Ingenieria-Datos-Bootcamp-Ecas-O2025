import pandas as pd
import numpy as np
from sklearn.datasets import make_classification
import matplotlib.pyplot as plt
import seaborn as sns

# Configurar semilla para reproducibilidad
np.random.seed(42)

def generate_credit_dataset(n_samples=10000):
    """
    Genera un dataset simulado para evaluación crediticia
    """
    
    # Generar datos base con make_classification
    X, y = make_classification(
        n_samples=n_samples,
        n_features=10,
        n_informative=8,
        n_redundant=2,
        n_clusters_per_class=1,
        random_state=42,
        class_sep=0.8
    )
    
    # Crear DataFrame con características realistas
    df = pd.DataFrame()
    
    # Variables numéricas
    df['age'] = np.random.normal(35, 12, n_samples).clip(18, 80).astype(int)
    df['income'] = np.random.lognormal(10, 0.5, n_samples).clip(20000, 200000)
    df['employment_length'] = np.random.exponential(5, n_samples).clip(0, 40)
    df['debt_to_income'] = np.random.beta(2, 5, n_samples) * 0.8
    df['credit_history_length'] = np.random.exponential(8, n_samples).clip(0, 50)
    df['number_of_accounts'] = np.random.poisson(3, n_samples).clip(0, 15)
    df['credit_utilization'] = np.random.beta(2, 3, n_samples)
    df['payment_history'] = np.random.beta(8, 2, n_samples)
    
    # Variables categóricas
    education_levels = ['High School', 'Bachelor', 'Master', 'PhD', 'Other']
    employment_types = ['Full-time', 'Part-time', 'Self-employed', 'Unemployed']
    
    df['education_level'] = np.random.choice(education_levels, n_samples, 
                                           p=[0.3, 0.4, 0.2, 0.05, 0.05])
    df['employment_type'] = np.random.choice(employment_types, n_samples,
                                           p=[0.7, 0.15, 0.1, 0.05])
    
    # Crear variable objetivo con lógica de negocio realista
    # Factores que influyen positivamente en la aprobación:
    income_score = (df['income'] - df['income'].min()) / (df['income'].max() - df['income'].min())
    age_score = np.where((df['age'] >= 25) & (df['age'] <= 65), 1, 0.5)
    employment_score = np.where(df['employment_length'] > 2, 1, 0.5)
    debt_score = 1 - df['debt_to_income']
    credit_history_score = np.minimum(df['credit_history_length'] / 10, 1)
    payment_score = df['payment_history']
    utilization_score = 1 - df['credit_utilization']
    
    # Puntuación educativa
    education_scores = {'PhD': 1.0, 'Master': 0.9, 'Bachelor': 0.8, 'High School': 0.6, 'Other': 0.5}
    education_score = df['education_level'].map(education_scores)
    
    # Puntuación de empleo
    employment_scores = {'Full-time': 1.0, 'Self-employed': 0.8, 'Part-time': 0.6, 'Unemployed': 0.2}
    employment_type_score = df['employment_type'].map(employment_scores)
    
    # Combinar scores con pesos
    final_score = (
        income_score * 0.25 +
        age_score * 0.1 +
        employment_score * 0.15 +
        debt_score * 0.2 +
        credit_history_score * 0.1 +
        payment_score * 0.15 +
        utilization_score * 0.05 +
        education_score * 0.05 +
        employment_type_score * 0.1
    )
    
    # Agregar ruido para hacer el problema más realista
    noise = np.random.normal(0, 0.1, n_samples)
    final_score += noise
    
    # Convertir a clasificación binaria
    threshold = np.percentile(final_score, 70)  # 70% aprobación
    df['approved'] = (final_score > threshold).astype(int)
    
    # Introducir algunos valores faltantes de manera realística
    missing_mask = np.random.random(n_samples) < 0.05
    df.loc[missing_mask, 'employment_length'] = np.nan
    
    missing_mask = np.random.random(n_samples) < 0.03
    df.loc[missing_mask, 'credit_history_length'] = np.nan
    
    return df

# Generar el dataset
df = generate_credit_dataset()

# Mostrar información básica del dataset
print("=== INFORMACIÓN DEL DATASET ===")
print(f"Shape: {df.shape}")
print(f"Valores faltantes por columna:")
print(df.isnull().sum())
print()

print("=== DISTRIBUCIÓN DE LA VARIABLE OBJETIVO ===")
print(df['approved'].value_counts(normalize=True))
print()

print("=== ESTADÍSTICAS DESCRIPTIVAS ===")
print(df.describe())

# Guardar el dataset
df.to_csv('credit_data.csv', index=False)
print("\nDataset guardado como 'credit_data.csv'")

# Función para análisis exploratorio rápido
def quick_eda(df):
    """
    Análisis exploratorio rápido del dataset
    """
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle('Análisis Exploratorio - Variables Numéricas Clave', fontsize=16)
    
    # Variables numéricas importantes
    numeric_vars = ['income', 'age', 'debt_to_income', 'credit_utilization', 'payment_history']
    
    for i, var in enumerate(numeric_vars):
        row, col = i // 3, i % 3
        sns.boxplot(data=df, x='approved', y=var, ax=axes[row, col])
        axes[row, col].set_title(f'Distribución de {var} por aprobación')
    
    # Matriz de correlación
    axes[1, 2].clear()
    correlation_matrix = df.select_dtypes(include=[np.number]).corr()
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0,
                ax=axes[1, 2], cbar_kws={'shrink': 0.8})
    axes[1, 2].set_title('Matriz de Correlación')
    
    plt.tight_layout()
    plt.show()
    
    # Análisis de variables categóricas
    fig, axes = plt.subplots(1, 2, figsize=(15, 5))
    
    # Distribución por nivel educativo
    pd.crosstab(df['education_level'], df['approved'], normalize='index').plot(
        kind='bar', ax=axes[0], title='Tasa de Aprobación por Nivel Educativo'
    )
    axes[0].legend(['Rechazado', 'Aprobado'])
    axes[0].tick_params(axis='x', rotation=45)
    
    # Distribución por tipo de empleo
    pd.crosstab(df['employment_type'], df['approved'], normalize='index').plot(
        kind='bar', ax=axes[1], title='Tasa de Aprobación por Tipo de Empleo'
    )
    axes[1].legend(['Rechazado', 'Aprobado'])
    axes[1].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.show()

# Ejecutar EDA si se ejecuta directamente
if __name__ == "__main__":
    print("\n=== EJECUTANDO ANÁLISIS EXPLORATORIO ===")
    quick_eda(df)