# Informe Técnico: Preprocesamiento y Escalamiento de Datos
**RetailData Analytics - Proyecto Modelo Predictivo de Clientes Recurrentes**


## 1. Descripción de Etapas Aplicadas

### **Imputación de Valores Faltantes**
Se aplicó la técnica de imputación por media para el valor faltante en la columna "Ingresos(USD)". El cliente ID=3 tenía un valor nulo que se reemplazó por $40,000 (media de los valores existentes: $30,000, $50,000, $40,000).

### **Codificación de Variables Categóricas**
Se implementaron tres métodos para la variable "Ciudad":

- **Label Encoding**: Asignó valores numéricos ordinales (Barcelona=0, Madrid=1, Sevilla=2)
- **One-Hot Encoding**: Creó 3 columnas binarias independientes para cada ciudad
- **Variables Dummy**: Similar al One-Hot pero eliminando una categoría de referencia para evitar multicolinealidad

### **Escalamiento de Variables Numéricas**
Se aplicaron dos técnicas de escalamiento a las variables "Edad" e "Ingresos":

- **Normalización Min-Max**: Transformó los valores al rango [0,1] preservando la distribución relativa
- **Estandarización Z-Score**: Centró los datos en media=0 con desviación estándar=1


## 2. Respuestas a Preguntas de Reflexión

### **¿Por qué es importante realizar estas tareas antes de entrenar un modelo de Machine Learning?**

El preprocesamiento es fundamental por las siguientes razones:

1. **Calidad de datos**: Los valores faltantes pueden causar errores o sesgos en el modelo
2. **Compatibilidad algorítmica**: Los algoritmos de ML requieren datos numéricos y no pueden procesar directamente variables categóricas
3. **Convergencia del modelo**: Las diferencias de escala pueden hacer que el algoritmo converja lentamente o se enfoque en variables con mayor magnitud
4. **Rendimiento predictivo**: Datos bien preparados mejoran significativamente la precisión y estabilidad del modelo

### **¿Qué diferencias observaste entre la normalización y la estandarización?**

**Normalización Min-Max:**
- Transforma datos al rango [0,1]
- Preserva la distribución original
- Sensible a valores atípicos
- Ideal cuando conocemos los límites teóricos de las variables

**Estandarización Z-Score:**
- Centra los datos en media=0 con desviación estándar=1
- No limita a un rango específico
- Más robusta ante valores atípicos
- Mejor para algoritmos que asumen distribución normal

**Recomendación**: Para este caso de clientes recurrentes, se sugiere Z-Score ya que las variables (edad, ingresos) pueden tener valores atípicos y queremos que el modelo trate ambas variables con igual importancia.



## 3. Resultados del Análisis

### **Dataset Original vs Transformado**
- **Registros procesados**: 4 clientes
- **Variables originales**: 4 (ID, Edad, Ciudad, Ingresos)
- **Variables finales**: 12 (incluyendo todas las transformaciones)
- **Valores faltantes**: 1 imputado exitosamente

### **Validación de Transformaciones**
✅ Imputación: Media de ingresos = $40,000
✅ Label Encoding: 3 ciudades mapeadas correctamente  
✅ Escalamiento: Rangos y distribuciones verificados
✅ Archivos generados: CSV y Excel con datos transformados



## 4. Recomendaciones para Modelado

1. **Usar estandarización Z-Score** para las variables numéricas en el modelo final
2. **Aplicar One-Hot Encoding** para variables categóricas si hay más de 2 categorías
3. **Monitorear la imputación** cuando se incorporen más datos
4. **Validar transformaciones** en datos de prueba antes del despliegue

