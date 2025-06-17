import json
import os
from collections import Counter, defaultdict
from datetime import datetime

def cargar_datos_json(nombre_archivo):
    """Carga datos desde un archivo JSON."""
    print(f"📂 CARGANDO DATOS JSON")
    print("=" * 25)
    
    try:
        if os.path.exists(nombre_archivo):
            with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
                datos = json.load(archivo)
            
            print(f"✅ Archivo cargado: {nombre_archivo}")
            print(f"📊 Registros encontrados: {len(datos) if isinstance(datos, list) else 1}")
            return datos
        else:
            print(f"❌ Archivo no encontrado: {nombre_archivo}")
            return None
            
    except json.JSONDecodeError as e:
        print(f"❌ Error al parsear JSON: {e}")
        return None
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return None

def procesar_posts_api(datos_posts):
    """Procesa datos de posts obtenidos de API."""
    if not datos_posts:
        return
    
    print(f"\n📝 PROCESANDO POSTS DE API")
    print("=" * 30)
    
    # Análisis de contenido
    palabras_comunes = Counter()
    longitudes_titulo = []
    longitudes_body = []
    
    for post in datos_posts:
        # Análisis de títulos
        titulo = post.get('title', '').lower()
        palabras_titulo = titulo.split()
        palabras_comunes.update(palabras_titulo)
        longitudes_titulo.append(len(titulo))
        
        # Análisis de contenido
        body = post.get('body', '')
        longitudes_body.append(len(body))
    
    # Estadísticas
    print(f"📊 Estadísticas de contenido:")
    print(f"  Longitud promedio título: {sum(longitudes_titulo)/len(longitudes_titulo):.1f} caracteres")
    print(f"  Longitud promedio body: {sum(longitudes_body)/len(longitudes_body):.1f} caracteres")
    
    # Palabras más comunes en títulos
    print(f"\n🏷️ Top 5 palabras en títulos:")
    for palabra, frecuencia in palabras_comunes.most_common(5):
        print(f"  {palabra}: {frecuencia} veces")
    
    # Análisis por usuario
    posts_por_usuario = defaultdict(list)
    for post in datos_posts:
        user_id = post.get('userId')
        posts_por_usuario[user_id].append(post)
    
    print(f"\n👥 Análisis por usuario:")
    for user_id, posts in sorted(posts_por_usuario.items())[:5]:
        promedio_titulo = sum(len(p.get('title', '')) for p in posts) / len(posts)
        print(f"  Usuario {user_id}: {len(posts)} posts, título promedio: {promedio_titulo:.1f} chars")

def procesar_sensores_tiempo_real(datos_sensores):
    """Procesa datos de sensores IoT."""
    if not datos_sensores:
        return
    
    print(f"\n🌡️ PROCESANDO DATOS DE SENSORES")
    print("=" * 35)
    
    # Agrupar por tipo de sensor
    sensores_por_tipo = defaultdict(list)
    for lectura in datos_sensores:
        sensor = lectura.get('sensor', '')
        if 'Temp' in sensor:
            tipo = 'Temperatura'
        elif 'Hum' in sensor:
            tipo = 'Humedad'
        elif 'Pres' in sensor:
            tipo = 'Presión'
        else:
            tipo = 'Otro'
        
        sensores_por_tipo[tipo].append(lectura)
    
    # Análisis por tipo de sensor
    for tipo, lecturas in sensores_por_tipo.items():
        valores = [l.get('valor', 0) for l in lecturas]
        
        if valores:
            promedio = sum(valores) / len(valores)
            maximo = max(valores)
            minimo = min(valores)
            unidad = lecturas[0].get('unidad', '')
            
            print(f"\n📊 {tipo}:")
            print(f"  Lecturas: {len(lecturas)}")
            print(f"  Promedio: {promedio:.2f} {unidad}")
            print(f"  Máximo: {maximo} {unidad}")
            print(f"  Mínimo: {minimo} {unidad}")
            
            # Tendencia simple
            if len(valores) >= 2:
                tendencia = "↗️ Creciente" if valores[-1] > valores[0] else "↘️ Decreciente"
                print(f"  Tendencia: {tendencia}")

