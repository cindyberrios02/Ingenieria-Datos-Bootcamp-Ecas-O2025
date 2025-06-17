from sistema_inventario import SistemaInventario
import os


class MenuInventario:
    """
    Clase para manejar el menú interactivo del sistema de inventario.
    """
    
    def __init__(self):
        """Inicializa el menú con una instancia del sistema."""
        self.sistema = SistemaInventario()
        self.ejecutando = True
    
    def mostrar_menu_principal(self):
        """Muestra el menú principal de opciones."""
        print("\n" + "="*60)
        print("📦 SISTEMA DE GESTIÓN DE INVENTARIO")
        print("🎓 Bootcamp Ingeniería de Datos - Clase 04")
        print("="*60)
        print("Selecciona una opción:")
        print("1.  ➕ Agregar producto")
        print("2.  ❌ Eliminar producto")
        print("3.  🔄 Actualizar producto")
        print("4.  📋 Listar por categoría")
        print("5.  💰 Calcular valor total")
        print("6.  🔍 Buscar productos")
        print("7.  📦 Mostrar inventario completo")
        print("8.  ⚠️  Productos con stock bajo")
        print("9.  📊 Resumen por categorías")
        print("10. 📋 Historial de movimientos")
        print("11. 💾 Exportar a CSV")
        print("12. 💾 Exportar a JSON")
        print("13. 📥 Importar desde CSV")
        print("14. 🧪 Cargar datos de prueba")
        print("15. 🗑️  Limpiar inventario")
        print("0.  🚪 Salir")
        print("-" * 60)
    
    def obtener_opcion(self):
        """Obtiene y valida la opción del usuario."""
        try:
            opcion = input("👉 Ingresa tu opción (0-15): ").strip()
            return opcion
        except KeyboardInterrupt:
            print("\n\n👋 Programa interrumpido por el usuario")
            return "0"
    
    def obtener_datos_producto(self):
        """Obtiene los datos de un producto del usuario."""
        try:
            print("\n📝 DATOS DEL PRODUCTO")
            print("-" * 25)
            
            nombre = input("🔸 Nombre del producto: ").strip()
            if not nombre:
                raise ValueError("El nombre no puede estar vacío")
            
            cantidad = int(input("🔸 Cantidad: "))
            if cantidad < 0:
                raise ValueError("La cantidad debe ser positiva")
            
            precio = float(input("🔸 Precio unitario: $"))
            if precio < 0:
                raise ValueError("El precio debe ser positivo")
            
            categoria = input("🔸 Categoría: ").strip()
            if not categoria:
                raise ValueError("La categoría no puede estar vacía")
            
            return nombre, cantidad, precio, categoria
            
        except ValueError as e:
            print(f"❌ Error en los datos: {e}")
            return None
        except KeyboardInterrupt:
            print("\n⏸️ Operación cancelada")
            return None
    
    def opcion_agregar_producto(self):
        """Maneja la opción de agregar producto."""
        print("\n➕ AGREGAR NUEVO PRODUCTO")
        print("=" * 30)
        
        datos = self.obtener_datos_producto()
        if datos:
            nombre, cantidad, precio, categoria = datos
            self.sistema.agregar_producto(nombre, cantidad, precio, categoria)
        
        self.pausa()
    
    def opcion_eliminar_producto(self):
        """Maneja la opción de eliminar producto."""
        print("\n❌ ELIMINAR PRODUCTO")
        print("=" * 22)
        
        try:
            # Mostrar productos disponibles
            if not self.sistema.inventario:
                print("❌ No hay productos en el inventario")
                self.pausa()
                return
            
            print("📦 Productos disponibles:")
            for i, nombre in enumerate(self.sistema.inventario.keys(), 1):
                print(f"  {i}. {nombre}")
            
            nombre = input("\n🔸 Nombre del producto a eliminar: ").strip()
            if nombre:
                self.sistema.eliminar_producto(nombre)
            else:
                print("❌ Nombre no válido")
                
        except KeyboardInterrupt:
            print("\n⏸️ Operación cancelada")
        
        self.pausa()
    
    def opcion_actualizar_producto(self):
        """Maneja la opción de actualizar producto."""
        print("\n🔄 ACTUALIZAR PRODUCTO")
        print("=" * 24)
        
        try:
            if not self.sistema.inventario:
                print("❌ No hay productos en el inventario")
                self.pausa()
                return
            
            print("📦 Productos disponibles:")
            for i, (nombre, detalles) in enumerate(self.sistema.inventario.items(), 1):
                print(f"  {i}. {nombre} - Cantidad: {detalles['cantidad']} - Precio: ${detalles['precio']:.2f}")
            
            nombre = input("\n🔸 Nombre del producto a actualizar: ").strip()
            if not nombre:
                print("❌ Nombre no válido")
                self.pausa()
                return
            
            if nombre not in self.sistema.inventario:
                print(f"❌ El producto '{nombre}' no existe")
                self.pausa()
                return
            
            print(f"\n📋 Datos actuales de '{nombre}':")
            detalles = self.sistema.inventario[nombre]
            print(f"   Cantidad: {detalles['cantidad']}")
            print(f"   Precio: ${detalles['precio']:.2f}")
            print(f"   Categoría: {detalles['categoria']}")
            
            print(f"\n💡 Deja en blanco para mantener el valor actual")
            
            # Obtener nuevos valores
            nueva_cantidad = input("🔸 Nueva cantidad: ").strip()
            nuevo_precio = input("🔸 Nuevo precio: $").strip()
            nueva_categoria = input("🔸 Nueva categoría: ").strip()
            
            # Convertir valores
            cantidad = int(nueva_cantidad) if nueva_cantidad else None
            precio = float(nuevo_precio) if nuevo_precio else None
            categoria = nueva_categoria if nueva_categoria else None
            
            self.sistema.actualizar_producto(nombre, cantidad, precio, categoria)
            
        except ValueError as e:
            print(f"❌ Error en los datos: {e}")
        except KeyboardInterrupt:
            print("\n⏸️ Operación cancelada")
        
        self.pausa()
    
    def opcion_listar_por_categoria(self):
        """Maneja la opción de listar por categoría."""
        print("\n📋 LISTAR POR CATEGORÍA")
        print("=" * 25)
        
        try:
            if not self.sistema.inventario:
                print("❌ No hay productos en el inventario")
                self.pausa()
                return
            
            print("🏷️ Categorías disponibles:")
            for i, categoria in enumerate(self.sistema.categorias_validas, 1):
                print(f"  {i}. {categoria}")
            
            categoria = input("\n🔸 Ingresa la categoría: ").strip()
            if categoria:
                self.sistema.listar_por_categoria(categoria)
            else:
                print("❌ Categoría no válida")
                
        except KeyboardInterrupt:
            print("\n⏸️ Operación cancelada")
        
        self.pausa()
    
    def opcion_calcular_valor_total(self):
        """Maneja la opción de calcular valor total."""
        print("\n💰 CALCULAR VALOR TOTAL")
        print("=" * 26)
        
        self.sistema.calcular_valor_total()
        self.pausa()
    
    def opcion_buscar_productos(self):
        """Maneja la opción de buscar productos."""
        print("\n🔍 BUSCAR PRODUCTOS")
        print("=" * 21)
        
        try:
            termino = input("🔸 Término de búsqueda (nombre o categoría): ").strip()
            if termino:
                self.sistema.buscar_producto(termino)
            else:
                print("❌ Término de búsqueda no válido")
                
        except KeyboardInterrupt:
            print("\n⏸️ Operación cancelada")
        
        self.pausa()
    
    def opcion_mostrar_inventario_completo(self):
        """Maneja la opción de mostrar inventario completo."""
        print("\n📦 INVENTARIO COMPLETO")
        print("=" * 24)
        
        self.sistema.mostrar_inventario_completo()
        self.pausa()
    
    def opcion_productos_stock_bajo(self):
        """Maneja la opción de productos con stock bajo."""
        print("\n⚠️ PRODUCTOS CON STOCK BAJO")
        print("=" * 31)
        
        try:
            umbral_input = input("🔸 Umbral de stock bajo (default: 5): ").strip()
            umbral = int(umbral_input) if umbral_input else 5
            
            self.sistema.obtener_productos_bajo_stock(umbral)
            
        except ValueError:
            print("❌ Umbral no válido, usando default (5)")
            self.sistema.obtener_productos_bajo_stock(5)
        except KeyboardInterrupt:
            print("\n⏸️ Operación cancelada")
        
        self.pausa()
    
    def opcion_resumen_categorias(self):
        """Maneja la opción de resumen por categorías."""
        print("\n📊 RESUMEN POR CATEGORÍAS")
        print("=" * 29)
        
        self.sistema.mostrar_resumen_categorias()
        self.pausa()
    
    def opcion_historial_movimientos(self):
        """Maneja la opción de historial de movimientos."""
        print("\n📋 HISTORIAL DE MOVIMIENTOS")
        print("=" * 31)
        
        try:
            limite_input = input("🔸 Número de movimientos a mostrar (default: 10): ").strip()
            limite = int(limite_input) if limite_input else 10
            
            self.sistema.mostrar_historial_movimientos(limite)
            
        except ValueError:
            print("❌ Número no válido, usando default (10)")
            self.sistema.mostrar_historial_movimientos(10)
        except KeyboardInterrupt:
            print("\n⏸️ Operación cancelada")
        
        self.pausa()
    
    def opcion_exportar_csv(self):
        """Maneja la opción de exportar a CSV."""
        print("\n💾 EXPORTAR A CSV")
        print("=" * 19)
        
        try:
            nombre_archivo = input("🔸 Nombre del archivo (default: inventario.csv): ").strip()
            if not nombre_archivo:
                nombre_archivo = "inventario.csv"
            
            if not nombre_archivo.endswith('.csv'):
                nombre_archivo += '.csv'
            
            self.sistema.exportar_inventario_csv(nombre_archivo)
            
        except KeyboardInterrupt:
            print("\n⏸️ Operación cancelada")
        
        self.pausa()
    
    def opcion_exportar_json(self):
        """Maneja la opción de exportar a JSON."""
        print("\n💾 EXPORTAR A JSON")
        print("=" * 20)
        
        try:
            nombre_archivo = input("🔸 Nombre del archivo (default: inventario.json): ").strip()
            if not nombre_archivo:
                nombre_archivo = "inventario.json"
            
            if not nombre_archivo.endswith('.json'):
                nombre_archivo += '.json'
            
            self.sistema.exportar_inventario_json(nombre_archivo)
            
        except KeyboardInterrupt:
            print("\n⏸️ Operación cancelada")
        
        self.pausa()
    
    def opcion_importar_csv(self):
        """Maneja la opción de importar desde CSV."""
        print("\n📥 IMPORTAR DESDE CSV")
        print("=" * 22)
        
        try:
            nombre_archivo = input("🔸 Nombre del archivo CSV: ").strip()
            if nombre_archivo:
                self.sistema.importar_inventario_csv(nombre_archivo)
            else:
                print("❌ Nombre de archivo no válido")
                
        except KeyboardInterrupt:
            print("\n⏸️ Operación cancelada")
        
        self.pausa()
    
    def opcion_cargar_datos_prueba(self):
        """Carga datos de prueba en el inventario."""
        print("\n🧪 CARGAR DATOS DE PRUEBA")
        print("=" * 27)
        
        if self.sistema.inventario:
            confirmar = input("⚠️ Esto agregará productos al inventario existente. ¿Continuar? (s/n): ").strip().lower()
            if confirmar not in ['s', 'si', 'sí', 'y', 'yes']:
                print("❌ Operación cancelada")
                self.pausa()
                return
        
        # Datos de prueba
        productos_prueba = [
            ("Laptop Gaming", 8, 1200.00, "Electrónica"),
            ("Monitor 4K", 15, 350.00, "Electrónica"),
            ("Teclado RGB", 25, 75.00, "Electrónica"),
            ("Mouse Gaming", 40, 45.00, "Electrónica"),
            ("Arroz", 200, 1.50, "Alimentos"),
            ("Pasta", 150, 0.99, "Alimentos"),
            ("Aceite de Oliva", 30, 8.50, "Alimentos"),
            ("Cuaderno A4", 100, 3.25, "Papelería"),
            ("Bolígrafos Pack", 80, 5.99, "Papelería"),
            ("Marcadores", 60, 12.50, "Papelería"),
            ("Silla Ergonómica", 6, 180.00, "Muebles"),
            ("Escritorio", 4, 250.00, "Muebles"),
            ("Estantería", 10, 120.00, "Muebles")
        ]
        
        print("📦 Agregando productos de prueba...")
        agregados = 0
        
        for nombre, cantidad, precio, categoria in productos_prueba:
            if self.sistema.agregar_producto(nombre, cantidad, precio, categoria):
                agregados += 1
        
        print(f"✅ Se agregaron {agregados} productos de prueba")
        self.pausa()
    
    def opcion_limpiar_inventario(self):
        """Limpia completamente el inventario."""
        print("\n🗑️ LIMPIAR INVENTARIO")
        print("=" * 22)
        
        if not self.sistema.inventario:
            print("📦 El inventario ya está vacío")
            self.pausa()
            return
        
        print(f"⚠️ ADVERTENCIA: Esto eliminará TODOS los productos del inventario")
        print(f"📊 Actualmente tienes {len(self.sistema.inventario)} productos")
        
        confirmar = input("\n¿Estás seguro? Escribe 'CONFIRMAR' para continuar: ").strip()
        
        if confirmar == "CONFIRMAR":
            # Limpiar inventario
            productos_eliminados = len(self.sistema.inventario)
            self.sistema.inventario.clear()
            self.sistema.categorias_validas.clear()
            
            # Registrar en historial
            self.sistema._registrar_movimiento('LIMPIAR', 'TODOS', productos_eliminados, 
                                             f"Inventario limpiado: {productos_eliminados} productos eliminados")
            
            print(f"✅ Inventario limpiado exitosamente")
            print(f"🗑️ Se eliminaron {productos_eliminados} productos")
        else:
            print("❌ Operación cancelada")
        
        self.pausa()
    
    def pausa(self):
        """Pausa el programa hasta que el usuario presione Enter."""
        try:
            input("\n⏸️ Presiona Enter para continuar...")
        except KeyboardInterrupt:
            pass
    
    def limpiar_pantalla(self):
        """Limpia la pantalla según el sistema operativo."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def ejecutar(self):
        """Ejecuta el bucle principal del programa."""
        print("🎉 ¡Bienvenido al Sistema de Gestión de Inventario!")
        print("💡 Usa Ctrl+C en cualquier momento para cancelar una operación")
        
        while self.ejecutando:
            try:
                self.mostrar_menu_principal()
                opcion = self.obtener_opcion()
                
                if opcion == "0":
                    self.ejecutando = False
                    print("\n👋 ¡Gracias por usar el Sistema de Inventario!")
                    print("🎓 Ejercicio de Clase 04 completado")
                    
                elif opcion == "1":
                    self.opcion_agregar_producto()
                elif opcion == "2":
                    self.opcion_eliminar_producto()
                elif opcion == "3":
                    self.opcion_actualizar_producto()
                elif opcion == "4":
                    self.opcion_listar_por_categoria()
                elif opcion == "5":
                    self.opcion_calcular_valor_total()
                elif opcion == "6":
                    self.opcion_buscar_productos()
                elif opcion == "7":
                    self.opcion_mostrar_inventario_completo()
                elif opcion == "8":
                    self.opcion_productos_stock_bajo()
                elif opcion == "9":
                    self.opcion_resumen_categorias()
                elif opcion == "10":
                    self.opcion_historial_movimientos()
                elif opcion == "11":
                    self.opcion_exportar_csv()
                elif opcion == "12":
                    self.opcion_exportar_json()
                elif opcion == "13":
                    self.opcion_importar_csv()
                elif opcion == "14":
                    self.opcion_cargar_datos_prueba()
                elif opcion == "15":
                    self.opcion_limpiar_inventario()
                else:
                    print("❌ Opción no válida. Por favor, selecciona un número del 0 al 15.")
                    self.pausa()
                    
            except KeyboardInterrupt:
                print("\n\n🤔 ¿Quieres salir del programa? (s/n): ", end="")
                try:
                    respuesta = input().strip().lower()
                    if respuesta in ['s', 'si', 'sí', 'y', 'yes']:
                        self.ejecutando = False
                        print("👋 ¡Hasta luego!")
                    else:
                        print("📱 Continuando con el programa...")
                except KeyboardInterrupt:
                    self.ejecutando = False
                    print("\n👋 ¡Hasta luego!")
            except Exception as e:
                print(f"\n❌ Error inesperado: {e}")
                print("🔄 El programa continuará funcionando...")
                self.pausa()


def main():
    """Función principal del programa."""
    try:
        menu = MenuInventario()
        menu.ejecutar()
    except Exception as e:
        print(f"❌ Error crítico: {e}")
        print("💡 Por favor, reinicia el programa")


if __name__ == "__main__":
    main()