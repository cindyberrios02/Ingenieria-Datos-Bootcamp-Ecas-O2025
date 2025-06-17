import csv
import json
from datetime import datetime
import os


class SistemaInventario:
    """
    Sistema completo de gestión de inventario con funcionalidades avanzadas.
    """
    
    def __init__(self):
        """Inicializa el sistema de inventario."""
        self.inventario = {}
        self.historial_movimientos = []
        self.categorias_validas = set()
        
    def agregar_producto(self, nombre, cantidad, precio, categoria):
        """
        Agrega un producto al inventario con validaciones.
        
        Args:
            nombre (str): Nombre del producto
            cantidad (int): Cantidad en stock
            precio (float): Precio unitario
            categoria (str): Categoría del producto
            
        Returns:
            bool: True si se agregó exitosamente, False en caso contrario
        """
        try:
            # Validaciones
            if not isinstance(nombre, str) or not nombre.strip():
                raise ValueError("El nombre del producto debe ser una cadena no vacía")
            
            if not isinstance(cantidad, int) or cantidad < 0:
                raise ValueError("La cantidad debe ser un número entero positivo")
            
            if not isinstance(precio, (int, float)) or precio < 0:
                raise ValueError("El precio debe ser un número positivo")
            
            if not isinstance(categoria, str) or not categoria.strip():
                raise ValueError("La categoría debe ser una cadena no vacía")
            
            # Normalizar datos
            nombre = nombre.strip().title()
            categoria = categoria.strip().title()
            precio = float(precio)
            
            # Verificar si el producto ya existe
            if nombre in self.inventario:
                print(f"⚠️ El producto '{nombre}' ya existe. Use actualizar_producto() para modificarlo.")
                return False
            
            # Agregar producto
            self.inventario[nombre] = {
                'cantidad': cantidad,
                'precio': precio,
                'categoria': categoria,
                'fecha_agregado': datetime.now().isoformat()
            }
            
            # Agregar categoría a la lista de válidas
            self.categorias_validas.add(categoria)
            
            # Registrar movimiento
            self._registrar_movimiento('AGREGAR', nombre, cantidad, f"Producto agregado: {cantidad} unidades a ${precio:.2f}")
            
            print(f"✅ Producto '{nombre}' agregado exitosamente")
            return True
            
        except ValueError as e:
            print(f"❌ Error al agregar producto: {e}")
            return False
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            return False
    
    def eliminar_producto(self, nombre):
        """
        Elimina un producto del inventario.
        
        Args:
            nombre (str): Nombre del producto a eliminar
            
        Returns:
            bool: True si se eliminó exitosamente, False en caso contrario
        """
        try:
            if not isinstance(nombre, str) or not nombre.strip():
                raise ValueError("El nombre del producto debe ser una cadena no vacía")
            
            nombre = nombre.strip().title()
            
            if nombre in self.inventario:
                producto_eliminado = self.inventario[nombre]
                del self.inventario[nombre]
                
                # Registrar movimiento
                self._registrar_movimiento('ELIMINAR', nombre, 0, f"Producto eliminado del inventario")
                
                print(f"✅ Producto '{nombre}' eliminado exitosamente")
                return True
            else:
                print(f"❌ El producto '{nombre}' no existe en el inventario")
                return False
                
        except ValueError as e:
            print(f"❌ Error: {e}")
            return False
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            return False
    
    def actualizar_producto(self, nombre, cantidad=None, precio=None, categoria=None):
        """
        Actualiza los datos de un producto existente.
        
        Args:
            nombre (str): Nombre del producto
            cantidad (int, optional): Nueva cantidad
            precio (float, optional): Nuevo precio
            categoria (str, optional): Nueva categoría
            
        Returns:
            bool: True si se actualizó exitosamente, False en caso contrario
        """
        try:
            if not isinstance(nombre, str) or not nombre.strip():
                raise ValueError("El nombre del producto debe ser una cadena no vacía")
            
            nombre = nombre.strip().title()
            
            if nombre not in self.inventario:
                print(f"❌ El producto '{nombre}' no existe en el inventario")
                return False
            
            cambios = []
            
            # Actualizar cantidad
            if cantidad is not None:
                if not isinstance(cantidad, int) or cantidad < 0:
                    raise ValueError("La cantidad debe ser un número entero positivo")
                
                cantidad_anterior = self.inventario[nombre]['cantidad']
                self.inventario[nombre]['cantidad'] = cantidad
                cambios.append(f"cantidad: {cantidad_anterior} → {cantidad}")
                
                # Registrar movimiento de stock
                diferencia = cantidad - cantidad_anterior
                tipo_movimiento = 'ENTRADA' if diferencia > 0 else 'SALIDA'
                self._registrar_movimiento(tipo_movimiento, nombre, abs(diferencia), 
                                         f"Ajuste de inventario: {diferencia:+d} unidades")
            
            # Actualizar precio
            if precio is not None:
                if not isinstance(precio, (int, float)) or precio < 0:
                    raise ValueError("El precio debe ser un número positivo")
                
                precio_anterior = self.inventario[nombre]['precio']
                self.inventario[nombre]['precio'] = float(precio)
                cambios.append(f"precio: ${precio_anterior:.2f} → ${precio:.2f}")
            
            # Actualizar categoría
            if categoria is not None:
                if not isinstance(categoria, str) or not categoria.strip():
                    raise ValueError("La categoría debe ser una cadena no vacía")
                
                categoria = categoria.strip().title()
                categoria_anterior = self.inventario[nombre]['categoria']
                self.inventario[nombre]['categoria'] = categoria
                self.categorias_validas.add(categoria)
                cambios.append(f"categoría: {categoria_anterior} → {categoria}")
            
            if cambios:
                print(f"✅ Producto '{nombre}' actualizado: {', '.join(cambios)}")
                return True
            else:
                print(f"⚠️ No se realizaron cambios en el producto '{nombre}'")
                return False
                
        except ValueError as e:
            print(f"❌ Error: {e}")
            return False
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            return False
    
    def listar_por_categoria(self, categoria):
        """
        Lista todos los productos de una categoría específica.
        
        Args:
            categoria (str): Categoría a filtrar
            
        Returns:
            list: Lista de productos en la categoría
        """
        try:
            if not isinstance(categoria, str) or not categoria.strip():
                raise ValueError("La categoría debe ser una cadena no vacía")
            
            categoria = categoria.strip().title()
            productos_categoria = []
            
            print(f"\n📦 PRODUCTOS EN CATEGORÍA: {categoria.upper()}")
            print("=" * 60)
            
            encontrados = False
            for nombre, detalles in self.inventario.items():
                if detalles['categoria'].lower() == categoria.lower():
                    valor_total = detalles['cantidad'] * detalles['precio']
                    productos_categoria.append({
                        'nombre': nombre,
                        'cantidad': detalles['cantidad'],
                        'precio': detalles['precio'],
                        'valor_total': valor_total
                    })
                    
                    print(f"🔸 {nombre}")
                    print(f"   Cantidad: {detalles['cantidad']} unidades")
                    print(f"   Precio: ${detalles['precio']:.2f}")
                    print(f"   Valor total: ${valor_total:.2f}")
                    print(f"   Fecha agregado: {detalles.get('fecha_agregado', 'N/A')}")
                    print("-" * 40)
                    encontrados = True
            
            if not encontrados:
                print(f"❌ No se encontraron productos en la categoría '{categoria}'")
                print(f"📋 Categorías disponibles: {', '.join(self.categorias_validas) if self.categorias_validas else 'Ninguna'}")
            else:
                # Estadísticas de la categoría
                total_productos = len(productos_categoria)
                total_unidades = sum(p['cantidad'] for p in productos_categoria)
                valor_categoria = sum(p['valor_total'] for p in productos_categoria)
                
                print(f"\n📊 RESUMEN DE CATEGORÍA:")
                print(f"   Total productos: {total_productos}")
                print(f"   Total unidades: {total_unidades}")
                print(f"   Valor total categoría: ${valor_categoria:.2f}")
            
            return productos_categoria
            
        except ValueError as e:
            print(f"❌ Error: {e}")
            return []
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            return []
    
    def calcular_valor_total(self):
        """
        Calcula el valor total del inventario.
        
        Returns:
            float: Valor total del inventario
        """
        try:
            if not self.inventario:
                print("📦 El inventario está vacío")
                return 0.0
            
            valor_total = sum(
                detalles['cantidad'] * detalles['precio'] 
                for detalles in self.inventario.values()
            )
            
            # Estadísticas adicionales
            total_productos = len(self.inventario)
            total_unidades = sum(detalles['cantidad'] for detalles in self.inventario.values())
            precio_promedio = sum(detalles['precio'] for detalles in self.inventario.values()) / total_productos
            
            print(f"\n💰 VALOR TOTAL DEL INVENTARIO")
            print("=" * 40)
            print(f"💵 Valor total: ${valor_total:,.2f}")
            print(f"📦 Total productos: {total_productos}")
            print(f"📊 Total unidades: {total_unidades:,}")
            print(f"📈 Precio promedio: ${precio_promedio:.2f}")
            
            return valor_total
            
        except Exception as e:
            print(f"❌ Error al calcular valor total: {e}")
            return 0.0
    
    def exportar_inventario_csv(self, nombre_archivo="inventario.csv"):
        """
        Exporta el inventario a un archivo CSV.
        
        Args:
            nombre_archivo (str): Nombre del archivo CSV
            
        Returns:
            bool: True si se exportó exitosamente, False en caso contrario
        """
        try:
            if not self.inventario:
                print("❌ No hay productos en el inventario para exportar")
                return False
            
            with open(nombre_archivo, 'w', newline='', encoding='utf-8') as archivo_csv:
                campos = ['Producto', 'Cantidad', 'Precio', 'Categoría', 'Valor_Total', 'Fecha_Agregado']
                writer = csv.writer(archivo_csv)
                
                # Escribir encabezados
                writer.writerow(campos)
                
                # Escribir datos
                for nombre, detalles in self.inventario.items():
                    valor_total = detalles['cantidad'] * detalles['precio']
                    writer.writerow([
                        nombre,
                        detalles['cantidad'],
                        detalles['precio'],
                        detalles['categoria'],
                        valor_total,
                        detalles.get('fecha_agregado', 'N/A')
                    ])
            
            print(f"✅ Inventario exportado exitosamente a '{nombre_archivo}'")
            print(f"📁 Ubicación: {os.path.abspath(nombre_archivo)}")
            return True
            
        except Exception as e:
            print(f"❌ Error al exportar inventario: {e}")
            return False
    
    def importar_inventario_csv(self, nombre_archivo):
        """
        Importa inventario desde un archivo CSV.
        
        Args:
            nombre_archivo (str): Nombre del archivo CSV
            
        Returns:
            bool: True si se importó exitosamente, False en caso contrario
        """
        try:
            if not os.path.exists(nombre_archivo):
                print(f"❌ El archivo '{nombre_archivo}' no existe")
                return False
            
            productos_importados = 0
            
            with open(nombre_archivo, 'r', encoding='utf-8') as archivo_csv:
                reader = csv.DictReader(archivo_csv)
                
                for fila in reader:
                    try:
                        nombre = fila['Producto']
                        cantidad = int(fila['Cantidad'])
                        precio = float(fila['Precio'])
                        categoria = fila['Categoría']
                        
                        if self.agregar_producto(nombre, cantidad, precio, categoria):
                            productos_importados += 1
                            
                    except (ValueError, KeyError) as e:
                        print(f"⚠️ Error en fila {reader.line_num}: {e}")
                        continue
            
            print(f"✅ Importación completada: {productos_importados} productos importados")
            return productos_importados > 0
            
        except Exception as e:
            print(f"❌ Error al importar inventario: {e}")
            return False
    
    def exportar_inventario_json(self, nombre_archivo="inventario.json"):
        """
        Exporta el inventario a un archivo JSON.
        
        Args:
            nombre_archivo (str): Nombre del archivo JSON
            
        Returns:
            bool: True si se exportó exitosamente, False en caso contrario
        """
        try:
            if not self.inventario:
                print("❌ No hay productos en el inventario para exportar")
                return False
            
            # Preparar datos para JSON
            datos_exportacion = {
                'inventario': self.inventario,
                'historial_movimientos': self.historial_movimientos,
                'fecha_exportacion': datetime.now().isoformat(),
                'total_productos': len(self.inventario),
                'valor_total': sum(d['cantidad'] * d['precio'] for d in self.inventario.values())
            }
            
            with open(nombre_archivo, 'w', encoding='utf-8') as archivo_json:
                json.dump(datos_exportacion, archivo_json, indent=2, ensure_ascii=False)
            
            print(f"✅ Inventario exportado a JSON: '{nombre_archivo}'")
            return True
            
        except Exception as e:
            print(f"❌ Error al exportar a JSON: {e}")
            return False
    
    def buscar_producto(self, termino_busqueda):
        """
        Busca productos por nombre o categoría.
        
        Args:
            termino_busqueda (str): Término a buscar
            
        Returns:
            list: Lista de productos encontrados
        """
        try:
            if not isinstance(termino_busqueda, str) or not termino_busqueda.strip():
                raise ValueError("El término de búsqueda debe ser una cadena no vacía")
            
            termino = termino_busqueda.strip().lower()
            productos_encontrados = []
            
            print(f"\n🔍 RESULTADOS DE BÚSQUEDA PARA: '{termino_busqueda}'")
            print("=" * 50)
            
            for nombre, detalles in self.inventario.items():
                if (termino in nombre.lower() or 
                    termino in detalles['categoria'].lower()):
                    
                    productos_encontrados.append({
                        'nombre': nombre,
                        'detalles': detalles
                    })
                    
                    valor_total = detalles['cantidad'] * detalles['precio']
                    print(f"🔸 {nombre}")
                    print(f"   Categoría: {detalles['categoria']}")
                    print(f"   Cantidad: {detalles['cantidad']}")
                    print(f"   Precio: ${detalles['precio']:.2f}")
                    print(f"   Valor: ${valor_total:.2f}")
                    print("-" * 30)
            
            if not productos_encontrados:
                print(f"❌ No se encontraron productos que coincidan con '{termino_busqueda}'")
            else:
                print(f"📊 Se encontraron {len(productos_encontrados)} producto(s)")
            
            return productos_encontrados
            
        except ValueError as e:
            print(f"❌ Error: {e}")
            return []
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            return []
    
    def obtener_productos_bajo_stock(self, umbral=5):
        """
        Obtiene productos con stock bajo.
        
        Args:
            umbral (int): Cantidad mínima considerada como stock bajo
            
        Returns:
            list: Lista de productos con stock bajo
        """
        try:
            productos_bajo_stock = []
            
            for nombre, detalles in self.inventario.items():
                if detalles['cantidad'] <= umbral:
                    productos_bajo_stock.append({
                        'nombre': nombre,
                        'cantidad': detalles['cantidad'],
                        'categoria': detalles['categoria'],
                        'precio': detalles['precio']
                    })
            
            if productos_bajo_stock:
                print(f"\n⚠️ PRODUCTOS CON STOCK BAJO (≤{umbral} unidades)")
                print("=" * 50)
                for producto in productos_bajo_stock:
                    print(f"🔸 {producto['nombre']}")
                    print(f"   Cantidad: {producto['cantidad']} unidades")
                    print(f"   Categoría: {producto['categoria']}")
                    print(f"   Precio: ${producto['precio']:.2f}")
                    print("-" * 30)
                print(f"📊 Total productos con stock bajo: {len(productos_bajo_stock)}")
            else:
                print(f"✅ No hay productos con stock bajo (≤{umbral} unidades)")
            
            return productos_bajo_stock
            
        except Exception as e:
            print(f"❌ Error al verificar stock bajo: {e}")
            return []
    
    def mostrar_resumen_categorias(self):
        """
        Muestra un resumen estadístico por categorías.
        """
        try:
            if not self.inventario:
                print("📦 El inventario está vacío")
                return
            
            estadisticas_categorias = {}
            
            # Calcular estadísticas por categoría
            for nombre, detalles in self.inventario.items():
                categoria = detalles['categoria']
                
                if categoria not in estadisticas_categorias:
                    estadisticas_categorias[categoria] = {
                        'productos': 0,
                        'unidades_totales': 0,
                        'valor_total': 0.0,
                        'precio_promedio': 0.0,
                        'precios': []
                    }
                
                stats = estadisticas_categorias[categoria]
                stats['productos'] += 1
                stats['unidades_totales'] += detalles['cantidad']
                stats['valor_total'] += detalles['cantidad'] * detalles['precio']
                stats['precios'].append(detalles['precio'])
            
            # Calcular precio promedio
            for categoria, stats in estadisticas_categorias.items():
                stats['precio_promedio'] = sum(stats['precios']) / len(stats['precios'])
            
            print(f"\n📊 RESUMEN POR CATEGORÍAS")
            print("=" * 60)
            
            for categoria, stats in estadisticas_categorias.items():
                print(f"\n🔹 {categoria.upper()}")
                print(f"   Productos únicos: {stats['productos']}")
                print(f"   Unidades totales: {stats['unidades_totales']:,}")
                print(f"   Valor total: ${stats['valor_total']:,.2f}")
                print(f"   Precio promedio: ${stats['precio_promedio']:.2f}")
                print("-" * 40)
            
        except Exception as e:
            print(f"❌ Error al mostrar resumen: {e}")
    
    def _registrar_movimiento(self, tipo, producto, cantidad, descripcion):
        """
        Registra un movimiento en el historial.
        
        Args:
            tipo (str): Tipo de movimiento (AGREGAR, ELIMINAR, ENTRADA, SALIDA)
            producto (str): Nombre del producto
            cantidad (int): Cantidad involucrada
            descripcion (str): Descripción del movimiento
        """
        movimiento = {
            'timestamp': datetime.now().isoformat(),
            'tipo': tipo,
            'producto': producto,
            'cantidad': cantidad,
            'descripcion': descripcion
        }
        self.historial_movimientos.append(movimiento)
    
    def mostrar_historial_movimientos(self, limite=10):
        """
        Muestra el historial de movimientos recientes.
        
        Args:
            limite (int): Número máximo de movimientos a mostrar
        """
        try:
            if not self.historial_movimientos:
                print("📋 No hay movimientos registrados")
                return
            
            print(f"\n📋 HISTORIAL DE MOVIMIENTOS (últimos {limite})")
            print("=" * 60)
            
            # Mostrar los últimos movimientos
            movimientos_recientes = self.historial_movimientos[-limite:]
            
            for movimiento in reversed(movimientos_recientes):
                timestamp = datetime.fromisoformat(movimiento['timestamp'])
                fecha_formateada = timestamp.strftime("%d/%m/%Y %H:%M:%S")
                
                print(f"🔸 {fecha_formateada}")
                print(f"   Tipo: {movimiento['tipo']}")
                print(f"   Producto: {movimiento['producto']}")
                print(f"   Cantidad: {movimiento['cantidad']}")
                print(f"   Descripción: {movimiento['descripcion']}")
                print("-" * 40)
            
        except Exception as e:
            print(f"❌ Error al mostrar historial: {e}")
    
    def mostrar_inventario_completo(self):
        """
        Muestra todo el inventario de forma organizada.
        """
        try:
            if not self.inventario:
                print("📦 El inventario está vacío")
                return
            
            print(f"\n📦 INVENTARIO COMPLETO")
            print("=" * 60)
            
            # Organizar por categorías
            productos_por_categoria = {}
            for nombre, detalles in self.inventario.items():
                categoria = detalles['categoria']
                if categoria not in productos_por_categoria:
                    productos_por_categoria[categoria] = []
                productos_por_categoria[categoria].append((nombre, detalles))
            
            # Mostrar por categoría
            for categoria in sorted(productos_por_categoria.keys()):
                print(f"\n🔹 {categoria.upper()}")
                print("-" * 30)
                
                for nombre, detalles in sorted(productos_por_categoria[categoria]):
                    valor_total = detalles['cantidad'] * detalles['precio']
                    stock_status = "🔴" if detalles['cantidad'] <= 5 else "🟢"
                    
                    print(f"  {stock_status} {nombre}")
                    print(f"     Cantidad: {detalles['cantidad']} | Precio: ${detalles['precio']:.2f} | Valor: ${valor_total:.2f}")
            
            # Resumen final
            print(f"\n📊 RESUMEN GENERAL:")
            total_productos = len(self.inventario)
            total_categorias = len(productos_por_categoria)
            valor_total = sum(d['cantidad'] * d['precio'] for d in self.inventario.values())
            
            print(f"   Total productos: {total_productos}")
            print(f"   Total categorías: {total_categorias}")
            print(f"   Valor total: ${valor_total:,.2f}")
            
        except Exception as e:
            print(f"❌ Error al mostrar inventario: {e}")


