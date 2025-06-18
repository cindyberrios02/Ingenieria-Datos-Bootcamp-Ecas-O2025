# Sistema de Biblioteca con Préstamo Simple y Manejo de Excepciones
# Aplicación práctica de POO y excepciones personalizadas

from datetime import datetime, timedelta
from typing import List, Dict, Optional
import json


# ==================== EXCEPCIONES PERSONALIZADAS ====================

class BibliotecaError(Exception):
    """Excepción base para errores del sistema de biblioteca."""
    pass


class LibroNoDisponibleError(BibliotecaError):
    """Excepción lanzada cuando un libro no está disponible para préstamo."""
    
    def __init__(self, titulo: str, stock_actual: int = 0):
        self.titulo = titulo
        self.stock_actual = stock_actual
        mensaje = f"El libro '{titulo}' no está disponible para préstamo."
        if stock_actual == 0:
            mensaje += " No hay ejemplares en stock."
        else:
            mensaje += f" Stock actual: {stock_actual} ejemplar(es) pero todos están prestados."
        super().__init__(mensaje)


class LibroNoEncontradoError(BibliotecaError):
    """Excepción lanzada cuando un libro no existe en la biblioteca."""
    
    def __init__(self, titulo: str):
        self.titulo = titulo
        super().__init__(f"El libro '{titulo}' no existe en el catálogo de la biblioteca.")


class UsuarioNoValidoError(BibliotecaError):
    """Excepción lanzada cuando un usuario no es válido."""
    
    def __init__(self, usuario: str, razon: str = ""):
        self.usuario = usuario
        mensaje = f"Usuario '{usuario}' no válido."
        if razon:
            mensaje += f" Razón: {razon}"
        super().__init__(mensaje)


# ==================== CLASES PRINCIPALES ====================

