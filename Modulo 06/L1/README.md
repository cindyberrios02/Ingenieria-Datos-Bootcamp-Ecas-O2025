# Análisis de Caso - Fundamentos del Aprendizaje de Máquina

## DataSolutions S.A. - Bootcamp de Ingeniería de Datos

Este repositorio contiene la implementación completa del análisis de caso para tres problemas de aprendizaje de máquina en DataSolutions S.A.

## 📁 Estructura del Proyecto

```
├── README.md                          # Este archivo
├── informe_analisis_caso.md          # Informe completo del análisis
├── flujo_trabajo_ml.html              # Esquema gráfico del flujo de trabajo
├── churn_prediction_complete.py       # Implementación completa de detección de churn
├── requirements.txt                   # Dependencias del proyecto
└── data/                              # Carpeta para datos (opcional)
```

## 🚀 Instalación y Configuración

### Prerrequisitos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Instalación de Dependencias

```bash
# Clonar el repositorio
git clone https://github.com/cindyberrios02/Ingenieria-Datos-Bootcamp-Ecas-O2025
cd ml-case-analysis

# Crear entorno virtual (recomendado)
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### Archivo requirements.txt
```
pandas>=1.5.0
numpy>=1.21.0
scikit-learn>=1.1.0
matplotlib>=3.5.0
seaborn>=0.11.0
plotly>=5.10.0
jupyter>=1.0.0
```

## 📊 Uso del Código

### Ejecución del Pipeline Completo

```python
from churn_prediction_complete import ChurnPredictor

# Instanciar el predictor
churn_predictor = ChurnPredictor()

# Ejecutar pipeline completo
results = churn_predictor.run_complete_pipeline()

# Ver resultados
print(f"ROI proyectado: {results['roi']:.1f}%")
print(f"Beneficio neto: ${results['net_benefit']:,.2f}")
```

### Ejecución Paso a Paso

```python
# Cargar y explorar datos
churn_predictor = ChurnPredictor()
df = churn_predictor.load_and_explore_data()

# Análisis exploratorio
churn_predictor.exploratory_data_analysis()

# Preprocesamiento
X, y = churn_predictor.data_preprocessing()

# División de datos
X_train, X_test, y_train, y_test = churn_predictor.split_and_scale_data()

# Entrenamiento
model_results = churn_predictor.train_models()

# Evaluación
churn_predictor.evaluate_model()

