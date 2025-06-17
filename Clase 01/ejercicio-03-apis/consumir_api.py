import requests
import json
from datetime import datetime
import time

def consumir_api_publica():
    """Consume una API pública para obtener datos."""
    print("🌐 CONSUMIENDO API PÚBLICA")
    print("=" * 30)
    
    try:
        # API de ejemplo: JSONPlaceholder (datos de prueba)
        url = "https://jsonplaceholder.typicode.com/posts"
        
        print(f"📡 Haciendo petición a: {url}")
        response = requests.get(url)
        
        # Verificar status code
        if response.status_code == 200:
            print(f"✅ Petición exitosa (Status: {response.status_code})")
            datos = response.json()
            
            print(f"📊 Se obtuvieron {len(datos)} registros")
            
            # Mostrar algunos ejemplos
            print(f"\n📝 Primeros 3 posts:")
            for post in datos[:3]:
                print(f"  ID: {post['id']} | Título: {post['title'][:50]}...")
            
            return datos
        else:
            print(f"❌ Error en la petición: {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")
        return None

def procesar_datos_api(datos):
    """Procesa los datos obtenidos de la API."""
    if not datos:
        return
    
    print(f"\n🔧 PROCESANDO DATOS DE LA API")
    print("=" * 35)
    
    # Análisis básico
    total_posts = len(datos)
    usuarios_unicos = len(set(post['userId'] for post in datos))
    
    print(f"📊 Estadísticas generales:")
    print(f"  Total de posts: {total_posts}")
    print(f"  Usuarios únicos: {usuarios_unicos}")
    print(f"  Posts por usuario: {total_posts / usuarios_unicos:.1f}")
    
    # Análisis por usuario
    posts_por_usuario = {}
    for post in datos:
        user_id = post['userId']
        if user_id not in posts_por_usuario:
            posts_por_usuario[user_id] = 0
        posts_por_usuario[user_id] += 1
    
    # Usuario más activo
    usuario_mas_activo = max(posts_por_usuario, key=posts_por_usuario.get)
    posts_max = posts_por_usuario[usuario_mas_activo]
    
    print(f"\n👤 Usuario más activo: Usuario {usuario_mas_activo} ({posts_max} posts)")
    
    # Longitud promedio de títulos
    longitudes = [len(post['title']) for post in datos]
    longitud_promedio = sum(longitudes) / len(longitudes)
    
    print(f"📏 Longitud promedio de títulos: {longitud_promedio:.1f} caracteres")
    
    return posts_por_usuario

def simular_api_tiempo_real():
    """Simula el consumo de una API en tiempo real."""
    print(f"\n⏰ SIMULACIÓN DE API EN TIEMPO REAL")
    print("=" * 40)
    
    # Simular datos de sensores IoT
    sensores = ["Sensor_Temp_01", "Sensor_Hum_01", "Sensor_Pres_01"]
    datos_tiempo_real = []
    
    print(f"🔄 Recolectando datos cada 2 segundos (5 iteraciones)...")
    
    for i in range(5):
        timestamp = datetime.now()
        
        for sensor in sensores:
            if "Temp" in sensor:
                valor = round(20 + (i * 2) + (i * 0.5), 1)  # Simulando temperatura
                unidad = "°C"
            elif "Hum" in sensor:
                valor = round(45 + (i * 3) - (i * 0.2), 1)  # Simulando humedad
                unidad = "%"
            else:
                valor = round(1013 + (i * 1) + (i * 0.1), 1)  # Simulando presión
                unidad = "hPa"
            
            lectura = {
                "sensor": sensor,
                "timestamp": timestamp.isoformat(),
                "valor": valor,
                "unidad": unidad
            }
            
            datos_tiempo_real.append(lectura)
            print(f"  📊 {sensor}: {valor} {unidad} [{timestamp.strftime('%H:%M:%S')}]")
        
        print(f"  ⏱️ Iteración {i+1}/5 completada")
        time.sleep(2)  # Esperar 2 segundos
    
    print(f"\n✅ Recolección completada: {len(datos_tiempo_real)} lecturas")
    return datos_tiempo_real

def guardar_datos_json(datos, nombre_archivo):
    """Guarda los datos en formato JSON."""
    print(f"\n💾 GUARDANDO DATOS EN JSON")
    print("=" * 30)
    
    try:
        with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
            json.dump(datos, archivo, indent=2, ensure_ascii=False)
        
        print(f"✅ Datos guardados en: {nombre_archivo}")
        print(f"📁 Tamaño del archivo: {len(json.dumps(datos, indent=2))} bytes")
        
    except Exception as e:
        print(f"❌ Error al guardar: {e}")

def main():
    """Función principal."""
    print("🔌 BOOTCAMP INGENIERÍA DE DATOS - APIs")
    print("=" * 45)
    
    # Consumir API pública
    datos_api = consumir_api_publica()
    
    if datos_api:
        # Procesar datos
        stats_usuarios = procesar_datos_api(datos_api)
        
        # Guardar resultados
        guardar_datos_json(datos_api, "posts_api.json")
    
    # Simular API en tiempo real
    datos_sensores = simular_api_tiempo_real()
    guardar_datos_json(datos_sensores, "sensores_tiempo_real.json")
    
    print(f"\n✅ ¡Ejercicio de APIs completado!")
    print(f"📚 Has aprendido: requests, JSON, APIs REST, datos en tiempo real")

if __name__ == "__main__":
    main()