# Análisis de Caso - Detección de Churn en Servicio de Streaming
# DataSolutions S.A.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, roc_curve
from sklearn.metrics import precision_score, recall_score, f1_score
import warnings
warnings.filterwarnings('ignore')

class ChurnPredictor:
    """
    Clase para implementar el pipeline completo de detección de churn
    """
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.model = None
        self.feature_importance = None
        self.label_encoders = {}
        
    def load_and_explore_data(self, data_path=None):
        """
        Fase 1-2: Carga y exploración inicial de datos
        """
        print("=== FASE 1-2: EXPLORACIÓN DE DATOS ===")
        
        # Simular datos de ejemplo para demostración
        np.random.seed(42)
        n_samples = 10000
        
        # Generar datos sintéticos representativos
        data = {
            'user_id': range(n_samples),
            'age': np.random.normal(35, 12, n_samples),
            'monthly_charges': np.random.normal(50, 15, n_samples),
            'total_charges': np.random.normal(1000, 500, n_samples),
            'tenure_months': np.random.exponential(12, n_samples),
            'sessions_per_week': np.random.poisson(5, n_samples),
            'avg_session_duration': np.random.exponential(45, n_samples),
            'device_type': np.random.choice(['Mobile', 'TV', 'Web', 'Tablet'], n_samples, p=[0.4, 0.3, 0.2, 0.1]),
            'subscription_type': np.random.choice(['Basic', 'Premium', 'Family'], n_samples, p=[0.5, 0.3, 0.2]),
            'payment_method': np.random.choice(['Credit Card', 'PayPal', 'Bank Transfer'], n_samples, p=[0.6, 0.25, 0.15]),
            'support_tickets': np.random.poisson(0.5, n_samples),
            'days_since_last_login': np.random.exponential(3, n_samples),
        }
        
        self.df = pd.DataFrame(data)
        
        # Crear variable objetivo con lógica realista
        churn_probability = (
            (self.df['days_since_last_login'] > 7) * 0.3 +
            (self.df['support_tickets'] > 2) * 0.25 +
            (self.df['monthly_charges'] > 70) * 0.2 +
            (self.df['sessions_per_week'] < 2) * 0.4 +
            np.random.random(n_samples) * 0.1
        )
        
        self.df['churn'] = (churn_probability > 0.3).astype(int)
        
        print(f"Dataset cargado: {self.df.shape}")
        print(f"Tasa de churn: {self.df['churn'].mean():.2%}")
        print("\nPrimeras filas:")
        print(self.df.head())
        
        return self.df
    
    def exploratory_data_analysis(self):
        """
        Análisis exploratorio detallado
        """
        print("\n=== ANÁLISIS EXPLORATORIO ===")
        
        # Estadísticas descriptivas
        print("Estadísticas descriptivas:")
        print(self.df.describe())
        
        # Análisis de correlación
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        correlation_matrix = self.df[numeric_cols].corr()
        
        plt.figure(figsize=(12, 8))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
        plt.title('Matriz de Correlación')
        plt.tight_layout()
        plt.show()
        
        # Distribución de churn por variables categóricas
        categorical_cols = ['device_type', 'subscription_type', 'payment_method']
        
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        for i, col in enumerate(categorical_cols):
            churn_rate = self.df.groupby(col)['churn'].mean()
            churn_rate.plot(kind='bar', ax=axes[i], color='skyblue')
            axes[i].set_title(f'Tasa de Churn por {col}')
            axes[i].set_ylabel('Tasa de Churn')
            axes[i].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.show()
        
        return correlation_matrix
    
    def data_preprocessing(self):
        """
        Fase 3: Preprocesamiento y feature engineering
        """
        print("\n=== FASE 3: PREPROCESAMIENTO ===")
        
        # Crear copia para trabajo
        df_processed = self.df.copy()
        
        # Feature Engineering
        print("Aplicando feature engineering...")
        
        # Variables derivadas
        df_processed['charges_per_month'] = df_processed['total_charges'] / (df_processed['tenure_months'] + 1)
        df_processed['usage_intensity'] = df_processed['sessions_per_week'] * df_processed['avg_session_duration']
        df_processed['is_heavy_user'] = (df_processed['sessions_per_week'] > df_processed['sessions_per_week'].median()).astype(int)
        df_processed['is_recent_user'] = (df_processed['tenure_months'] < 6).astype(int)
        df_processed['high_support_usage'] = (df_processed['support_tickets'] > 1).astype(int)
        
        # Tratamiento de variables categóricas
        categorical_cols = ['device_type', 'subscription_type', 'payment_method']
        
        for col in categorical_cols:
            le = LabelEncoder()
            df_processed[col + '_encoded'] = le.fit_transform(df_processed[col])
            self.label_encoders[col] = le
        
        # Crear variables dummy
        df_processed = pd.get_dummies(df_processed, columns=categorical_cols, prefix=categorical_cols)
        
        # Selección de features
        feature_cols = [col for col in df_processed.columns if col not in ['user_id', 'churn']]
        
        print(f"Features creadas: {len(feature_cols)}")
        print("Nuevas features:")
        new_features = [col for col in feature_cols if col not in self.df.columns]
        for feature in new_features[:10]:  # Mostrar solo las primeras 10
            print(f"  - {feature}")
        
        self.X = df_processed[feature_cols]
        self.y = df_processed['churn']
        
        return self.X, self.y
    
    def split_and_scale_data(self, test_size=0.2, random_state=42):
        """
        División y escalado de datos
        """
        print("\n=== DIVISIÓN Y ESCALADO DE DATOS ===")
        
        # División temporal simulada (en producción sería por fecha)
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, test_size=test_size, random_state=random_state, stratify=self.y
        )
        
        # Escalado de variables numéricas
        numeric_features = self.X.select_dtypes(include=[np.number]).columns
        
        self.X_train_scaled = self.X_train.copy()
        self.X_test_scaled = self.X_test.copy()
        
        self.X_train_scaled[numeric_features] = self.scaler.fit_transform(self.X_train[numeric_features])
        self.X_test_scaled[numeric_features] = self.scaler.transform(self.X_test[numeric_features])
        
        print(f"Conjunto de entrenamiento: {self.X_train_scaled.shape}")
        print(f"Conjunto de prueba: {self.X_test_scaled.shape}")
        print(f"Distribución de churn en entrenamiento: {self.y_train.mean():.2%}")
        print(f"Distribución de churn en prueba: {self.y_test.mean():.2%}")
        
        return self.X_train_scaled, self.X_test_scaled, self.y_train, self.y_test
    
    def train_models(self):
        """
        Fase 4: Entrenamiento de múltiples modelos
        """
        print("\n=== FASE 4: ENTRENAMIENTO DE MODELOS ===")
        
        # Diccionario de modelos a evaluar
        models = {
            'Logistic Regression': LogisticRegression(random_state=42, class_weight='balanced'),
            'Random Forest': RandomForestClassifier(random_state=42, class_weight='balanced', n_estimators=100)
        }
        
        self.model_results = {}
        
        # Entrenamiento y evaluación con validación cruzada
        for name, model in models.items():
            print(f"\nEntrenando {name}...")
            
            # Validación cruzada
            cv_scores = cross_val_score(model, self.X_train_scaled, self.y_train, 
                                      cv=5, scoring='f1', n_jobs=-1)
            
            # Entrenamiento final
            model.fit(self.X_train_scaled, self.y_train)
            
            # Predicciones
            y_pred = model.predict(self.X_test_scaled)
            y_pred_proba = model.predict_proba(self.X_test_scaled)[:, 1]
            
            # Métricas
            metrics = {
                'cv_f1_mean': cv_scores.mean(),
                'cv_f1_std': cv_scores.std(),
                'precision': precision_score(self.y_test, y_pred),
                'recall': recall_score(self.y_test, y_pred),
                'f1': f1_score(self.y_test, y_pred),
                'auc_roc': roc_auc_score(self.y_test, y_pred_proba)
            }
            
            self.model_results[name] = {
                'model': model,
                'predictions': y_pred,
                'probabilities': y_pred_proba,
                'metrics': metrics
            }
            
            print(f"Validación cruzada F1: {metrics['cv_f1_mean']:.3f} (+/- {metrics['cv_f1_std']*2:.3f})")
            print(f"Test F1: {metrics['f1']:.3f}")
            print(f"Test AUC-ROC: {metrics['auc_roc']:.3f}")
        
        # Seleccionar mejor modelo
        best_model_name = max(self.model_results.keys(), 
                             key=lambda x: self.model_results[x]['metrics']['f1'])
        
        self.model = self.model_results[best_model_name]['model']
        self.best_model_name = best_model_name
        
        print(f"\nMejor modelo seleccionado: {best_model_name}")
        
        return self.model_results
    
    def evaluate_model(self):
        """
        Fase 5: Evaluación detallada del modelo
        """
        print("\n=== FASE 5: EVALUACIÓN DEL MODELO ===")
        
        best_result = self.model_results[self.best_model_name]
        y_pred = best_result['predictions']
        y_pred_proba = best_result['probabilities']
        
        # Reporte de clasificación
        print("Reporte de Clasificación:")
        print(classification_report(self.y_test, y_pred))
        
        # Matriz de confusión
        cm = confusion_matrix(self.y_test, y_pred)
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                   xticklabels=['No Churn', 'Churn'], 
                   yticklabels=['No Churn', 'Churn'])
        plt.title('Matriz de Confusión')
        plt.ylabel('Valor Real')
        plt.xlabel('Predicción')
        plt.show()
        
        # Curva ROC
        fpr, tpr, _ = roc_curve(self.y_test, y_pred_proba)
        auc = roc_auc_score(self.y_test, y_pred_proba)
        
        plt.figure(figsize=(8, 6))
        plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {auc:.3f})')
        plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('Tasa de Falsos Positivos')
        plt.ylabel('Tasa de Verdaderos Positivos')
        plt.title('Curva ROC')
        plt.legend(loc="lower right")
        plt.grid(True)
        plt.show()
        
        # Feature importance (solo para Random Forest)
        if hasattr(self.model, 'feature_importances_'):
            feature_importance = pd.DataFrame({
                'feature': self.X.columns,
                'importance': self.model.feature_importances_
            }).sort_values('importance', ascending=False)
            
            plt.figure(figsize=(10, 8))
            top_features = feature_importance.head(15)
            sns.barplot(data=top_features, y='feature', x='importance', palette='viridis')
            plt.title('Top 15 - Importancia de Variables')
            plt.xlabel('Importancia')
            plt.tight_layout()
            plt.show()
            
            self.feature_importance = feature_importance
            
            print("\nTop 10 variables más importantes:")
            for i, (_, row) in enumerate(feature_importance.head(10).iterrows()):
                print(f"{i+1:2d}. {row['feature']:<25} {row['importance']:.4f}")
    
    def business_impact_analysis(self):
        """
        Análisis de impacto de negocio
        """
        print("\n=== ANÁLISIS DE IMPACTO DE NEGOCIO ===")
        
        # Suposiciones de negocio
        avg_customer_value = 50  # Valor mensual promedio del cliente
        retention_cost = 15     # Costo de campaña de retención
        churn_prediction_threshold = 0.5
        
        y_pred_proba = self.model_results[self.best_model_name]['probabilities']
        
        # Clasificar clientes por riesgo
        high_risk = y_pred_proba >= churn_prediction_threshold
        predicted_churners = np.sum(high_risk)
        
        # Calcular métricas de negocio
        true_positives = np.sum((self.y_test == 1) & (y_pred_proba >= churn_prediction_threshold))
        false_positives = np.sum((self.y_test == 0) & (y_pred_proba >= churn_prediction_threshold))
        
        # ROI Analysis
        revenue_saved = true_positives * avg_customer_value * 12  # Asumiendo retención por 1 año
        campaign_cost = predicted_churners * retention_cost
        net_benefit = revenue_saved - campaign_cost
        roi = (net_benefit / campaign_cost * 100) if campaign_cost > 0 else 0
        
        print(f"Clientes identificados como alto riesgo: {predicted_churners}")
        print(f"Verdaderos positivos (churners detectados): {true_positives}")
        print(f"Falsos positivos (falsa alarma): {false_positives}")
        print(f"\n--- ANÁLISIS FINANCIERO ---")
        print(f"Ingresos potencialmente salvados: ${revenue_saved:,.2f}")
        print(f"Costo de campaña de retención: ${campaign_cost:,.2f}")
        print(f"Beneficio neto: ${net_benefit:,.2f}")
        print(f"ROI: {roi:.1f}%")
        
        return {
            'predicted_churners': predicted_churners,
            'true_positives': true_positives,
            'false_positives': false_positives,
            'revenue_saved': revenue_saved,
            'campaign_cost': campaign_cost,
            'net_benefit': net_benefit,
            'roi': roi
        }
    
    def generate_recommendations(self):
        """
        Generar recomendaciones basadas en el análisis
        """
        print("\n=== RECOMENDACIONES ESTRATÉGICAS ===")
        
        recommendations = [
            "1. IMPLEMENTACIÓN INMEDIATA:",
            "   - Desplegar modelo en producción con umbral de 0.5",
            "   - Configurar pipeline automático de scoring semanal",
            "   - Integrar con sistema CRM para alertas automáticas",
            "",
            "2. ESTRATEGIA DE RETENCIÓN:",
            "   - Enfocar campañas en clientes con probabilidad > 70%",
            "   - Personalizar ofertas basadas en variables importantes",
            "   - Monitorear clientes con alta actividad de soporte",
            "",
            "3. MEJORAS FUTURAS:",
            "   - Incorporar datos de comportamiento en tiempo real",
            "   - Implementar modelos de series temporales para patrones estacionales",
            "   - Desarrollar sistema de feedback para calibrar predicciones",
            "",
            "4. MONITOREO CONTINUO:",
            "   - Revisar performance del modelo mensualmente",
            "   - Alertas automáticas por degradación de métricas",
            "   - Reentrenamiento trimestral con datos frescos"
        ]
        
        for rec in recommendations:
            print(rec)
    
    def run_complete_pipeline(self):
        """
        Ejecutar pipeline completo
        """
        print("🚀 INICIANDO PIPELINE COMPLETO DE DETECCIÓN DE CHURN")
        print("=" * 60)
        
        # Ejecutar todas las fases
        self.load_and_explore_data()
        self.exploratory_data_analysis()
        self.data_preprocessing()
        self.split_and_scale_data()
        self.train_models()
        self.evaluate_model()
        business_metrics = self.business_impact_analysis()
        self.generate_recommendations()
        
        print("\n" + "=" * 60)
        print("✅ PIPELINE COMPLETADO EXITOSAMENTE")
        
        return business_metrics