class Libro:
    """
    Clase que representa un libro en la biblioteca.
    """
    
    def __init__(self, titulo: str, autor: str, stock: int = 1):
        """
        Inicializa un libro con título, autor y stock.
        
        Args:
            titulo (str): Título del libro
            autor (str): Autor del libro
            stock (int): Cantidad de ejemplares disponibles
            
        Raises:
            ValueError: Si algún parámetro no es válido
        """
        self.titulo = self._validar_titulo(titulo)
        self.autor = self._validar_autor(autor)
        self.stock_total = self._validar_stock(stock)
        self.stock_disponible = self.stock_total
        self.prestamos_activos = []
        self.historial_prestamos = []
        self.fecha_agregado = datetime.now()
    
    def _validar_titulo(self, titulo: str) -> str:
        """Valida y formatea el título del libro."""
        if not isinstance(titulo, str):
            raise ValueError("El título debe ser una cadena de texto")
        
        titulo = titulo.strip()
        if not titulo:
            raise ValueError("El título no puede estar vacío")
        
        if len(titulo) < 2:
            raise ValueError("El título debe tener al menos 2 caracteres")
        
        return titulo.title()
    
    def _validar_autor(self, autor: str) -> str:
        """Valida y formatea el autor del libro."""
        if not isinstance(autor, str):
            raise ValueError("El autor debe ser una cadena de texto")
        
        autor = autor.strip()
        if not autor:
            raise ValueError("El autor no puede estar vacío")
        
        if len(autor) < 2:
            raise ValueError("El autor debe tener al menos 2 caracteres")
        
        return autor.title()
    
    def _validar_stock(self, stock: int) -> int:
        """Valida el stock del libro."""
        if not isinstance(stock, int):
            raise ValueError("El stock debe ser un número entero")
        
        if stock < 0:
            raise ValueError("El stock no puede ser negativo")
        
        if stock > 100:
            raise ValueError("El stock no puede ser mayor a 100 ejemplares")
        
        return stock
    
    def esta_disponible(self) -> bool:
        """
        Verifica si el libro está disponible para préstamo.
        
        Returns:
            bool: True si hay ejemplares disponibles, False en caso contrario
        """
        return self.stock_disponible > 0
    
    def prestar(self, usuario: str) -> Dict:
        """
        Presta un ejemplar del libro a un usuario.
        
        Args:
            usuario (str): Nombre del usuario que solicita el préstamo
            
        Returns:
            dict: Información del préstamo realizado
            
        Raises:
            LibroNoDisponibleError: Si no hay ejemplares disponibles
            UsuarioNoValidoError: Si el usuario no es válido
        """
        # Validar usuario
        if not isinstance(usuario, str) or not usuario.strip():
            raise UsuarioNoValidoError(usuario, "Nombre de usuario vacío o inválido")
        
        usuario = usuario.strip().title()
        
        # Verificar disponibilidad
        if not self.esta_disponible():
            raise LibroNoDisponibleError(self.titulo, self.stock_disponible)
        
        # Realizar préstamo
        self.stock_disponible -= 1
        
        prestamo = {
            'usuario': usuario,
            'fecha_prestamo': datetime.now(),
            'fecha_devolucion_esperada': datetime.now() + timedelta(days=14),
            'devuelto': False,
            'id_prestamo': len(self.historial_prestamos) + 1
        }
        
        self.prestamos_activos.append(prestamo)
        self.historial_prestamos.append(prestamo.copy())
        
        return prestamo
    
    def devolver(self, usuario: str) -> Dict:
        """
        Devuelve un ejemplar del libro.
        
        Args:
            usuario (str): Nombre del usuario que devuelve el libro
            
        Returns:
            dict: Información de la devolución
            
        Raises:
            ValueError: Si el usuario no tiene préstamos activos de este libro
        """
        usuario = usuario.strip().title()
        
        # Buscar préstamo activo del usuario
        prestamo_activo = None
        for i, prestamo in enumerate(self.prestamos_activos):
            if prestamo['usuario'] == usuario:
                prestamo_activo = prestamo
                del self.prestamos_activos[i]
                break
        
        if not prestamo_activo:
            raise ValueError(f"El usuario '{usuario}' no tiene préstamos activos de '{self.titulo}'")
        
        # Procesar devolución
        self.stock_disponible += 1
        fecha_devolucion = datetime.now()
        
        # Actualizar historial
        for prestamo in self.historial_prestamos:
            if (prestamo['usuario'] == usuario and 
                prestamo['id_prestamo'] == prestamo_activo['id_prestamo'] and
                not prestamo['devuelto']):
                prestamo['devuelto'] = True
                prestamo['fecha_devolucion_real'] = fecha_devolucion
                break
        
        # Calcular días de retraso
        dias_retraso = max(0, (fecha_devolucion - prestamo_activo['fecha_devolucion_esperada']).days)
        
        return {
            'usuario': usuario,
            'fecha_devolucion': fecha_devolucion,
            'dias_retraso': dias_retraso,
            'multa': dias_retraso * 0.50  # $0.50 por día de retraso
        }
    
    def obtener_info(self) -> Dict:
        """
        Obtiene información completa del libro.
        
        Returns:
            dict: Información detallada del libro
        """
        return {
            'titulo': self.titulo,
            'autor': self.autor,
            'stock_total': self.stock_total,
            'stock_disponible': self.stock_disponible,
            'prestamos_activos': len(self.prestamos_activos),
            'total_prestamos': len(self.historial_prestamos),
            'disponible': self.esta_disponible(),
            'fecha_agregado': self.fecha_agregado.strftime('%d/%m/%Y')
        }
    
    def __str__(self) -> str:
        """Representación en cadena del libro."""
        estado = "Disponible" if self.esta_disponible() else "No disponible"
        return f"'{self.titulo}' por {self.autor} - {estado} ({self.stock_disponible}/{self.stock_total})"
    
    def __repr__(self) -> str:
        """Representación oficial del libro."""
        return f"Libro('{self.titulo}', '{self.autor}', {self.stock_total})"


