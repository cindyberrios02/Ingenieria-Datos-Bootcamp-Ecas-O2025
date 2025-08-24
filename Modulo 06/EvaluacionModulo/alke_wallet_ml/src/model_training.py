import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import cross_val_score, validation_curve, learning_curve
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_auc_score, roc_curve,
    mean_absolute_error, mean_squared_error, r2_score
)
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
import joblib
import warnings
warnings.filterwarnings('ignore')

class ModelTrainer:
    """
    Clase para entrenamiento y evaluación de modelos de machine learning
    """
    
    def __init__(self):
        self.models = {}
        self.best_model = None
        self.results = {}
        
    def get_classification_models(self):
        """
        Definir modelos de clasificación a entrenar
        """
        models = {
            'Logistic_Regression': LogisticRegression(random_state=42, max_iter=1000),
            'Random_Forest': RandomForestClassifier(n_estimators=100, random_state=42),
            'KNN': KNeighborsClassifier(n_neighbors=5),
            'Decision_Tree': DecisionTreeClassifier(random_state=42, max_depth=10),
            'SVM': SVC(random_state=42, probability=True)
        }
        return models
    
    def get_regression_models(self):
        """
        Definir modelos de regresión a entrenar
        """
        models = {
            'Ridge_Regression': Ridge(random_state=42),
            'Random_Forest_Reg': RandomForestRegressor(n_estimators=100, random_state=42)
        }
        return models
    
    def train_classification_models(self, X_train, y_train, X_val, y_val):
        """
        Entrenar modelos de clasificación
        """
        models = self.get_classification_models()
        results = {}
        
        print("=== ENTRENANDO MODELOS DE CLASIFICACIÓN ===")
        
        for name, model in models.items():
            print(f"\nEntrenando {name}...")
            
            # Entrenar modelo
            model.fit(X_train, y_train)
            
            # Predicciones
            y_train_pred = model.predict(X_train)
            y_val_pred = model.predict(X_val)
            y_val_proba = model.predict_proba(X_val)[:, 1] if hasattr(model, 'predict_proba') else None
            
            # Métricas de entrenamiento
            train_metrics = {
                'accuracy': accuracy_score(y_train, y_train_pred),
                'precision': precision_score(y_train, y_train_pred),
                'recall': recall_score(y_train, y_train_pred),
                'f1': f1_score(y_train, y_train_pred)
            }
            
            # Métricas de validación
            val_metrics = {
                'accuracy': accuracy_score(y_val, y_val_pred),
                'precision': precision_score(y_val, y_val_pred),
                'recall': recall_score(y_val, y_val_pred),
                'f1': f1_score(y_val, y_val_pred),
                'auc_roc': roc_auc_score(y_val, y_val_proba) if y_val_proba is not None else None
            }
            
            # Validación cruzada
            cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='f1')
            
            results[name] = {
                'model': model,
                'train_metrics': train_metrics,
                'val_metrics': val_metrics,
                'cv_mean': cv_scores.mean(),
                'cv_std': cv_scores.std(),
                'y_val_pred': y_val_pred,
                'y_val_proba': y_val_proba
            }
            
            print(f"F1-Score Validación: {val_metrics['f1']:.4f}")
            print(f"AUC-ROC: {val_metrics['auc_roc']:.4f}" if val_metrics['auc_roc'] else "AUC-ROC: N/A")
            print(f"CV F1-Score: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
        
        self.results.update(results)
        return results
    
    def evaluate_model_performance(self, results, y_val):
        """
        Evaluar y comparar el rendimiento de los modelos
        """
        print("\n=== COMPARACIÓN DE MODELOS ===")
        
        # Crear DataFrame de comparación
        comparison_data = []
        for name, result in results.items():
            comparison_data.append({
                'Model': name,
                'Accuracy': result['val_metrics']['accuracy'],
                'Precision': result['val_metrics']['precision'],
                'Recall': result['val_metrics']['recall'],
                'F1_Score': result['val_metrics']['f1'],
                'AUC_ROC': result['val_metrics']['auc_roc'] or 0,
                'CV_F1_Mean': result['cv_mean']
            })
        
        comparison_df = pd.DataFrame(comparison_data).sort_values('F1_Score', ascending=False)
        print(comparison_df.round(4))
        
        # Seleccionar mejor modelo
        best_model_name = comparison_df.iloc[0]['Model']
        self.best_model = results[best_model_name]['model']
        
        print(f"\n🏆 Mejor modelo: {best_model_name}")
        
        return comparison_df, best_model_name
    
    def plot_model_comparison(self, comparison_df):
        """
        Visualizar comparación de modelos
        """
        fig, axes = plt.subpl