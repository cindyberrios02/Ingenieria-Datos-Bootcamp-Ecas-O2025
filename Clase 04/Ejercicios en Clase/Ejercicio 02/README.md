👥 DIRECTORIO DE EMPLEADOS
========================================
Directorio creado con los siguientes empleados:
  emp1: Ana, 28 años
  emp2: Luis, 35 años
  emp3: Carmen, 42 años
  ...

🔍 Paso 2: Recorriendo empleados con for y .items()
  📋 ID: emp1
      Nombre: Ana
      Edad: 28 años
      Generación: Joven
      🔹 30 años o menor

🎯 Paso 3: Filtrando empleados mayores de 30 años
  Ana (28 años) → ❌ EXCLUIDO (30 años o menor)
  Luis (35 años) → ✅ INCLUIDO (Mayor de 30)
  ...

📊 Paso 4: Resultados del análisis
EMPLEADOS MAYORES DE 30 AÑOS:
📋 Lista: ['Luis', 'Carmen', 'Sofía', 'Roberto', 'Carlos']
📈 Cantidad: 5

📊 ESTADÍSTICAS GENERALES:
👥 Total de empleados: 8
📈 Mayores de 30: 5 (62.5%)
📉 30 años o menor: 3 (37.5%)

Para ejecutar

# Ejecutar el programa completo
python directorio_empleados.py

# O ejecutar solo la función principal
python -c "from directorio_empleados import crear_directorio_empleados; crear_directorio_empleados()"