def crear_json_complejo():
    """Crea un archivo JSON con estructura compleja."""
    print(f"\n🏗️ CREANDO JSON COMPLEJO")
    print("=" * 30)
    
    # Estructura compleja simulando una empresa de datos
    empresa_datos = {
        "empresa": {
            "nombre": "DataTech Solutions",
            "fundacion": "2020-01-15",
            "ubicacion": {
                "pais": "Chile",
                "ciudad": "Santiago",
                "direccion": "Av. Providencia 123"
            }
        },
        "departamentos": [
            {
                "nombre": "Data Engineering",
                "jefe": "Ana García",
                "empleados": [
                    {
                        "id": 1,
                        "nombre": "Carlos Ruiz",
                        "cargo": "Senior Data Engineer",
                        "salario": 95000,
                        "skills": ["Python", "SQL", "Apache Spark", "AWS"],
                        "proyectos_activos": 3
                    },
                    {
                        "id": 2,
                        "nombre": "María López",
                        "cargo": "Data Engineer",
                        "salario": 75000,
                        "skills": ["Python", "PostgreSQL", "Docker"],
                        "proyectos_activos": 2
                    }
                ]
            },
            {
                "nombre": "Data Science",
                "jefe": "Pedro Martín",
                "empleados": [
                    {
                        "id": 3,
                        "nombre": "Lucía Torres",
                        "cargo": "Senior Data Scientist",
                        "salario": 105000,
                        "skills": ["Python", "R", "Machine Learning", "TensorFlow"],
                        "proyectos_activos": 2
                    }
                ]
            }
        ],
        "proyectos": [
            {
                "id": "PROJ-001",
                "nombre": "Sistema de Recomendaciones",
                "estado": "En desarrollo",
                "presupuesto": 150000,
                "fecha_inicio": "2024-01-01",
                "fecha_estimada_fin": "2024-06-30",
                "equipo": [1, 3],
                "tecnologias": ["Python", "TensorFlow", "Redis", "PostgreSQL"]
            },
            {
                "id": "PROJ-002",
                "nombre": "Pipeline de Datos en Tiempo Real",
                "estado": "Planificación",
                "presupuesto": 200000,
                "fecha_inicio": "2024-03-01",
                "fecha_estimada_fin": "2024-12-31",
                "equipo": [1, 2],
                "tecnologias": ["Apache Kafka", "Spark Streaming", "AWS Kinesis"]
            }
        ],
        "metricas": {
            "empleados_total": 4,
            "proyectos_activos": 2,
            "ingresos_anuales": 2500000,
            "clientes": 15,
            "satisfaccion_cliente": 4.7
        }
    }
    
    # Guardar el JSON
    with open('empresa_datos_complejo.json', 'w', encoding='utf-8') as archivo:
        json.dump(empresa_datos, archivo, indent=2, ensure_ascii=False)
    
    print(f"✅ JSON complejo creado: empresa_datos_complejo.json")
    return empresa_datos