# Función para probar el sistema
def demo_sistema_inventario():
    """
    Función de demostración del sistema de inventario.
    """
    print("🎓 BOOTCAMP INGENIERÍA DE DATOS - CLASE 04")
    print("📦 DEMO: Sistema de Gestión de Inventario")
    print("=" * 60)
    
    # Crear instancia del sistema
    sistema = SistemaInventario()
    
    print("\n1. 📥 AGREGANDO PRODUCTOS AL INVENTARIO")
    print("-" * 40)
    
    # Agregar productos de prueba
    productos_demo = [
        ("Laptop Dell", 15, 750.00, "Electrónica"),
        ("Mouse Inalámbrico", 50, 25.99, "Electrónica"),
        ("Teclado Mecánico", 30, 89.50, "Electrónica"),
        ("Manzanas", 100, 0.75, "Alimentos"),
        ("Plátanos", 80, 0.50, "Alimentos"),
        ("Leche", 40, 1.20, "Alimentos"),
        ("Cuaderno", 200, 2.50, "Papelería"),
        ("Bolígrafo", 500, 0.99, "Papelería"),
        ("Silla Oficina", 8, 150.00, "Muebles"),
        ("Mesa Escritorio", 5, 200.00, "Muebles")
    ]
    
    for nombre, cantidad, precio, categoria in productos_demo:
        sistema.agregar_producto(nombre, cantidad, precio, categoria)
    
    print("\n2. 📊 MOSTRANDO VALOR TOTAL DEL INVENTARIO")
    print("-" * 45)
    sistema.calcular_valor_total()
    
    print("\n3. 📋 LISTANDO PRODUCTOS POR CATEGORÍA")
    print("-" * 40)
    sistema.listar_por_categoria("Electrónica")
    
    print("\n4. 🔄 ACTUALIZANDO PRODUCTOS")
    print("-" * 30)
    sistema.actualizar_producto("Laptop Dell", cantidad=12, precio=720.00)
    sistema.actualizar_producto("Mouse Inalámbrico", cantidad=45)
    
    print("\n5. 🔍 BÚSQUEDA DE PRODUCTOS")
    print("-" * 30)
    sistema.buscar_producto("laptop")
    
    print("\n6. ⚠️ PRODUCTOS CON STOCK BAJO")
    print("-" * 35)
    sistema.obtener_productos_bajo_stock(10)
    
    print("\n7. 📊 RESUMEN POR CATEGORÍAS")
    print("-" * 32)
    sistema.mostrar_resumen_categorias()
    
    print("\n8. 💾 EXPORTANDO A CSV")
    print("-" * 25)
    sistema.exportar_inventario_csv("demo_inventario.csv")
    
    print("\n9. 💾 EXPORTANDO A JSON")
    print("-" * 26)
    sistema.exportar_inventario_json("demo_inventario.json")
    
    print("\n10. 📋 HISTORIAL DE MOVIMIENTOS")
    print("-" * 35)
    sistema.mostrar_historial_movimientos(5)
    
    print("\n11. ❌ ELIMINANDO UN PRODUCTO")
    print("-" * 33)
    sistema.eliminar_producto("Silla Oficina")
    
    print("\n12. 📦 INVENTARIO FINAL")
    print("-" * 25)
    sistema.mostrar_inventario_completo()
    
    print(f"\n✅ ¡Demo completada exitosamente!")
    print(f"🎓 Has visto todas las funcionalidades del sistema de inventario")
    
    return sistema


if __name__ == "__main__":
    # Ejecutar demostración
    sistema_demo = demo_sistema_inventario()