class Biblioteca:
    """
    Clase que representa una biblioteca con sistema de préstamos.
    """
    
    def __init__(self, nombre: str = "Biblioteca Central"):
        """
        Inicializa la biblioteca.
        
        Args:
            nombre (str): Nombre de la biblioteca
        """
        self.nombre = nombre
        self.catalogo: Dict[str, Libro] = {}
        self.usuarios_registrados = set()
        self.historial_sistema = []
        self.fecha_creacion = datetime.now()
    
    def agregar_libro(self, titulo: str, autor: str, stock: int = 1) -> Libro:
        """
        Agrega un libro al catálogo de la biblioteca.
        
        Args:
            titulo (str): Título del libro
            autor (str): Autor del libro
            stock (int): Cantidad de ejemplares
            
        Returns:
            Libro: El libro agregado
            
        Raises:
            ValueError: Si el libro ya existe o los parámetros son inválidos
        """
        try:
            titulo_normalizado = titulo.strip().title()
            
            if titulo_normalizado in self.catalogo:
                # Si el libro ya existe, agregar al stock
                libro_existente = self.catalogo[titulo_normalizado]
                libro_existente.stock_total += stock
                libro_existente.stock_disponible += stock
                
                self._registrar_evento(f"Stock actualizado para '{titulo_normalizado}': +{stock} ejemplares")
                return libro_existente
            else:
                # Crear nuevo libro
                nuevo_libro = Libro(titulo, autor, stock)
                self.catalogo[titulo_normalizado] = nuevo_libro
                
                self._registrar_evento(f"Libro agregado: '{titulo_normalizado}' por {autor}")
                return nuevo_libro
                
        except ValueError as e:
            self._registrar_evento(f"Error al agregar libro: {e}")
            raise
    
    def prestar_libro(self, titulo: str, usuario: str) -> Dict:
        """
        Presta un libro a un usuario.
        
        Args:
            titulo (str): Título del libro a prestar
            usuario (str): Nombre del usuario
            
        Returns:
            dict: Información del préstamo
            
        Raises:
            LibroNoEncontradoError: Si el libro no existe
            LibroNoDisponibleError: Si el libro no está disponible
            UsuarioNoValidoError: Si el usuario no es válido
        """
        try:
            titulo_normalizado = titulo.strip().title()
            
            # Verificar si el libro existe
            if titulo_normalizado not in self.catalogo:
                raise LibroNoEncontradoError(titulo)
            
            # Registrar usuario si es nuevo
            usuario_normalizado = usuario.strip().title()
            self.usuarios_registrados.add(usuario_normalizado)
            
            # Realizar préstamo
            libro = self.catalogo[titulo_normalizado]
            prestamo = libro.prestar(usuario_normalizado)
            
            self._registrar_evento(f"Préstamo realizado: '{titulo_normalizado}' a {usuario_normalizado}")
            
            return prestamo
            
        except (LibroNoEncontradoError, LibroNoDisponibleError, UsuarioNoValidoError) as e:
            self._registrar_evento(f"Error en préstamo: {e}")
            raise
    
    def devolver_libro(self, titulo: str, usuario: str) -> Dict:
        """
        Procesa la devolución de un libro.
        
        Args:
            titulo (str): Título del libro a devolver
            usuario (str): Nombre del usuario
            
        Returns:
            dict: Información de la devolución
            
        Raises:
            LibroNoEncontradoError: Si el libro no existe
            ValueError: Si el usuario no tiene el libro prestado
        """
        try:
            titulo_normalizado = titulo.strip().title()
            usuario_normalizado = usuario.strip().title()
            
            # Verificar si el libro existe
            if titulo_normalizado not in self.catalogo:
                raise LibroNoEncontradoError(titulo)
            
            # Procesar devolución
            libro = self.catalogo[titulo_normalizado]
            devolucion = libro.devolver(usuario_normalizado)
            
            mensaje_evento = f"Devolución: '{titulo_normalizado}' por {usuario_normalizado}"
            if devolucion['dias_retraso'] > 0:
                mensaje_evento += f" (Retraso: {devolucion['dias_retraso']} días, Multa: ${devolucion['multa']:.2f})"
            
            self._registrar_evento(mensaje_evento)
            
            return devolucion
            
        except (LibroNoEncontradoError, ValueError) as e:
            self._registrar_evento(f"Error en devolución: {e}")
            raise
    
    def buscar_libro(self, titulo: str) -> Optional[Libro]:
        """
        Busca un libro en el catálogo.
        
        Args:
            titulo (str): Título del libro a buscar
            
        Returns:
            Libro o None: El libro encontrado o None si no existe
        """
        titulo_normalizado = titulo.strip().title()
        return self.catalogo.get(titulo_normalizado)
    
    def listar_libros_disponibles(self) -> List[Libro]:
        """
        Lista todos los libros disponibles para préstamo.
        
        Returns:
            list: Lista de libros disponibles
        """
        return [libro for libro in self.catalogo.values() if libro.esta_disponible()]
    
    def listar_todos_los_libros(self) -> List[Libro]:
        """
        Lista todos los libros en el catálogo.
        
        Returns:
            list: Lista de todos los libros
        """
        return list(self.catalogo.values())
    
    def obtener_estadisticas(self) -> Dict:
        """
        Obtiene estadísticas de la biblioteca.
        
        Returns:
            dict: Estadísticas detalladas
        """
        total_libros = len(self.catalogo)
        total_ejemplares = sum(libro.stock_total for libro in self.catalogo.values())
        ejemplares_disponibles = sum(libro.stock_disponible for libro in self.catalogo.values())
        ejemplares_prestados = total_ejemplares - ejemplares_disponibles
        total_prestamos = sum(len(libro.historial_prestamos) for libro in self.catalogo.values())
        
        return {
            'nombre_biblioteca': self.nombre,
            'total_titulos': total_libros,
            'total_ejemplares': total_ejemplares,
            'ejemplares_disponibles': ejemplares_disponibles,
            'ejemplares_prestados': ejemplares_prestados,
            'usuarios_registrados': len(self.usuarios_registrados),
            'total_prestamos_historicos': total_prestamos,
            'porcentaje_ocupacion': (ejemplares_prestados / total_ejemplares * 100) if total_ejemplares > 0 else 0
        }
    
    def _registrar_evento(self, descripcion: str):
        """Registra un evento en el historial del sistema."""
        evento = {
            'timestamp': datetime.now(),
            'descripcion': descripcion
        }
        self.historial_sistema.append(evento)
        
        # Mantener solo los últimos 100 eventos
        if len(self.historial_sistema) > 100:
            self.historial_sistema.pop(0)
    
    def mostrar_historial(self, limite: int = 10):
        """
        Muestra el historial reciente de eventos.
        
        Args:
            limite (int): Número máximo de eventos a mostrar
        """
        if not self.historial_sistema:
            print("📋 No hay eventos registrados")
            return
        
        print(f"\n📋 HISTORIAL DE EVENTOS ({self.nombre})")
        print("=" * 50)
        
        eventos_recientes = self.historial_sistema[-limite:]
        for evento in reversed(eventos_recientes):
            timestamp = evento['timestamp'].strftime("%d/%m/%Y %H:%M:%S")
            print(f"[{timestamp}] {evento['descripcion']}")


