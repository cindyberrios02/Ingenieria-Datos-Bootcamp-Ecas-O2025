"""
Análisis Principal de Machine Learning con MLlib
Implementación completa de predicción de compras para e-commerce
"""

from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import *
from pyspark.ml.feature import VectorAssembler, StandardScaler, StringIndexer
from pyspark.ml.classification import LogisticRegression, RandomForestClassifier
from pyspark.ml.evaluation import BinaryClassificationEvaluator, MulticlassClassificationEvaluator
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder
from pyspark.ml import Pipeline
from pyspark.ml.stat import Correlation
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

class EcommerceMLAnalysis:
    """
    Clase principal para el análisis de Machine Learning escalable
    con MLlib para predicción de compras en e-commerce
    """
    
    def __init__(self, app_name="EcommerceMLAnalysis"):
        """Inicializar Spark Session"""
        self.spark = SparkSession.builder \
            .appName(app_name) \
            .config("spark.sql.adaptive.enabled", "true") \
            .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
            .getOrCreate()
        
        self.spark.sparkContext.setLogLevel("WARN")
        print(f"✅ Spark Session iniciada: {app_name}")
        print(f"🔧 Versión de Spark: {self.spark.version}")
    
    def load_data(self, file_path):
        """
        Cargar datos desde archivo CSV
        
        Args:
            file_path: Ruta del archivo CSV
            
        Returns:
            DataFrame de Spark
        """
        print(f"📊 Cargando datos desde: {file_path}")
        
        # Schema explícito para mejor rendimiento
        schema = StructType([
            StructField("customer_id", StringType(), True),
            StructField("age", IntegerType(), True),
            StructField("gender", StringType(), True),
            StructField("city", StringType(), True),
            StructField("device_type", StringType(), True),
            StructField("days_since_registration", IntegerType(), True),
            StructField("sessions_per_week", IntegerType(), True),
            StructField("avg_session_duration_minutes", DoubleType(), True),
            StructField("pages_per_session", IntegerType(), True),
            StructField("total_orders", IntegerType(), True),
            StructField("avg_order_value", DoubleType(), True),
            StructField("days_since_last_order", IntegerType(), True),
            StructField("products_viewed", IntegerType(), True),
            StructField("products_in_cart", IntegerType(), True),
            StructField("avg_rating_given", DoubleType(), True),
            StructField("reviews_written", IntegerType(), True),
            StructField("email_opens_per_week", IntegerType(), True),
            StructField("email_clicks_per_week", IntegerType(), True),
            StructField("newsletter_subscriber", IntegerType(), True),
            StructField("recent_sessions", IntegerType(), True),
            StructField("recent_page_views", IntegerType(), True),
            StructField("recent_time_on_site_minutes", DoubleType(), True),
            StructField("abandoned_carts", IntegerType(), True),
            StructField("will_purchase_next_7_days", IntegerType(), True)
        ])
        
        df = self.spark.read.csv(file_path, header=True, schema=schema)
        
        print(f"✅ Datos cargados exitosamente")
        print(f"📏 Dimensiones: {df.count():,} filas x {len(df.columns)} columnas")
        
        return df
    
    def explore_data(self, df):
        """
        Análisis exploratorio de datos
        
        Args:
            df: DataFrame de Spark
        """
        print("\n" + "="*50)
        print("📊 ANÁLISIS EXPLORATORIO DE DATOS")
        print("="*50)
        
        # Información básica
        print("\n🔍 Información del Dataset:")
        df.printSchema()
        
        # Estadísticas descriptivas
        print("\n📈 Estadísticas Descriptivas:")
        numeric_cols = [f.name for f in df.schema.fields if f.dataType in [IntegerType(), DoubleType()]]
        df.select(numeric_cols).describe().show()
        
        # Distribución de la variable objetivo
        print("\n🎯 Distribución de Variable Objetivo:")
        target_dist = df.groupBy("will_purchase_next_7_days").count().collect()
        for row in target_dist:
            pct = (row['count'] / df.count()) * 100
            print(f"  Clase {row['will_purchase_next_7_days']}: {row['count']:,} ({pct:.1f}%)")
        
        # Valores faltantes
        print("\n❓ Análisis de Valores Faltantes:")
        for col in df.columns:
            null_count = df.filter(col(col).isNull()).count()
            if null_count > 0:
                print(f"  {col}: {null_count:,} valores faltantes")
            else:
                print(f"  {col}: Sin valores faltantes")
    
    def preprocess_data(self, df):
        """
        Preprocesamiento y ingeniería de características
        
        Args:
            df: DataFrame de Spark
            
        Returns:
            DataFrame preprocesado
        """
        print("\n" + "="*50)
        print("🔧 PREPROCESAMIENTO DE DATOS")
        print("="*50)
        
        # Feature engineering
        df_processed = df.withColumn(
            "has_purchase_history", 
            when(col("total_orders") > 0, 1).otherwise(0)
        ).withColumn(
            "engagement_score",
            (col("sessions_per_week") * col("avg_session_duration_minutes")) / 60
        ).withColumn(
            "cart_conversion_rate",
            when(col("products_viewed") > 0, 
                 col("products_in_cart") / col("products_viewed")).otherwise(0)
        ).withColumn(
            "email_engagement",
            when(col("email_opens_per_week") > 0,
                 col("email_clicks_per_week") / col("email_opens_per_week")).otherwise(0)
        ).withColumn(
            "days_since_last_order_filled",
            when(col("days_since_last_order") == -1, 999).otherwise(col("days_since_last_order"))
        )
        
        # Codificación de variables categóricas
        gender_indexer = StringIndexer(inputCol="gender", outputCol="gender_indexed")
        city_indexer = StringIndexer(inputCol="city", outputCol="city_indexed") 
        device_indexer = StringIndexer(inputCol="device_type", outputCol="device_indexed")
        
        df_processed = gender_indexer.fit(df_processed).transform(df_processed)
        df_processed = city_indexer.fit(df_processed).transform(df_processed)
        df_processed = device_indexer.fit(df_processed).transform(df_processed)
        
        print("✅ Features creadas:")
        print("  - has_purchase_history")
        print("  - engagement_score") 
        print("  - cart_conversion_rate")
        print("  - email_engagement")
        print("  - Variables categóricas codificadas")
        
        return df_processed
    
    def prepare_features(self, df):
        """
        Preparar vector de características para MLlib
        
        Args:
            df: DataFrame preprocesado
            
        Returns:
            DataFrame con vector de características
        """
        print("\n🎯 Preparando vector de características...")
        
        # Seleccionar características numéricas
        feature_cols = [
            'age', 'days_since_registration', 'sessions_per_week',
            'avg_session_duration_minutes', 'pages_per_session', 'total_orders',
            'avg_order_value', 'days_since_last_order_filled', 'products_viewed',
            'products_in_cart', 'avg_rating_given', 'reviews_written',
            'email_opens_per_week', 'email_clicks_per_week', 'newsletter_subscriber',
            'recent_sessions', 'recent_page_views', 'recent_time_on_site_minutes',
            'abandoned_carts', 'gender_indexed', 'city_indexed', 'device_indexed',
            'has_purchase_history', 'engagement_score', 'cart_conversion_rate',
            'email_engagement'
        ]
        
        # Crear vector assembler
        assembler = VectorAssembler(
            inputCols=feature_cols,
            outputCol="features_raw"
        )
        
        # Escalar características
        scaler = StandardScaler(
            inputCol="features_raw",
            outputCol="features",
            withStd=True,
            withMean=True
        )
        
        # Pipeline de preparación
        prep_pipeline = Pipeline(stages=[assembler, scaler])
        prep_model = prep_pipeline.fit(df)
        df_features = prep_model.transform(df)
        
        print(f"✅ Vector de características creado con {len(feature_cols)} features")
        
        return df_features, feature_cols
    
    def split_data(self, df, train_ratio=0.8, random_seed=42):
        """
        Dividir datos en entrenamiento y prueba
        
        Args:
            df: DataFrame con características
            train_ratio: Proporción para entrenamiento
            random_seed: Semilla aleatoria
            
        Returns:
            Tuple (train_df, test_df)
        """
        print(f"\n📊 Dividiendo datos: {train_ratio:.0%} entrenamiento, {1-train_ratio:.0%} prueba")
        
        train_df, test_df = df.randomSplit([train_ratio, 1-train_ratio], seed=random_seed)
        
        print(f"  Entrenamiento: {train_df.count():,} registros")
        print(f"  Prueba: {test_df.count():,} registros")
        
        return train_df, test_df
    
    def train_models(self, train_df):
        """
        Entrenar múltiples modelos de clasificación
        
        Args:
            train_df: DataFrame de entrenamiento
            
        Returns:
            Diccionario con modelos entrenados
        """
        print("\n" + "="*50)
        print("🤖 ENTRENAMIENTO DE MODELOS")
        print("="*50)
        
        models = {}
        
        # 1. Regresión Logística
        print("\n📈 Entrenando Regresión Logística...")
        lr = LogisticRegression(
            featuresCol="features",
            labelCol="will_purchase_next_7_days",
            maxIter=100,
            regParam=0.01
        )
        
        # Grid search para hyperparameter tuning
        lr_param_grid = ParamGridBuilder() \
            .addGrid(lr.regParam, [0.001, 0.01, 0.1]) \
            .addGrid(lr.elasticNetParam, [0.0, 0.5, 1.0]) \
            .build()
        
        lr_evaluator = BinaryClassificationEvaluator(
            labelCol="will_purchase_next_7_days",
            metricName="areaUnderROC"
        )
        
        lr_cv = CrossValidator(
            estimator=lr,
            estimatorParamMaps=lr_param_grid,
            evaluator=lr_evaluator,
            numFolds=3,
            seed=42
        )
        
        lr_model = lr_cv.fit(train_df)
        models['logistic_regression'] = lr_model
        print("✅ Regresión Logística entrenada")
        
        # 2. Random Forest
        print("\n🌲 Entrenando Random Forest...")
        rf = RandomForestClassifier(
            featuresCol="features",
            labelCol="will_purchase_next_7_days",
            numTrees=50,
            seed=42
        )
        
        rf_param_grid = ParamGridBuilder() \
            .addGrid(rf.numTrees, [20, 50, 100]) \
            .addGrid(rf.maxDepth, [5, 10, 15]) \
            .build()
        
        rf_cv = CrossValidator(
            estimator=rf,
            estimatorParamMaps=rf_param_grid,
            evaluator=lr_evaluator,
            numFolds=3,
            seed=42
        )
        
        rf_model = rf_cv.fit(train_df)
        models['random_forest'] = rf_model
        print("✅ Random Forest entrenado")
        
        return models
    
    def evaluate_models(self, models, test_df):
        """
        Evaluar rendimiento de los modelos
        
        Args:
            models: Diccionario con modelos entrenados
            test_df: DataFrame de prueba
            
        Returns:
            Diccionario con métricas
        """
        print("\n" + "="*50)
        print("📊 EVALUACIÓN DE MODELOS")
        print("="*50)
        
        results = {}
        
        # Evaluadores
        binary_evaluator = BinaryClassificationEvaluator(
            labelCol="will_purchase_next_7_days"
        )
        
        multi_evaluator = MulticlassClassificationEvaluator(
            labelCol="will_purchase_next_7_days"
        )
        
        for model_name, model in models.items():
            print(f"\n🔍 Evaluando {model_name.replace('_', ' ').title()}:")
            
            # Predicciones
            predictions = model.transform(test_df)
            
            # Métricas
            auc = binary_evaluator.evaluate(predictions, {binary_evaluator.metricName: "areaUnderROC"})
            precision = multi_evaluator.evaluate(predictions, {multi_evaluator.metricName: "precisionByLabel"})
            recall = multi_evaluator.evaluate(predictions, {multi_evaluator.metricName: "recallByLabel"})
            f1 = multi_evaluator.evaluate(predictions, {multi_evaluator.metricName: "f1"})
            accuracy = multi_evaluator.evaluate(predictions, {multi_evaluator.metricName: "accuracy"})
            
            results[model_name] = {
                'auc': auc,
                'precision': precision,
                'recall': recall,
                'f1': f1,
                'accuracy': accuracy,
                'predictions': predictions
            }
            
            print(f"  📈 AUC-ROC: {auc:.4f}")
            print(f"  🎯 Precisión: {precision:.4f}")
            print(f"  🔍 Recall: {recall:.4f}")
            print(f"  ⚖️  F1-Score: {f1:.4f}")
            print(f"  ✅ Accuracy: {accuracy:.4f}")
        
        return results
    
    def generate_insights(self, models, feature_cols):
        """
        Generar insights y feature importance
        
        Args:
            models: Modelos entrenados
            feature_cols: Lista de nombres de características
        """
        print("\n" + "="*50)
        print("💡 INSIGHTS Y FEATURE IMPORTANCE")
        print("="*50)
        
        # Feature importance de Random Forest
        if 'random_forest' in models:
            rf_model = models['random_forest'].bestModel
            feature_importance = rf_model.featureImportances.toArray()
            
            importance_df = pd.DataFrame({
                'feature': feature_cols,
                'importance': feature_importance
            }).sort_values('importance', ascending=False)
            
            print("\n🌟 Top 10 Features más Importantes (Random Forest):")
            for i, row in importance_df.head(10).iterrows():
                print(f"  {row['feature']}: {row['importance']:.4f}")
    
    def save_model(self, model, model_name, path="models/"):
        """
        Guardar modelo entrenado
        
        Args:
            model: Modelo entrenado
            model_name: Nombre del modelo
            path: Ruta de guardado
        """
        model_path = f"{path}{model_name}"
        model.write().overwrite().save(model_path)
        print(f"💾 Modelo guardado en: {model_path}")
    
    def generate_report(self, results, feature_cols):
        """
        Generar reporte final con resultados
        
        Args:
            results: Resultados de evaluación
            feature_cols: Características utilizadas
        """
        print("\n" + "="*60)
        print("📋 REPORTE FINAL DE RESULTADOS")
        print("="*60)
        
        # Comparación de modelos
        print("\n📊 Comparación de Modelos:")
        print("-" * 50)
        print(f"{'Modelo':<20} {'AUC-ROC':<10} {'Precisión':<10} {'F1-Score':<10}")
        print("-" * 50)
        
        for model_name, metrics in results.items():
            name_display = model_name.replace('_', ' ').title()
            print(f"{name_display:<20} {metrics['auc']:<10.4f} {metrics['precision']:<10.4f} {metrics['f1']:<10.4f}")
        
        # Mejor modelo
        best_model = max(results.keys(), key=lambda x: results[x]['auc'])
        print(f"\n🏆 Mejor Modelo: {best_model.replace('_', ' ').title()}")
        print(f"   AUC-ROC: {results[best_model]['auc']:.4f}")
        
        print(f"\n📈 Total de características utilizadas: {len(feature_cols)}")
        print(f"🎯 Problema: Clasificación binaria (compra/no compra)")
        print(f"⚡ Framework: Apache Spark MLlib")
    
    def run_complete_analysis(self, data_path):
        """
        Ejecutar análisis completo end-to-end
        
        Args:
            data_path: Ruta de los datos
        """
        print("🚀 INICIANDO ANÁLISIS COMPLETO DE ML CON MLLIB")
        print("="*60)
        
        try:
            # 1. Cargar datos
            df = self.load_data(data_path)
            
            # 2. Análisis exploratorio
            self.explore_data(df)
            
            # 3. Preprocesamiento
            df_processed = self.preprocess_data(df)
            
            # 4. Preparar características
            df_features, feature_cols = self.prepare_features(df_processed)
            
            # 5. Dividir datos
            train_df, test_df = self.split_data(df_features)
            
            # 6. Entrenar modelos
            models = self.train_models(train_df)
            
            # 7. Evaluar modelos
            results = self.evaluate_models(models, test_df)
            
            # 8. Generar insights
            self.generate_insights(models, feature_cols)
            
            # 9. Guardar mejor modelo
            best_model_name = max(results.keys(), key=lambda x: results[x]['auc'])
            self.save_model(models[best_model_name], best_model_name)
            
            # 10. Reporte final
            self.generate_report(results, feature_cols)
            
            print("\n✅ ANÁLISIS COMPLETADO EXITOSAMENTE")
            
            return results, models
            
        except Exception as e:
            print(f"❌ Error durante el análisis: {str(e)}")
            raise
        
        finally:
            self.spark.stop()
            print("🔌 Spark Session cerrada")

def main():
    """Función principal para ejecutar el análisis"""
    
    # Configuración
    DATA_PATH = "sample_ecommerce_data.csv"
    
    # Crear instancia del analizador
    analyzer = EcommerceMLAnalysis("EcommercePredictionAnalysis")
    
    # Ejecutar análisis completo
    results, models = analyzer.run_complete_analysis(DATA_PATH)
    
    return results, models

if __name__ == "__main__":
    main()