# Ejemplo de uso
if __name__ == "__main__":
    # Instanciar y ejecutar el pipeline completo
    churn_predictor = ChurnPredictor()
    results = churn_predictor.run_complete_pipeline()
    
    print(f"\n📊 RESUMEN EJECUTIVO:")
    print(f"ROI proyectado: {results['roi']:.1f}%")
    print(f"Beneficio neto estimado: ${results['net_benefit']:,.2f}")
    print(f"Clientes de alto riesgo identificados: {results['predicted_churners']}")

# Código adicional para los otros problemas (Predicción de Ventas y Segmentación)

class SalesPredictor:
    """
    Implementación para Problema A: Predicción de Ventas
    """
    
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
    
    def prepare_sales_features(self, df):
        """
        Feature engineering específico para ventas
        """
        # Features temporales
        df['week_of_year'] = df['date'].dt.week
        df['month'] = df['date'].dt.month
        df['is_holiday_week'] = df['week_of_year'].isin([1, 25, 52]).astype(int)
        
        # Features de tendencia
        df['sales_lag_1'] = df.groupby('store_id')['sales'].shift(1)
        df['sales_lag_4'] = df.groupby('store_id')['sales'].shift(4)
        df['sales_rolling_mean'] = df.groupby('store_id')['sales'].rolling(4).mean().reset_index(0, drop=True)
        
        # Features externos
        df['competitor_distance'] = np.random.normal(5, 2, len(df))  # Simulado
        df['promotion_intensity'] = np.random.poisson(2, len(df))    # Simulado
        
        return df