# ==================== FUNCIONES DE DEMOSTRACIÓN ====================

def demo_basica_biblioteca():
    """
    Demostración básica del sistema de biblioteca con manejo de excepciones.
    """
    print("📚 DEMO: SISTEMA DE BIBLIOTECA CON EXCEPCIONES")
    print("=" * 55)
    
    # Crear biblioteca
    biblioteca = Biblioteca("Biblioteca Central Demo")
    
    print(f"🏛️ Biblioteca creada: {biblioteca.nombre}")
    
    # Agregar libros
    print(f"\n📖 Agregando libros al catálogo...")
    try:
        libro1 = biblioteca.agregar_libro("Cien Años de Soledad", "Gabriel García Márquez", 3)
        libro2 = biblioteca.agregar_libro("Don Quijote", "Miguel de Cervantes", 2)
        libro3 = biblioteca.agregar_libro("1984", "George Orwell", 1)
        
        print(f"✅ Libros agregados exitosamente")
        
    except ValueError as e:
        print(f"❌ Error al agregar libro: {e}")
    
    # Mostrar catálogo
    print(f"\n📚 Catálogo actual:")
    for libro in biblioteca.listar_todos_los_libros():
        print(f"   {libro}")
    
    # Casos de préstamo exitoso
    print(f"\n✅ CASOS DE PRÉSTAMO EXITOSO")
    print("-" * 35)
    
    casos_exitosos = [
        ("Cien Años de Soledad", "Ana García"),
        ("Don Quijote", "Carlos López"),
        ("1984", "María Rodríguez")
    ]
    
    for titulo, usuario in casos_exitosos:
        try:
            prestamo = biblioteca.prestar_libro(titulo, usuario)
            print(f"📖 '{titulo}' prestado a {usuario}")
            print(f"   Fecha límite: {prestamo['fecha_devolucion_esperada'].strftime('%d/%m/%Y')}")
            
        except (LibroNoEncontradoError, LibroNoDisponibleError, UsuarioNoValidoError) as e:
            print(f"❌ Error: {e}")
    
    # Casos de error - Libro no disponible
    print(f"\n❌ CASOS DE ERROR - LIBRO NO DISPONIBLE")
    print("-" * 45)
    
    try:
        biblioteca.prestar_libro("1984", "Pedro Martín")  # Ya está prestado
    except LibroNoDisponibleError as e:
        print(f"🚫 Excepción capturada: {e}")
        print(f"   Tipo: {type(e).__name__}")
        print(f"   Libro: {e.titulo}")
        print(f"   Stock actual: {e.stock_actual}")
    
    # Casos de error - Libro no encontrado
    print(f"\n❌ CASOS DE ERROR - LIBRO NO ENCONTRADO")
    print("-" * 45)
    
    try:
        biblioteca.prestar_libro("El Hobbit", "Luis Pérez")  # No existe
    except LibroNoEncontradoError as e:
        print(f"🚫 Excepción capturada: {e}")
        print(f"   Tipo: {type(e).__name__}")
        print(f"   Libro buscado: {e.titulo}")
    
    # Casos de error - Usuario no válido
    print(f"\n❌ CASOS DE ERROR - USUARIO NO VÁLIDO")
    print("-" * 42)
    
    try:
        biblioteca.prestar_libro("Don Quijote", "")  # Usuario vacío
    except UsuarioNoValidoError as e:
        print(f"🚫 Excepción capturada: {e}")
        print(f"   Tipo: {type(e).__name__}")
    
    # Devolución exitosa
    print(f"\n🔄 DEVOLUCIÓN DE LIBROS")
    print("-" * 25)
    
    try:
        devolucion = biblioteca.devolver_libro("Cien Años de Soledad", "Ana García")
        print(f"✅ Libro devuelto por Ana García")
        if devolucion['dias_retraso'] > 0:
            print(f"   ⏰ Días de retraso: {devolucion['dias_retraso']}")
            print(f"   💰 Multa: ${devolucion['multa']:.2f}")
        else:
            print(f"   ⏰ Devuelto a tiempo")
            
    except (LibroNoEncontradoError, ValueError) as e:
        print(f"❌ Error en devolución: {e}")
    
    # Mostrar estadísticas
    print(f"\n📊 ESTADÍSTICAS DE LA BIBLIOTECA")
    print("-" * 35)
    
    stats = biblioteca.obtener_estadisticas()
    for clave, valor in stats.items():
        if isinstance(valor, float):
            print(f"   {clave}: {valor:.1f}")
        else:
            print(f"   {clave}: {valor}")
    
    # Mostrar historial
    print(f"\n📋 HISTORIAL RECIENTE")
    print("-" * 22)
    biblioteca.mostrar_historial(5)


