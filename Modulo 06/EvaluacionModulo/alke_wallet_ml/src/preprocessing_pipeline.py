import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib
import warnings
warnings.filterwarnings('ignore')

class DataPreprocessor:
    """
    Clase para el preprocesamiento completo de datos de evaluación crediticia
    """
    
    def __init__(self):
        self.preprocessor = None
        self.feature_names = None
        self.target_encoder = None
        
    def create_preprocessing_pipeline(self, df):
        """
        Crea el pipeline de preprocesamiento
        """
        # Identificar tipos de columnas
        numeric_features = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
        if 'approved' in numeric_features:
            numeric_features.remove('approved')
            
        categorical_features = df.select_dtypes(include=['object']).columns.tolist()
        
        print(f"Variables numéricas: {numeric_features}")
        print(f"Variables categóricas: {categorical_features}")
        
        # Pipeline para variables numéricas
        numeric_transformer = Pipeline(steps=[
            ('imputer', KNNImputer(n_neighbors=5)),  # Imputación con KNN
            ('scaler', StandardScaler())  # Escalamiento estándar
        ])
        
        # Pipeline para variables categóricas
        categorical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='most_frequent')),  # Imputación con moda
            ('onehot', OneHotEncoder(drop='first', handle_unknown='ignore'))  # One-hot encoding
        ])
        
        # Combinar transformadores
        self.preprocessor = ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, numeric_features),
                ('cat', categorical_transformer, categorical_features)
            ]
        )
        
        return self.preprocessor
    
    def fit_transform(self, X, y=None):
        """
        Ajustar y transformar los datos
        """
        if self.preprocessor is None:
            raise ValueError("Debe crear el pipeline primero con create_preprocessing_pipeline()")
        
        # Ajustar y transformar
        X_transformed = self.preprocessor.fit_transform(X)
        
        # Obtener nombres de características para interpretabilidad
        self._get_feature_names(X)
        
        return X_transformed
    
    def transform(self, X):
        """
        Transformar nuevos datos usando el pipeline ajustado
        """
        if self.preprocessor is None:
            raise ValueError("Debe ajustar el pipeline primero")
        
        return self.preprocessor.transform(X)
    
    def _get_feature_names(self, X):
        """
        Obtener nombres de las características después de la transformación
        """
        feature_names = []
        
        # Obtener nombres de transformadores
        for name, transformer, features in self.preprocessor.transformers_:
            if name == 'num':
                feature_names.extend(features)
            elif name == 'cat':
                if hasattr(transformer.named_steps['onehot'], 'get_feature_names_out'):
                    cat_names = transformer.named_steps['onehot'].get_feature_names_out(features)
                    feature_names.extend(cat_names)
                else:
                    # Fallback para versiones más antiguas
                    feature_names.extend([f"{feature}_{cat}" for feature in features 
                                        for cat in transformer.named_steps['onehot'].categories_[0][1:]])
        
        self.feature_names = feature_names
        return feature_names
    
    def get_feature_importance_df(self, model, top_n=15):
        """
        Crear DataFrame con importancia de características
        """
        if self.feature_names is None:
            raise ValueError("Nombres de características no disponibles")
        
        if hasattr(model, 'feature_importances_'):
            importances = model.feature_importances_
        elif hasattr(model, 'coef_'):
            importances = np.abs(model.coef_).flatten()
        else:
            raise ValueError("El modelo no tiene importancias de características disponibles")
        
        importance_df = pd.DataFrame({
            'feature': self.feature_names[:len(importances)],
            'importance': importances
        }).sort_values('importance', ascending=False).head(top_n)
        
        return importance_df
    
    def save_preprocessor(self, filepath='models/preprocessor.joblib'):
        """
        Guardar el preprocessor
        """
        joblib.dump(self.preprocessor, filepath)
        print(f"Preprocessor guardado en: {filepath}")
    
    def load_preprocessor(self, filepath='models/preprocessor.joblib'):
        """
        Cargar preprocessor guardado
        """
        self.preprocessor = joblib.load(filepath)
        print(f"Preprocessor cargado desde: {filepath}")

