# Estructura Completa del Proyecto MLlib E-commerce

## 📁 Estructura de Directorios

```
mllib-ecommerce-analysis/
│
├── 📄 README.md                              # Documentación principal
├── 📄 requirements.txt                       # Dependencias Python
├── 📄 .gitignore                            # Archivos ignorados por Git
├── 📄 LICENSE                               # Licencia del proyecto
├── 📄 setup.py                              # Configuración de instalación
│
├── 📁 data/                                 # Datos del proyecto
│   ├── 📄 generate_sample_data.py           # Generador de datos sintéticos
│   ├── 📄 sample_ecommerce_data.csv         # Dataset principal
│   ├── 📄 data_validation.py                # Validación de calidad de datos
│   └── 📁 raw/                              # Datos crudos (no procesados)
│
├── 📁 src/                                  # Código fuente principal
│   ├── 📄 __init__.py
│   ├── 📄 ecommerce_ml_analysis.py          # Clase principal de análisis
│   ├── 📄 data_preprocessing.py             # Preprocesamiento de datos
│   ├── 📄 feature_engineering.py            # Ingeniería de características
│   ├── 📄 model_training.py                 # Entrenamiento de modelos
│   ├── 📄 model_evaluation.py               # Evaluación de modelos
│   └── 📄 utils.py                          # Utilidades generales
│
├── 📁 notebooks/                            # Jupyter Notebooks
│   ├── 📄 01_data_exploration.ipynb         # Análisis exploratorio
│   ├── 📄 02_feature_engineering.ipynb      # Ingeniería de características
│   ├── 📄 03_model_development.ipynb        # Desarrollo de modelos
│   ├── 📄 04_model_evaluation.ipynb         # Evaluación detallada
│   └── 📄 ecommerce_prediction_analysis.ipynb # Notebook principal completo
│
├── 📁 scripts/                              # Scripts de automatización
│   ├── 📄 run_pipeline.py                   # Pipeline principal
│   ├── 📄 train_models.py                   # Script de entrenamiento
│   ├── 📄 evaluate_models.py                # Script de evaluación
│   ├── 📄 deploy_model.py                   # Script de deployment
│   └── 📄 monitor_model.py                  # Script de monitoreo
│
├── 📁 models/                               # Modelos entrenados
│   ├── 📁 trained_models/                   # Modelos guardados
│   │   ├── 📄 logistic_regression/
│   │   └── 📄 random_forest/
│   ├── 📁 experiments/                      # Experimentos de hyperparameters
│   └── 📄 model_registry.json               # Registro de modelos
│
├── 📁 reports/                              # Reportes y resultados
│   ├── 📄 model_performance_report.md       # Reporte principal
│   ├── 📄 executive_summary.md              # Resumen ejecutivo
│   ├── 📄 technical_documentation.md        # Documentación técnica
│   ├── 📁 visualizations/                   # Gráficos y visualizaciones
│   │   ├── 📄 model_comparison.png
│   │   ├── 📄 feature_importance.png
│   │   └── 📄 confusion_matrix.png
│   └── 📁 experiments/                      # Reportes de experimentos
│
├── 📁 config/                               # Configuraciones
│   ├── 📄 spark_config.json                # Configuración de Spark
│   ├── 📄 model_config.json                # Configuración de modelos
│   └── 📄 deployment_config.yaml           # Configuración de despliegue
│
├── 📁 tests/                                # Tests unitarios
│   ├── 📄 __init__.py
│   ├── 📄 test_data_preprocessing.py        # Tests de preprocesamiento
│   ├── 📄 test_feature_engineering.py       # Tests de features
│   ├── 📄 test_model_training.py            # Tests de entrenamiento
│   └── 📄 test_model_evaluation.py          # Tests de evaluación
│
├── 📁 deployment/                           # Archivos de despliegue
│   ├── 📄 Dockerfile                        # Containerización
│   ├── 📄 docker-compose.yml               # Orquestación local
│   ├── 📄 kubernetes_deployment.yaml       # Despliegue K8s
│   └── 📁 terraform/                        # Infraestructura como código
│
├── 📁 monitoring/                           # Monitoreo y alertas
│   ├── 📄 model_drift_detection.py         # Detección de drift
│   ├── 📄 performance_monitoring.py        # Monitoreo de performance
│   └── 📄 alert_system.py                  # Sistema de alertas
│
├── 📁 docs/                                 # Documentación adicional
│   ├── 📄 api_documentation.md             # Documentación de API
│   ├── 📄 user_guide.md                    # Guía de usuario
│   ├── 📄 troubleshooting.md               # Solución de problemas
│   └── 📁 images/                           # Imágenes para documentación
│
└── 📁 logs/                                 # Logs de ejecución
    ├── 📄 pipeline_execution_*.log          # Logs del pipeline
    ├── 📄 model_training_*.log              # Logs de entrenamiento
    └── 📄 error_*.log                       # Logs de errores
```