# Análisis de impacto
business_impact = churn_predictor.business_impact_analysis()
```

## 📋 Contenido de los Entregables

### 1. Informe Escrito (`informe_analisis_caso.md`)

**Incluye:**
- ✅ Clasificación de cada problema (Regresión, Clasificación, Clustering)
- ✅ Modelos propuestos y justificación técnica
- ✅ Análisis detallado de riesgos y desafíos
- ✅ Reflexión personal sobre aplicación práctica
- ✅ Propuesta de métricas de evaluación para cada modelo

**Problemas analizados:**
- **Problema A**: Predicción de ventas semanales (Regresión - Random Forest)
- **Problema B**: Detección de churn (Clasificación - Gradient Boosting)  
- **Problema C**: Segmentación de clientes (Clustering - K-Means + PCA)

### 2. Esquema Gráfico (`flujo_trabajo_ml.html`)

**Flujo completo para detección de churn:**
- 🎯 Fase 1: Entendimiento del problema
- 📊 Fase 2: Recolección y exploración de datos
- 🔧 Fase 3: Preparación y limpieza de datos
- 🤖 Fase 4: Modelado y entrenamiento
- 📈 Fase 5: Evaluación y validación
- 🚀 Fase 6: Despliegue e implementación
- 📊 Fase 7: Monitoreo y mantenimiento continuo

### 3. Implementación Práctica (`churn_prediction_complete.py`)

**Características del código:**
- Pipeline completo automatizado
- Generación de datos sintéticos realistas
- Análisis exploratorio con visualizaciones
- Feature engineering avanzado
- Comparación de múltiples modelos
- Evaluación con métricas de negocio
- Análisis de ROI y impacto financiero
- Recomendaciones estratégicas

## 🔧 Funcionalidades Principales

### Clase ChurnPredictor

```python
# Métodos principales:
load_and_explore_data()          # Carga y exploración inicial
exploratory_data_analysis()      # EDA con visualizaciones
data_preprocessing()             # Feature engineering
split_and_scale_data()          # División y escalado
train_models()                  # Entrenamiento de modelos
evaluate_model()                # Evaluación completa
business_impact_analysis()      # Análisis de ROI
generate_recommendations()      # Recomendaciones estratégicas
run_complete_pipeline()         # Ejecución completa
```

### Métricas Implementadas

**Para Clasificación (Churn):**
- Precision, Recall, F1-Score
- AUC-ROC y curvas ROC
- Matriz de confusión
- Análisis de importancia de variables
- Métricas de negocio (ROI, beneficio neto)

**Para Regresión (Ventas):**
- RMSE, MAE, MAPE
- R² (coeficiente de determinación)
- Análisis de residuos

**Para Clustering (Segmentación):**
- Silhouette Score
- Inertia/WCSS
- Calinski-Harabasz Index

## 📊 Visualizaciones Incluidas

- Matriz de correlación
- Distribuciones de churn por categorías
- Matriz de confusión
- Curvas ROC
- Importancia de variables
- Método del codo para clustering

## 🎓 Aspectos Educativos

### Conceptos Implementados:
- **Aprendizaje Supervisado**: Regresión y Clasificación
- **Aprendizaje No Supervisado**: Clustering
- **Feature Engineering**: Creación de variables derivadas
- **Validación Cruzada**: Evaluación robusta de modelos
- **Manejo de Desbalance**: Class weights y SMOTE
- **Métricas de Negocio**: ROI y análisis financiero

### Buenas Prácticas:
- **División temporal**: Evitar data leakage en series temporales
- **Escalado de variables**: Normalización para algoritmos sensibles a escala
- **Validación estratificada**: Mantener distribución de clases
- **Regularización**: Prevención de overfitting
- **Interpretabilidad**: Balance entre performance y explicabilidad

## 🔍 Ejemplo de Salida del Programa

```
🚀 INICIANDO PIPELINE COMPLETO DE DETECCIÓN DE CHURN
============================================================

=== FASE 1-2: EXPLORACIÓN DE DATOS ===
Dataset cargado: (10000, 13)
Tasa de churn: 28.45%

=== ANÁLISIS EXPLORATORIO ===
Estadísticas descriptivas:
[Matriz de correlación y gráficos]

=== FASE 3: PREPROCESAMIENTO ===
Aplicando feature engineering...
Features creadas: 20
Nuevas features:
  - charges_per_month
  - usage_intensity
  - is_heavy_user
  - is_recent_user
  - high_support_usage

=== DIVISIÓN Y ESCALADO DE DATOS ===
Conjunto de entrenamiento: (8000, 20)
Conjunto de prueba: (2000, 20)

=== FASE 4: ENTRENAMIENTO DE MODELOS ===
Entrenando Logistic Regression...
Validación cruzada F1: 0.745 (+/- 0.032)
Test F1: 0.752

Entrenando Random Forest...
Validación cruzada F1: 0.798 (+/- 0.028)
Test F1: 0.805

Mejor modelo seleccionado: Random Forest

=== FASE 5: EVALUACIÓN DEL MODELO ===
Reporte de Clasificación:
              precision    recall  f1-score   support
           0       0.89      0.92      0.90      1431
           1       0.73      0.67      0.70       569
    accuracy                           0.85      2000

=== ANÁLISIS DE IMPACTO DE NEGOCIO ===
Clientes identificados como alto riesgo: 485
Verdaderos positivos (churners detectados): 381
Falsos positivos (falsa alarma): 104