def prepare_data_for_modeling(df, test_size=0.2, val_size=0.1, random_state=42):
    """
    Preparar datos para modelado con conjuntos de entrenamiento, validación y prueba
    """
    # Separar características y variable objetivo
    X = df.drop('approved', axis=1)
    y = df['approved']
    
    # División inicial: entrenamiento + validación vs. prueba
    X_temp, X_test, y_temp, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    
    # División secundaria: entrenamiento vs. validación
    val_size_adjusted = val_size / (1 - test_size)  # Ajustar tamaño de validación
    X_train, X_val, y_train, y_val = train_test_split(
        X_temp, y_temp, test_size=val_size_adjusted, random_state=random_state, stratify=y_temp
    )
    
    print("=== DISTRIBUCIÓN DE CONJUNTOS ===")
    print(f"Entrenamiento: {X_train.shape[0]} muestras ({X_train.shape[0]/len(df)*100:.1f}%)")
    print(f"Validación: {X_val.shape[0]} muestras ({X_val.shape[0]/len(df)*100:.1f}%)")
    print(f"Prueba: {X_test.shape[0]} muestras ({X_test.shape[0]/len(df)*100:.1f}%)")
    
    # Verificar balanceo de clases
    print("\n=== DISTRIBUCIÓN DE CLASES ===")
    print("Entrenamiento:")
    print(y_train.value_counts(normalize=True))
    print("Validación:")
    print(y_val.value_counts(normalize=True))
    print("Prueba:")
    print(y_test.value_counts(normalize=True))
    
    return X_train, X_val, X_test, y_train, y_val, y_test

def apply_preprocessing_pipeline(X_train, X_val, X_test, create_new=True):
    """
    Aplicar pipeline de preprocesamiento a todos los conjuntos
    """
    preprocessor = DataPreprocessor()
    
    if create_new:
        # Crear y ajustar pipeline con datos de entrenamiento
        preprocessor.create_preprocessing_pipeline(pd.concat([X_train, pd.DataFrame({'approved': [0]})]))
        X_train_processed = preprocessor.fit_transform(X_train)
    else:
        # Cargar pipeline existente
        preprocessor.load_preprocessor()
        X_train_processed = preprocessor.transform(X_train)
    
    # Transformar conjuntos de validación y prueba
    X_val_processed = preprocessor.transform(X_val)
    X_test_processed = preprocessor.transform(X_test)
    
    print(f"\n=== RESULTADO DEL PREPROCESAMIENTO ===")
    print(f"Forma después del preprocesamiento:")
    print(f"- Entrenamiento: {X_train_processed.shape}")
    print(f"- Validación: {X_val_processed.shape}")
    print(f"- Prueba: {X_test_processed.shape}")
    
    return X_train_processed, X_val_processed, X_test_processed, preprocessor

# Función principal para ejecutar todo el pipeline
def main_preprocessing_pipeline():
    """
    Pipeline principal de preprocesamiento
    """
    # Cargar datos
    print("Cargando dataset...")
    df = pd.read_csv('credit_data.csv')
    
    # Análisis inicial de datos faltantes
    print("\n=== ANÁLISIS DE DATOS FALTANTES ===")
    missing_data = df.isnull().sum()
    missing_percentage = (missing_data / len(df)) * 100
    missing_df = pd.DataFrame({
        'Column': missing_data.index,
        'Missing_Count': missing_data.values,
        'Missing_Percentage': missing_percentage.values
    })
    print(missing_df[missing_df.Missing_Count > 0])
    
    # Preparar datos
    X_train, X_val, X_test, y_train, y_val, y_test = prepare_data_for_modeling(df)
    
    # Aplicar preprocesamiento
    X_train_processed, X_val_processed, X_test_processed, preprocessor = apply_preprocessing_pipeline(
        X_train, X_val, X_test
    )
    
    # Guardar preprocessor
    preprocessor.save_preprocessor()
    
    # Guardar conjuntos procesados
    datasets = {
        'X_train': X_train_processed,
        'X_val': X_val_processed,
        'X_test': X_test_processed,
        'y_train': y_train.values,
        'y_val': y_val.values,
        'y_test': y_test.values
    }
    
    joblib.dump(datasets, 'models/processed_datasets.joblib')
    print("\nConjuntos de datos procesados guardados en: models/processed_datasets.joblib")
    
    return datasets, preprocessor

if __name__ == "__main__":
    datasets, preprocessor = main_preprocessing_pipeline()