## 📄 Archivos Principales

### Código Fuente

- **`src/ecommerce_ml_analysis.py`**: Clase principal que orquesta todo el análisis
- **`data/generate_sample_data.py`**: Generador de datos sintéticos realistas
- **`scripts/run_pipeline.py`**: Script principal para ejecutar el pipeline completo
- **`notebooks/ecommerce_prediction_analysis.ipynb`**: Análisis interactivo paso a paso

### Configuración

- **`requirements.txt`**: Todas las dependencias necesarias
- **`config/spark_config.json`**: Configuración optimizada de Spark
- **`config/model_config.json`**: Hiperparámetros y configuración de modelos

### Documentación

- **`README.md`**: Documentación principal del proyecto
- **`reports/model_performance_report.md`**: Reporte detallado de resultados
- **`docs/api_documentation.md`**: Documentación de la API del modelo

## 🚀 Comandos Principales

### Instalación y Setup
```bash
# Clonar repositorio
git clone https://github.com/tu-usuario/mllib-ecommerce-analysis.git
cd mllib-ecommerce-analysis

# Instalar dependencias
pip install -r requirements.txt

# Configurar Spark (opcional, si no está instalado)
./scripts/setup_spark.sh
```

### Ejecución del Análisis
```bash
# Pipeline completo (recomendado)
python scripts/run_pipeline.py

# Generar solo datos
python scripts/run_pipeline.py --generate-data --skip-analysis

# Usar datos existentes
python scripts/run_pipeline.py --data-file path/to/your/data.csv

# Análisis interactivo
jupyter notebook notebooks/ecommerce_prediction_analysis.ipynb
```

### Entrenamiento de Modelos
```bash
# Entrenar modelos específicos
python scripts/train_models.py --model logistic_regression
python scripts/train_models.py --model random_forest
python scripts/train_models.py --model all

# Evaluación de modelos
python scripts/evaluate_models.py --model-path models/trained_models/
```

### Testing y Validación
```bash
# Ejecutar tests
pytest tests/

# Tests específicos
pytest tests/test_model_training.py -v

# Coverage report
pytest --cov=src tests/
```

## 📊 Archivos de Configuración

### `config/spark_config.json`
```json
{
  "spark.app.name": "EcommerceMLAnalysis",
  "spark.master": "local[*]",
  "spark.sql.adaptive.enabled": "true",
  "spark.sql.adaptive.coalescePartitions.enabled": "true",
  "spark.sql.adaptive.skewJoin.enabled": "true",
  "spark.sql.execution.arrow.pyspark.enabled": "true",
  "spark.serializer": "org.apache.spark.serializer.KryoSerializer",
  "spark.sql.execution.arrow.maxRecordsPerBatch": "10000"
}
```

### `config/model_config.json`
```json
{
  "logistic_regression": {
    "maxIter": [50, 100, 200],
    "regParam": [0.001, 0.01, 0.1],
    "elasticNetParam": [0.0, 0.5, 1.0]
  },
  "random_forest": {
    "numTrees": [50, 100, 150],
    "maxDepth": [5, 10, 15],
    "minInstancesPerNode": [1, 5, 10]
  },
  "cross_validation": {
    "numFolds": 3,
    "seed": 42
  },
  "evaluation_metrics": [
    "areaUnderROC",
    "areaUnderPR",
    "accuracy",
    "f1",
    "precision",
    "recall"
  ]
}
```

## 🔧 Scripts de Utilidad

### `scripts/setup_spark.sh`
```bash
#!/bin/bash
# Script para instalar y configurar Spark localmente

SPARK_VERSION="3.4.0"
HADOOP_VERSION="3"

echo "🔧 Instalando Apache Spark ${SPARK_VERSION}..."

# Descargar Spark
wget https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz

# Extraer
tar -xzf spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz

# Configurar variables de entorno
export SPARK_HOME=./spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}
export PATH=$PATH:$SPARK_HOME/bin

echo "✅ Spark instalado exitosamente"
echo "🚀 Para usar: export SPARK_HOME=$PWD/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}"
```