def sistema_interactivo():
    """
    Sistema interactivo de biblioteca.
    """
    biblioteca = Biblioteca("Mi Biblioteca Personal")
    
    # Agregar algunos libros de ejemplo
    libros_iniciales = [
        ("El Principito", "Antoine de Saint-Exupéry", 2),
        ("Cien Años de Soledad", "Gabriel García Márquez", 1),
        ("1984", "George Orwell", 3),
        ("To Kill a Mockingbird", "Harper Lee", 2),
        ("The Great Gatsby", "F. Scott Fitzgerald", 1)
    ]
    
    print("📚 Inicializando biblioteca con libros de ejemplo...")
    for titulo, autor, stock in libros_iniciales:
        biblioteca.agregar_libro(titulo, autor, stock)
    
    while True:
        print(f"\n" + "="*60)
        print(f"📚 SISTEMA DE BIBLIOTECA - {biblioteca.nombre}")
        print("="*60)
        print("Selecciona una opción:")
        print("1. 📖 Prestar libro")
        print("2. 🔄 Devolver libro")
        print("3. 🔍 Buscar libro")
        print("4. 📋 Ver libros disponibles")
        print("5. 📚 Ver todo el catálogo")
        print("6. ➕ Agregar libro")
        print("7. 📊 Ver estadísticas")
        print("8. 📋 Ver historial")
        print("9. 🎓 Demo de excepciones")
        print("0. 🚪 Salir")
        print("-" * 60)
        
        try:
            opcion = input("👉 Ingresa tu opción (0-9): ").strip()
            
            if opcion == "0":
                print("\n👋 ¡Gracias por usar el sistema de biblioteca!")
                break
                
            elif opcion == "1":
                titulo = input("📖 Título del libro: ").strip()
                usuario = input("👤 Nombre del usuario: ").strip()
                
                try:
                    prestamo = biblioteca.prestar_libro(titulo, usuario)
                    print(f"✅ Préstamo exitoso!")
                    print(f"   Libro: {titulo}")
                    print(f"   Usuario: {usuario}")
                    print(f"   Fecha límite: {prestamo['fecha_devolucion_esperada'].strftime('%d/%m/%Y')}")
                    
                except LibroNoEncontradoError as e:
                    print(f"❌ {e}")
                except LibroNoDisponibleError as e:
                    print(f"❌ {e}")
                except UsuarioNoValidoError as e:
                    print(f"❌ {e}")
                    
            elif opcion == "2":
                titulo = input("📖 Título del libro a devolver: ").strip()
                usuario = input("👤 Nombre del usuario: ").strip()
                
                try:
                    devolucion = biblioteca.devolver_libro(titulo, usuario)
                    print(f"✅ Devolución exitosa!")
                    if devolucion['dias_retraso'] > 0:
                        print(f"   ⏰ Días de retraso: {devolucion['dias_retraso']}")
                        print(f"   💰 Multa: ${devolucion['multa']:.2f}")
                    else:
                        print(f"   ⏰ Devuelto a tiempo")
                        
                except LibroNoEncontradoError as e:
                    print(f"❌ {e}")
                except ValueError as e:
                    print(f"❌ {e}")
                    
            elif opcion == "3":
                titulo = input("🔍 Título a buscar: ").strip()
                libro = biblioteca.buscar_libro(titulo)
                
                if libro:
                    info = libro.obtener_info()
                    print(f"✅ Libro encontrado:")
                    print(f"   Título: {info['titulo']}")
                    print(f"   Autor: {info['autor']}")
                    print(f"   Stock: {info['stock_disponible']}/{info['stock_total']}")
                    print(f"   Estado: {'Disponible' if info['disponible'] else 'No disponible'}")
                else:
                    print(f"❌ Libro no encontrado: '{titulo}'")
                    
            elif opcion == "4":
                libros_disponibles = biblioteca.listar_libros_disponibles()
                if libros_disponibles:
                    print(f"\n📚 Libros disponibles ({len(libros_disponibles)}):")
                    for libro in libros_disponibles:
                        print(f"   {libro}")
                else:
                    print("❌ No hay libros disponibles actualmente")
                    
            elif opcion == "5":
                todos_libros = biblioteca.listar_todos_los_libros()
                if todos_libros:
                    print(f"\n📚 Catálogo completo ({len(todos_libros)} títulos):")
                    for libro in todos_libros:
                        print(f"   {libro}")
                else:
                    print("❌ El catálogo está vacío")
                    
            elif opcion == "6":
                titulo = input("📖 Título del nuevo libro: ").strip()
                autor = input("✍️ Autor: ").strip()
                
                try:
                    stock = int(input("📦 Stock inicial: "))
                    libro = biblioteca.agregar_libro(titulo, autor, stock)
                    print(f"✅ Libro agregado: {libro}")
                except ValueError as e:
                    print(f"❌ Error: {e}")
                    
            elif opcion == "7":
                stats = biblioteca.obtener_estadisticas()
                print(f"\n📊 ESTADÍSTICAS:")
                for clave, valor in stats.items():
                    if isinstance(valor, float):
                        print(f"   {clave.replace('_', ' ').title()}: {valor:.1f}")
                    else:
                        print(f"   {clave.replace('_', ' ').title()}: {valor}")
                        
            elif opcion == "8":
                biblioteca.mostrar_historial(10)
                
            elif opcion == "9":
                demo_basica_biblioteca()
                
            else:
                print("❌ Opción no válida. Selecciona un número del 0 al 9.")
            
            if opcion != "0":
                input("\n⏸️ Presiona Enter para continuar...")
                
        except KeyboardInterrupt:
            print("\n\n👋 ¡Hasta luego!")
            break
        except Exception as e:
            print(f"\n❌ Error inesperado: {e}")
            input("\n⏸️ Presiona Enter para continuar...")


if __name__ == "__main__":
    print("📚 SISTEMA DE BIBLIOTECA CON MANEJO DE EXCEPCIONES")
    print("🎓 Bootcamp Ingeniería de Datos - Aplicación Práctica POO")
    print("=" * 65)
    
    print("\nSelecciona el modo de ejecución:")
    print("1. 🎬 Demo automática (muestra todos los casos)")
    print("2. 🎮 Sistema interactivo")
    print("0. 🚪 Salir")
    
    try:
        modo = input("\n👉 Selecciona (0-2): ").strip()
        
        if modo == "1":
            demo_basica_biblioteca()
        elif modo == "2":
            sistema_interactivo()
        elif modo == "0":
            print("👋 ¡Hasta luego!")
        else:
            print("❌ Opción no válida")
            
    except KeyboardInterrupt:
        print("\n👋 ¡Hasta luego!")
    except Exception as e:
        print(f"❌ Error: {e}")