import json
import requests
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import os

class AnalizadorDatos:
    """Clase principal para análisis de datos del bootcamp."""
    
    def __init__(self):
        self.datos_ventas = []
        self.datos_usuarios = []
        self.configuracion = self.cargar_configuracion()
    
    def cargar_configuracion(self):
        """Carga configuración del proyecto."""
        config_default = {
            "nombre_proyecto": "Análisis Integral de Datos",
            "version": "1.0.0",
            "autor": "Estudiante Bootcamp",
            "fecha_creacion": datetime.now().isoformat(),
            "archivos_salida": {
                "reporte_general": "reporte_general.json",
                "metricas": "metricas_clave.json",
                "log_proceso": "proceso.log"
            }
        }
        
        try:
            with open('config.json', 'r') as f:
                config = json.load(f)
                return {**config_default, **config}
        except FileNotFoundError:
            # Crear archivo de configuración
            with open('config.json', 'w') as f:
                json.dump(config_default, f, indent=2)
            return config_default
    
    def log_proceso(self, mensaje):
        """Registra eventos del proceso."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {mensaje}"
        print(log_entry)
        
        with open(self.configuracion["archivos_salida"]["log_proceso"], 'a') as f:
            f.write(log_entry + "\n")
    
    def generar_datos_ventas(self, num_registros=500):
        """Genera datos de ventas simulados."""
        self.log_proceso(f"Generando {num_registros} registros de ventas")
        
        import random
        random.seed(42)
        
        productos = [
            {"nombre": "Laptop Pro", "categoria": "Electrónicos", "precio_base": 1200},
            {"nombre": "Mouse Inalámbrico", "categoria": "Accesorios", "precio_base": 45},
            {"nombre": "Teclado Mecánico", "categoria": "Accesorios", "precio_base": 120},
            {"nombre": "Monitor 4K", "categoria": "Electrónicos", "precio_base": 400},
            {"nombre": "Webcam HD", "categoria": "Accesorios", "precio_base": 80},
            {"nombre": "Tablet Pro", "categoria": "Electrónicos", "precio_base": 600},
            {"nombre": "Auriculares", "categoria": "Audio", "precio_base": 150},
            {"nombre": "Smartphone", "categoria": "Móviles", "precio_base": 800}
        ]
        
        regiones = ["Norte", "Sur", "Este", "Oeste", "Centro"]
        canales = ["Online", "Tienda Física", "Teléfono", "App Móvil"]
        
        fecha_inicio = datetime(2024, 1, 1)
        
        for i in range(num_registros):
            producto = random.choice(productos)
            dias_transcurridos = random.randint(0, 165)  # Hasta junio
            fecha_venta = fecha_inicio + timedelta(days=dias_transcurridos)
            
            # Simular variaciones estacionales
            factor_estacional = 1.0
            if fecha_venta.month in [11, 12]:  # Black Friday, Navidad
                factor_estacional = 1.3
            elif fecha_venta.month in [1, 2]:  # Post-navidad
                factor_estacional = 0.8
            
            precio_final = producto["precio_base"] * factor_estacional
            precio_final *= random.uniform(0.9, 1.1)  # Variación aleatoria
            
            venta = {
                "id": f"VT-{i+1:04d}",
                "fecha": fecha_venta.isoformat()[:10],
                "producto": producto["nombre"],
                "categoria": producto["categoria"],
                "cantidad": random.randint(1, 5),
                "precio_unitario": round(precio_final, 2),
                "region": random.choice(regiones),
                "canal": random.choice(canales),
                "vendedor_id": f"VEND-{random.randint(1, 15):02d}",
                "cliente_tipo": random.choice(["Nuevo", "Recurrente", "VIP"])
            }
            
            venta["total"] = round(venta["cantidad"] * venta["precio_unitario"], 2)
            self.datos_ventas.append(venta)
        
        self.log_proceso(f"Datos de ventas generados exitosamente")
    
    def obtener_datos_externos(self):
        """Obtiene datos externos de APIs públicas."""
        self.log_proceso("Obteniendo datos externos de APIs")
        
        try:
            # API de usuarios de prueba
            response = requests.get("https://jsonplaceholder.typicode.com/users")
            if response.status_code == 200:
                usuarios_api = response.json()
                
                # Transformar datos para nuestro análisis
                for usuario in usuarios_api:
                    usuario_procesado = {
                        "id": usuario["id"],
                        "nombre": usuario["name"],
                        "email": usuario["email"],
                        "ciudad": usuario["address"]["city"],
                        "compania": usuario["company"]["name"],
                        "sitio_web": usuario["website"]
                    }
                    self.datos_usuarios.append(usuario_procesado)
                
                self.log_proceso(f"Obtenidos {len(usuarios_api)} usuarios de API externa")
            
        except requests.exceptions.RequestException as e:
            self.log_proceso(f"Error al obtener datos externos: {e}")
    
    def analizar_ventas_por_periodo(self):
        """Análisis temporal de ventas."""
        self.log_proceso("Iniciando análisis temporal de ventas")
        
        ventas_por_mes = defaultdict(lambda: {"total": 0, "cantidad": 0, "transacciones": 0})
        ventas_por_categoria = defaultdict(lambda: {"total": 0, "cantidad": 0})
        
        for venta in self.datos_ventas:
            mes = venta["fecha"][:7]  # YYYY-MM
            categoria = venta["categoria"]
            
            # Por mes
            ventas_por_mes[mes]["total"] += venta["total"]
            ventas_por_mes[mes]["cantidad"] += venta["cantidad"]
            ventas_por_mes[mes]["transacciones"] += 1
            
            # Por categoría
            ventas_por_categoria[categoria]["total"] += venta["total"]
            ventas_por_categoria[categoria]["cantidad"] += venta["cantidad"]
        
        # Resultados mensuales
        print(f"\n📅 ANÁLISIS TEMPORAL")
        print("=" * 25)
        for mes in sorted(ventas_por_mes.keys()):
            datos = ventas_por_mes[mes]
            promedio = datos["total"] / datos["transacciones"]
            print(f"{mes}: ${datos['total']:,.2f} ({datos['transacciones']} ventas, promedio: ${promedio:.2f})")
        
        # Resultados por categoría
        print(f"\n🏷️ ANÁLISIS POR CATEGORÍA")
        print("=" * 30)
        categorias_ordenadas = sorted(ventas_por_categoria.items(), 
                                    key=lambda x: x[1]["total"], reverse=True)
        
        for categoria, datos in categorias_ordenadas:
            print(f"{categoria}: ${datos['total']:,.2f} ({datos['cantidad']} unidades)")
        
        return ventas_por_mes, ventas_por_categoria
    
    def analizar_rendimiento_vendedores(self):
        """Análisis de rendimiento de vendedores."""
        self.log_proceso("Analizando rendimiento de vendedores")
        
        vendedores = defaultdict(lambda: {
            "ventas_total": 0,
            "transacciones": 0,
            "productos_vendidos": 0,
            "clientes_tipos": Counter()
        })
        
        for venta in self.datos_ventas:
            vendedor = venta["vendedor_id"]
            vendedores[vendedor]["ventas_total"] += venta["total"]
            vendedores[vendedor]["transacciones"] += 1
            vendedores[vendedor]["productos_vendidos"] += venta["cantidad"]
            vendedores[vendedor]["clientes_tipos"][venta["cliente_tipo"]] += 1
        
        print(f"\n👥 TOP 5 VENDEDORES")
        print("=" * 25)
        
        vendedores_ordenados = sorted(vendedores.items(), 
                                    key=lambda x: x[1]["ventas_total"], reverse=True)
        
        for i, (vendedor_id, datos) in enumerate(vendedores_ordenados[:5], 1):
            promedio = datos["ventas_total"] / datos["transacciones"]
            print(f"{i}. {vendedor_id}: ${datos['ventas_total']:,.2f}")
            print(f"   Transacciones: {datos['transacciones']} | Promedio: ${promedio:.2f}")
            
            # Cliente más frecuente
            cliente_top = datos["clientes_tipos"].most_common(1)[0]
            print(f"   Cliente más atendido: {cliente_top[0]} ({cliente_top[1]} veces)")
        
        return vendedores
    
    def detectar_patrones_anomalos(self):
        """Detecta patrones anómalos en las ventas."""
        self.log_proceso("Detectando patrones anómalos")
        
        # Calcular estadísticas para detectar anomalías
        totales_venta = [venta["total"] for venta in self.datos_ventas]
        promedio_global = sum(totales_venta) / len(totales_venta)
        
        # Desviación estándar simple
        varianza = sum((x - promedio_global) ** 2 for x in totales_venta) / len(totales_venta)
        desviacion = varianza ** 0.5
        
        # Umbral para anomalías (3 desviaciones estándar)
        umbral_alto = promedio_global + (3 * desviacion)
        umbral_bajo = promedio_global - (3 * desviacion)
        
        anomalias_altas = [v for v in self.datos_ventas if v["total"] > umbral_alto]
        anomalias_bajas = [v for v in self.datos_ventas if v["total"] < umbral_bajo and v["total"] > 0]
        
        print(f"\n⚠️ DETECCIÓN DE ANOMALÍAS")
        print("=" * 30)
        print(f"Promedio global: ${promedio_global:.2f}")
        print(f"Desviación estándar: ${desviacion:.2f}")
        print(f"Ventas excepcionalmente altas: {len(anomalias_altas)}")
        print(f"Ventas excepcionalmente bajas: {len(anomalias_bajas)}")
        
        if anomalias_altas:
            print(f"\n🔥 Top 3 ventas más altas:")
            for venta in sorted(anomalias_altas, key=lambda x: x["total"], reverse=True)[:3]:
                print(f"  {venta['id']}: ${venta['total']:,.2f} - {venta['producto']} ({venta['fecha']})")
        
        return anomalias_altas, anomalias_bajas
    
    def generar_reporte_ejecutivo(self):
        """Genera reporte ejecutivo completo."""
        self.log_proceso("Generando reporte ejecutivo")
        
        # Métricas clave
        total_ventas = sum(v["total"] for v in self.datos_ventas)
        total_transacciones = len(self.datos_ventas)
        ticket_promedio = total_ventas / total_transacciones
        
        productos_unicos = len(set(v["producto"] for v in self.datos_ventas))
        regiones_activas = len(set(v["region"] for v in self.datos_ventas))
        vendedores_activos = len(set(v["vendedor_id"] for v in self.datos_ventas))
        
        # Producto más vendido
        productos_counter = Counter(v["producto"] for v in self.datos_ventas)
        producto_top = productos_counter.most_common(1)[0]
        
        # Región con más ventas
        ventas_por_region = defaultdict(float)
        for venta in self.datos_ventas:
            ventas_por_region[venta["region"]] += venta["total"]
        
        region_top = max(ventas_por_region.items(), key=lambda x: x[1])
        
        reporte = {
            "fecha_generacion": datetime.now().isoformat(),
            "periodo_analizado": "2024-01-01 a 2024-06-12",
            "metricas_generales": {
                "ingresos_totales": round(total_ventas, 2),
                "transacciones": total_transacciones,
                "ticket_promedio": round(ticket_promedio, 2),
                "productos_unicos": productos_unicos,
                "regiones_activas": regiones_activas,
                "vendedores_activos": vendedores_activos
            },
            "top_performers": {
                "producto_mas_vendido": {
                    "nombre": producto_top[0],
                    "ventas": producto_top[1]
                },
                "region_top_ingresos": {
                    "region": region_top[0],
                    "ingresos": round(region_top[1], 2)
                }
            },
            "datos_externos": {
                "usuarios_api": len(self.datos_usuarios)
            }
        }
        
        # Guardar reporte
        archivo_reporte = self.configuracion["archivos_salida"]["reporte_general"]
        with open(archivo_reporte, 'w') as f:
            json.dump(reporte, f, indent=2)
        
        print(f"\n📊 REPORTE EJECUTIVO")
        print("=" * 25)
        print(f"💰 Ingresos totales: ${total_ventas:,.2f}")
        print(f"🛒 Transacc# 🚀 Bootcamp Ingeniería de Datos - Ejercicios Completos")