### `scripts/monitor_model.py`
```python
#!/usr/bin/env python3
"""Script de monitoreo continuo del modelo en producción"""

import time
import json
import logging
from datetime import datetime
from src.model_evaluation import ModelMonitor

def main():
    monitor = ModelMonitor()
    
    while True:
        try:
            # Verificar performance
            metrics = monitor.check_model_performance()
            
            # Detectar drift
            drift_detected = monitor.detect_data_drift()
            
            # Generar alertas si es necesario
            if drift_detected or metrics['auc'] < 0.75:
                monitor.send_alert(metrics, drift_detected)
            
            # Log estado
            logging.info(f"Model health check: AUC={metrics['auc']:.4f}, Drift={drift_detected}")
            
            # Esperar 1 hora
            time.sleep(3600)
            
        except Exception as e:
            logging.error(f"Error en monitoreo: {e}")
            time.sleep(300)  # Esperar 5 min en caso de error

if __name__ == "__main__":
    main()
```

## 📦 Deployment

### `deployment/Dockerfile`
```dockerfile
FROM python:3.9-slim

# Instalar Java (requerido para Spark)
RUN apt-get update && apt-get install -y openjdk-11-jre-headless && rm -rf /var/lib/apt/lists/*

# Configurar directorio de trabajo
WORKDIR /app

# Copiar requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY src/ src/
COPY config/ config/
COPY scripts/ scripts/

# Configurar variables de entorno
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PYTHONPATH=/app

# Comando por defecto
CMD ["python", "scripts/run_pipeline.py"]
```

### `deployment/docker-compose.yml`
```yaml
version: '3.8'

services:
  mllib-analysis:
    build: .
    container_name: ecommerce-ml-analysis
    volumes:
      - ./data:/app/data
      - ./models:/app/models
      - ./reports:/app/reports
      - ./logs:/app/logs
    environment:
      - SPARK_MASTER=local[*]
      - PYTHONPATH=/app
    ports:
      - "4040:4040"  # Spark UI
    restart: unless-stopped

  model-monitor:
    build: .
    container_name: model-monitor
    command: python scripts/monitor_model.py
    volumes:
      - ./models:/app/models
      - ./logs:/app/logs
    environment:
      - PYTHONPATH=/app
    restart: always
    depends_on:
      - mllib-analysis
```

## 🧪 Testing

### `tests/test_model_training.py`
```python
import unittest
import pandas as pd
from pyspark.sql import SparkSession
from src.ecommerce_ml_analysis import EcommerceMLAnalysis

class TestModelTraining(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.spark = SparkSession.builder.appName("TestMLAnalysis").getOrCreate()
        cls.analyzer = EcommerceMLAnalysis("TestAnalysis")
    
    def test_data_loading(self):
        """Test carga de datos"""
        # Crear datos de prueba
        test_data = pd.DataFrame({
            'customer_id': ['C001', 'C002'],
            'age': [25, 35],
            'will_purchase_next_7_days': [0, 1]
        })
        
        test_data.to_csv('test_data.csv', index=False)
        df = self.analyzer.load_data('test_data.csv')
        
        self.assertEqual(df.count(), 2)
        self.assertIn('customer_id', df.columns)
    
    def test_feature_engineering(self):
        """Test ingeniería de características"""
        # Implementar test de features
        pass
    
    def test_model_training(self):
        """Test entrenamiento de modelos"""
        # Implementar test de entrenamiento
        pass
    
    @classmethod
    def tearDownClass(cls):
        cls.spark.stop()

if __name__ == '__main__':
    unittest.main()
```

## 📈 Monitoreo y Alertas

### Métricas Clave a Monitorear
- **Model Performance**: AUC, Precision, Recall
- **Data Drift**: Distribución de características
- **Prediction Drift**: Distribución de predicciones
- **System Health**: Latencia, throughput, errores

### Alertas Automáticas
- AUC < 0.75: Alerta crítica de degradación
- Data drift > threshold: Alerta de cambio en datos
- Latencia > 500ms: Alerta de performance
- Error rate > 5%: Alerta de estabilidad

## 🔄 CI/CD Pipeline

### `.github/workflows/ci.yml`
```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v3
      with:
        python-version: 3.9
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        pytest tests/ --cov=src
    
    - name: Run data validation
      run: |
        python data/data_validation.py
    
    - name: Build Docker image
      run: |
        docker build -t mllib-analysis .
```

## 📚 Recursos Adicionales

### Enlaces Útiles
- [Apache Spark MLlib Documentation](https://spark.apache.org/mllib/)
- [PySpark API Reference](https://spark.apache.org/docs/latest/api/python/)
- [Machine Learning Best Practices](https://ml-ops.org/)

### Próximos Pasos
1. **Implementar en producción** con monitoreo continuo
2. **Agregar más algoritmos** (XGBoost, Deep Learning)
3. **Optimizar pipeline** para datos en tiempo real
4. **Integrar con sistemas existentes** de la empresa

---

**Nota**: Esta estructura proporciona una base sólida y escalable para el proyecto de Machine Learning con MLlib. Todos los archivos están diseñados para ser funcionales y seguir las mejores prácticas de la industria.