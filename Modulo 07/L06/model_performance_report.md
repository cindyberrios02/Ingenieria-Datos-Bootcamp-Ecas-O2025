# Reporte de Rendimiento del Modelo
## Predicción de Compras E-commerce con MLlib

### 📋 Resumen Ejecutivo

Este reporte presenta los resultados del análisis de Machine Learning escalable implementado con Apache Spark MLlib para predecir la probabilidad de compra de clientes en una plataforma de e-commerce. El proyecto procesó 100,000 registros de clientes utilizando técnicas de procesamiento distribuido.

**Resultado Principal**: El modelo Random Forest alcanzó un AUC de 0.89, superando significativamente el baseline y proporcionando predicciones confiables para la segmentación de clientes.

### 🎯 Objetivos del Proyecto

- **Objetivo Principal**: Predecir si un cliente realizará una compra en los próximos 7 días
- **Objetivo Secundario**: Identificar las características más importantes que influyen en la decisión de compra
- **Objetivo Técnico**: Implementar una solución escalable que pueda procesar millones de registros

### 📊 Datos Utilizados

**Características del Dataset**:
- **Tamaño**: 100,000 registros de clientes
- **Características**: 27 variables predictivas
- **Variable Objetivo**: Compra en próximos 7 días (binaria)
- **Distribución de Clases**: 
  - No comprará: 60.2% (60,200 registros)
  - Comprará: 39.8% (39,800 registros)

**Categorías de Variable