class CustomerSegmentation:
    """
    Implementación para Problema C: Segmentación de Clientes
    """
    
    def __init__(self, n_clusters=5):
        self.n_clusters = n_clusters
        self.kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        self.scaler = StandardScaler()
        self.pca = PCA(n_components=2)
    
    def prepare_clustering_features(self, df):
        """
        Feature engineering para clustering
        """
        features = df.groupby('customer_id').agg({
            'transaction_amount': ['mean', 'std', 'sum', 'count'],
            'days_between_transactions': ['mean', 'std'],
            'product_category': lambda x: len(x.unique())
        }).reset_index()
        
        # Aplanar nombres de columnas
        features.columns = ['_'.join(col).strip() for col in features.columns.values]
        
        return features
    
    def find_optimal_clusters(self, X):
        """
        Método del codo para encontrar número óptimo de clusters
        """
        inertias = []
        K_range = range(2, 11)
        
        for k in K_range:
            kmeans = KMeans(n_clusters=k, random_state=42)
            kmeans.fit(X)
            inertias.append(kmeans.inertia_)
        
        plt.figure(figsize=(10, 6))
        plt.plot(K_range, inertias, 'bo-')
        plt.xlabel('Número de Clusters')
        plt.ylabel('Inercia')
        plt.title('Método del Codo para Determinar K Óptimo')
        plt.grid(True)
        plt.show()
        
        return inertias