def analizar_json_complejo(datos_empresa):
    """Analiza el JSON complejo de la empresa."""
    print(f"\n🔍 ANÁLISIS DE EMPRESA")
    print("=" * 25)
    
    # Información general
    empresa = datos_empresa['empresa']
    print(f"🏢 Empresa: {empresa['nombre']}")
    print(f"📍 Ubicación: {empresa['ubicacion']['ciudad']}, {empresa['ubicacion']['pais']}")
    
    # Análisis de empleados
    todos_empleados = []
    for dept in datos_empresa['departamentos']:
        todos_empleados.extend(dept['empleados'])
    
    if todos_empleados:
        salarios = [emp['salario'] for emp in todos_empleados]
        salario_promedio = sum(salarios) / len(salarios)
        salario_max = max(salarios)
        salario_min = min(salarios)
        
        print(f"\n💰 Análisis salarial:")
        print(f"  Empleados: {len(todos_empleados)}")
        print(f"  Salario promedio: ${salario_promedio:,.2f}")
        print(f"  Salario máximo: ${salario_max:,}")
        print(f"  Salario mínimo: ${salario_min:,}")
    
    # Skills más comunes
    todas_skills = []
    for emp in todos_empleados:
        todas_skills.extend(emp.get('skills', []))
    
    skills_counter = Counter(todas_skills)
    print(f"\n🎯 Top 5 skills:")
    for skill, count in skills_counter.most_common(5):
        print(f"  {skill}: {count} empleados")
    
    # Análisis de proyectos
    proyectos = datos_empresa.get('proyectos', [])
    if proyectos:
        presupuesto_total = sum(p.get('presupuesto', 0) for p in proyectos)
        print(f"\n🚀 Proyectos:")
        print(f"  Total proyectos: {len(proyectos)}")
        print(f"  Presupuesto total: ${presupuesto_total:,}")
        
        for proyecto in proyectos:
            print(f"  - {proyecto['nombre']}: {proyecto['estado']}")

def transformar_y_filtrar():
    """Demuestra transformaciones y filtros complejos."""
    print(f"\n🔄 TRANSFORMACIONES Y FILTROS")
    print("=" * 35)
    
    # Datos de ejemplo: logs de servidor
    logs_servidor = [
        {"timestamp": "2024-06-12 10:30:15", "level": "INFO", "message": "Usuario conectado", "user_id": 123},
        {"timestamp": "2024-06-12 10:31:22", "level": "ERROR", "message": "Conexión fallida", "user_id": 456},
        {"timestamp": "2024-06-12 10:32:10", "level": "INFO", "message": "Consulta ejecutada", "user_id": 123},
        {"timestamp": "2024-06-12 10:33:45", "level": "WARNING", "message": "Memoria baja", "user_id": None},
        {"timestamp": "2024-06-12 10:34:12", "level": "ERROR", "message": "Base de datos no disponible", "user_id": 789}
    ]
    
    # Filtrar solo errores
    errores = [log for log in logs_servidor if log['level'] == 'ERROR']
    print(f"❌ Errores encontrados: {len(errores)}")
    for error in errores:
        print(f"  {error['timestamp']}: {error['message']}")
    
    # Contar logs por nivel
    niveles = Counter(log['level'] for log in logs_servidor)
    print(f"\n📊 Logs por nivel:")
    for nivel, count in niveles.items():
        print(f"  {nivel}: {count}")
    
    # Usuarios únicos (excluyendo None)
    usuarios_unicos = set(log['user_id'] for log in logs_servidor if log['user_id'] is not None)
    print(f"\n👥 Usuarios únicos: {len(usuarios_unicos)}")
    print(f"  IDs: {sorted(list(usuarios_unicos))}")
    
    # Guardar logs filtrados
    with open('logs_errores.json', 'w', encoding='utf-8') as archivo:
        json.dump(errores, archivo, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Errores guardados en: logs_errores.json")

def main():
    """Función principal."""
    print("📄 BOOTCAMP INGENIERÍA DE DATOS - PROCESAMIENTO JSON")
    print("=" * 55)
    
    # Intentar cargar datos existentes
    posts = cargar_datos_json('posts_api.json')
    if posts:
        procesar_posts_api(posts)
    
    sensores = cargar_datos_json('sensores_tiempo_real.json')
    if sensores:
        procesar_sensores_tiempo_real(sensores)
    
    # Crear y analizar JSON complejo
    empresa = crear_json_complejo()
    analizar_json_complejo(empresa)
    
    # Demostraciones adicionales
    transformar_y_filtrar()
    
    print(f"\n✅ ¡Procesamiento JSON completado!")
    print(f"📚 Has aprendido: JSON complejo, filtros, transformaciones, análisis")

if __name__ == "__main__":
    main()