--- ANÁLISIS FINANCIERO ---
Ingresos potencialmente salvados: $228,600.00
Costo de campaña de retención: $7,275.00
Beneficio neto: $221,325.00
ROI: 3041.2%

=== RECOMENDACIONES ESTRATÉGICAS ===
1. IMPLEMENTACIÓN INMEDIATA:
   - Desplegar modelo en producción con umbral de 0.5
   - Configurar pipeline automático de scoring semanal

✅ PIPELINE COMPLETADO EXITOSAMENTE

📊 RESUMEN EJECUTIVO:
ROI proyectado: 3041.2%
Beneficio neto estimado: $221,325.00
Clientes de alto riesgo identificados: 485
```

## 🎯 Casos de Uso Adicionales

### 1. Problema A - Predicción de Ventas

```python
from churn_prediction_complete import SalesPredictor

# Crear instancia
sales_predictor = SalesPredictor()

# Preparar features específicas para ventas
df_sales = sales_predictor.prepare_sales_features(df_ventas)

# Entrenar modelo de regresión
sales_predictor.train_sales_model(df_sales)
```

### 2. Problema C - Segmentación de Clientes

```python
from churn_prediction_complete import CustomerSegmentation

# Crear instancia
segmentation = CustomerSegmentation(n_clusters=5)

# Preparar features para clustering
features = segmentation.prepare_clustering_features(df_clientes)

# Encontrar número óptimo de clusters
segmentation.find_optimal_clusters(features)

# Aplicar clustering
clusters = segmentation.fit_transform(features)
```

## 📈 Extensiones Sugeridas

### Para Mejorar el Proyecto:

1. **Datos Reales**: Reemplazar datos sintéticos con datasets reales
2. **Modelos Avanzados**: Implementar XGBoost, LightGBM, Neural Networks
3. **Feature Store**: Sistema centralizado de características
4. **MLOps**: Pipeline CI/CD para modelos en producción
5. **Monitoring**: Dashboard en tiempo real para drift detection
6. **A/B Testing**: Framework para comparar versiones de modelos

### Tecnologías Complementarias:

```python
# Ejemplo con MLflow para tracking
import mlflow
import mlflow.sklearn

with mlflow.start_run():
    mlflow.log_params(model.get_params())
    mlflow.log_metrics({"f1_score": f1, "auc_roc": auc})
    mlflow.sklearn.log_model(model, "model")
```

## 🐛 Troubleshooting

### Problemas Comunes:

**Error de importación:**
```bash
pip install --upgrade scikit-learn pandas numpy matplotlib seaborn
```

**Problemas de memoria con datasets grandes:**
```python
# Usar chunking para datasets grandes
chunk_size = 1000
for chunk in pd.read_csv('large_file.csv', chunksize=chunk_size):
    process_chunk(chunk)
```

**Visualizaciones no aparecen:**
```python
import matplotlib.pyplot as plt
plt.ion()  # Modo interactivo
plt.show()
```

## 📚 Referencias y Recursos Adicionales

### Documentación:
- [Scikit-learn Documentation](https://scikit-learn.org/stable/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Matplotlib Documentation](https://matplotlib.org/stable/contents.html)

### Datasets para Práctica:
- [Kaggle Telco Customer Churn](https://www.kaggle.com/blastchar/telco-customer-churn)
- [UCI ML Repository](https://archive.ics.uci.edu/ml/index.php)
- [Google Dataset Search](https://datasetsearch.research.google.com/)

### Libros Recomendados:
- "Hands-On Machine Learning" - Aurélien Géron
- "Pattern Recognition and Machine Learning" - Christopher Bishop
- "The Elements of Statistical Learning" - Hastie, Tibshirani, Friedman

## 🤝 Contribuciones

Para contribuir al proyecto:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crea un Pull Request


