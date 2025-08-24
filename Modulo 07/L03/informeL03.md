# Análisis de Caso  
## Procesamiento distribuido de datos con Apache Spark  


### 📍 Situación inicial  
La empresa **DataStream Analytics S.A.** ofrece servicios de análisis de datos para el sector financiero.  
Actualmente, necesitan **generar reportes diarios** sobre los movimientos financieros de millones de registros provenientes de sucursales distribuidas en todo el país.  

El sistema local utilizado hasta ahora no escala ni responde a la velocidad requerida. Por eso, el equipo de tecnología decidió migrar a una solución de **procesamiento distribuido con Apache Spark**.  


### 🔎 Descripción del caso  
Como Ingeniero/a de Datos, el desafío consiste en diseñar una solución con Spark que permita:  

- Procesar archivos de gran volumen.  
- Detectar patrones sospechosos para prevenir fraudes.  
- Asegurar **escalabilidad** y **tolerancia a fallos**.  


### 1. Creación del RDD  

```python
from pyspark import SparkContext

sc = SparkContext("local[*]", "AnalisisFinanciero")
rdd = sc.textFile("hdfs://ruta/datos_movimientos/*.csv")


textFile() carga datos de manera distribuida desde HDFS/S3.

Cada línea se convierte en un registro dentro del RDD.

El trabajo se reparte automáticamente entre los nodos del cluster.

2. Transformaciones propuestas

Filtrado de registros inválidos o incompletos

rdd_filtrado = rdd.filter(lambda linea: len(linea.split(",")) == 6)


Mapeo y estructuración de datos

rdd_mapeado = rdd_filtrado.map(lambda linea: linea.split(","))


Agregación por usuario (ejemplo: sumar montos)

rdd_agrupado = rdd_mapeado.map(lambda x: (x[0], float(x[2]))).reduceByKey(lambda a, b: a + b)

3. Acciones propuestas

take() o collect() → Obtener una muestra para validación.

muestra = rdd_agrupado.take(10)


saveAsTextFile() → Exportar resultados procesados.

rdd_agrupado.saveAsTextFile("hdfs://ruta/resultados/reportes_diarios")

4. Definición de un Job Spark

Un Job Spark es la unidad de ejecución que comienza cuando se llama a una acción.
En este caso, un Job corresponde al flujo:

Leer archivos distribuidos.

Aplicar transformaciones (filtrado, mapeo, agregación).

Ejecutar la acción final para guardar los reportes diarios.

5. Reflexión

✅ Importancia del procesamiento distribuido:

Procesar millones de registros rápidamente.

Escalar horizontalmente agregando nodos.

Tolerancia a fallos con reintentos automáticos.

Procesamiento en memoria → mucho más rápido que sistemas locales.

⚠️ Desafíos técnicos:

Configuración del cluster y recursos (memoria, cores, particiones).

Balanceo de carga entre nodos.

Limpieza y consistencia de los datos.

Costos de infraestructura si no se optimiza.

📊 Esquema visual del flujo con Spark
   [Sucursales: Archivos CSV grandes]
                   │
                   ▼
          Ingesta en HDFS / S3
                   │
                   ▼
       SparkContext → RDD inicial
                   │
        ┌──────────┴──────────┐
        ▼                     ▼
   [Transformación 1]   Filtrado de registros
   [Transformación 2]   Mapeo y estructuración
   [Transformación 3]   Agregación por usuario
                   │
                   ▼
             Acciones (Jobs)
        ┌──────────┴──────────┐
        ▼                     ▼
   `collect()` (validación)   `saveAsTextFile()` (reportes diarios)



