# Clase 05: Programación Orientada a Objetos (POO)
# Sistema de gestión de personas con validaciones y funcionalidades avanzadas

import re
from datetime import datetime, date
import json


class Persona:
    """
    Clase Persona que representa a una persona con nombre, edad y correo electrónico.
    Incluye validaciones, métodos de actualización y funcionalidades avanzadas.
    """
    
    # Atributo de clase para llevar registro de todas las personas creadas
    contador_personas = 0
    personas_creadas = []
    
    def __init__(self, nombre, edad, correo_electronico):
        """
        Constructor de la clase Persona.
        
        Args:
            nombre (str): Nombre completo de la persona
            edad (int): Edad en años
            correo_electronico (str): Dirección de correo electrónico
            
        Raises:
            ValueError: Si algún parámetro no es válido
        """
        # Validar y asignar atributos
        self.nombre = self._validar_nombre(nombre)
        self.edad = self._validar_edad(edad)
        self.correo_electronico = correo_electronico
        
        # Validar correo al crear la persona
        if not self.validar_correo():
            raise ValueError(f"El correo electrónico '{correo_electronico}' no es válido")
        
        # Atributos adicionales
        self.fecha_creacion = datetime.now()
        self.id_persona = Persona.contador_personas + 1
        
        # Actualizar contador de clase
        Persona.contador_personas += 1
        Persona.personas_creadas.append(self)
    
    def _validar_nombre(self, nombre):
        """
        Valida que el nombre sea válido.
        
        Args:
            nombre (str): Nombre a validar
            
        Returns:
            str: Nombre validado y formateado
            
        Raises:
            ValueError: Si el nombre no es válido
        """
        if not isinstance(nombre, str):
            raise ValueError("El nombre debe ser una cadena de texto")
        
        nombre = nombre.strip()
        if not nombre:
            raise ValueError("El nombre no puede estar vacío")
        
        if len(nombre) < 2:
            raise ValueError("El nombre debe tener al menos 2 caracteres")
        
        if len(nombre) > 100:
            raise ValueError("El nombre no puede tener más de 100 caracteres")
        
        # Verificar que solo contenga letras y espacios
        if not re.match(r'^[a-zA-ZÀ-ÿñÑ\s]+$', nombre):
            raise ValueError("El nombre solo puede contener letras y espacios")
        
        # Formatear nombre (primera letra de cada palabra en mayúscula)
        return ' '.join(word.capitalize() for word in nombre.split())
    
    def _validar_edad(self, edad):
        """
        Valida que la edad sea válida.
        
        Args:
            edad (int): Edad a validar
            
        Returns:
            int: Edad validada
            
        Raises:
            ValueError: Si la edad no es válida
        """
        if not isinstance(edad, int):
            raise ValueError("La edad debe ser un número entero")
        
        if edad < 0:
            raise ValueError("La edad no puede ser negativa")
        
        if edad > 150:
            raise ValueError("La edad no puede ser mayor a 150 años")
        
        return edad
    
    def mostrar_datos(self):
        """
        Muestra los datos de la persona en un formato amigable.
        """
        print(f"👤 INFORMACIÓN PERSONAL")
        print(f"=" * 30)
        print(f"🆔 ID: {self.id_persona}")
        print(f"📝 Nombre: {self.nombre}")
        print(f"🎂 Edad: {self.edad} años")
        print(f"📧 Email: {self.correo_electronico}")
        print(f"✅ Correo válido: {'Sí' if self.validar_correo() else 'No'}")
        print(f"🔞 Mayor de edad: {'Sí' if self.es_mayor_de_edad() else 'No'}")
        print(f"📅 Creado: {self.fecha_creacion.strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"🎯 Categoría: {self.obtener_categoria_edad()}")
    
    def validar_correo(self):
        """
        Valida si el correo electrónico tiene un formato válido usando expresiones regulares.
        
        Returns:
            bool: True si el correo es válido, False en caso contrario
        """
        # Patrón mejorado para validación de correo electrónico
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        # Verificaciones adicionales
        if not isinstance(self.correo_electronico, str):
            return False
        
        if len(self.correo_electronico) > 254:  # RFC 5321
            return False
        
        # Verificar que no tenga caracteres especiales problemáticos
        if '..' in self.correo_electronico:
            return False
        
        if self.correo_electronico.startswith('.') or self.correo_electronico.endswith('.'):
            return False
        
        return bool(re.match(patron, self.correo_electronico))
    
    def actualizar_datos(self, nombre=None, edad=None, correo_electronico=None):
        """
        Permite actualizar los datos de la persona con validaciones.
        
        Args:
            nombre (str, optional): Nuevo nombre
            edad (int, optional): Nueva edad
            correo_electronico (str, optional): Nuevo correo electrónico
            
        Returns:
            dict: Diccionario con los cambios realizados
        """
        cambios = {}
        
        try:
            # Actualizar nombre si se proporciona
            if nombre is not None:
                nombre_anterior = self.nombre
                self.nombre = self._validar_nombre(nombre)
                cambios['nombre'] = {'anterior': nombre_anterior, 'nuevo': self.nombre}
                print(f"✅ Nombre actualizado: {nombre_anterior} → {self.nombre}")
            
            # Actualizar edad si se proporciona
            if edad is not None:
                edad_anterior = self.edad
                self.edad = self._validar_edad(edad)
                cambios['edad'] = {'anterior': edad_anterior, 'nuevo': self.edad}
                print(f"✅ Edad actualizada: {edad_anterior} → {self.edad} años")
            
            # Actualizar correo si se proporciona
            if correo_electronico is not None:
                correo_anterior = self.correo_electronico
                self.correo_electronico = correo_electronico
                
                if self.validar_correo():
                    cambios['correo_electronico'] = {'anterior': correo_anterior, 'nuevo': self.correo_electronico}
                    print(f"✅ Correo actualizado: {correo_anterior} → {self.correo_electronico}")
                else:
                    # Revertir si el correo no es válido
                    self.correo_electronico = correo_anterior
                    raise ValueError(f"El correo '{correo_electronico}' no es válido")
            
            if cambios:
                print(f"📝 Actualización completada exitosamente")
            else:
                print(f"⚠️ No se realizaron cambios")
            
            return cambios
            
        except ValueError as e:
            print(f"❌ Error al actualizar: {e}")
            return {}
    
    def es_mayor_de_edad(self):
        """
        Verifica si la persona es mayor de edad (18 años o más).
        
        Returns:
            bool: True si es mayor de edad, False en caso contrario
        """
        return self.edad >= 18
    
    def obtener_categoria_edad(self):
        """
        Obtiene la categoría de edad de la persona.
        
        Returns:
            str: Categoría de edad
        """
        if self.edad < 13:
            return "Niño/a"
        elif self.edad < 18:
            return "Adolescente"
        elif self.edad < 30:
            return "Joven Adulto"
        elif self.edad < 60:
            return "Adulto"
        else:
            return "Adulto Mayor"
    
    def calcular_año_nacimiento(self):
        """
        Calcula el año aproximado de nacimiento.
        
        Returns:
            int: Año de nacimiento aproximado
        """
        año_actual = datetime.now().year
        return año_actual - self.edad
    
    def dias_hasta_cumpleanos(self, fecha_cumpleanos):
        """
        Calcula los días hasta el próximo cumpleaños.
        
        Args:
            fecha_cumpleanos (str): Fecha de cumpleaños en formato 'DD/MM'
            
        Returns:
            int: Días hasta el cumpleaños
        """
        try:
            dia, mes = map(int, fecha_cumpleanos.split('/'))
            año_actual = datetime.now().year
            cumple_este_año = datetime(año_actual, mes, dia).date()
            hoy = date.today()
            
            if cumple_este_año < hoy:
                cumple_proximo = datetime(año_actual + 1, mes, dia).date()
            else:
                cumple_proximo = cumple_este_año
            
            dias = (cumple_proximo - hoy).days
            return dias
            
        except Exception as e:
            print(f"❌ Error al calcular días hasta cumpleaños: {e}")
            return None
    
    # EJERCICIO PLUS: Comparar edades
    def comparar_edad_con(self, otra_persona):
        """
        Compara la edad con otra persona y devuelve quién es mayor.
        
        Args:
            otra_persona (Persona): Otra instancia de Persona
            
        Returns:
            str: Resultado de la comparación
        """
        if not isinstance(otra_persona, Persona):
            raise ValueError("El parámetro debe ser una instancia de la clase Persona")
        
        if self.edad > otra_persona.edad:
            diferencia = self.edad - otra_persona.edad
            return f"{self.nombre} es mayor que {otra_persona.nombre} por {diferencia} año(s)"
        elif self.edad < otra_persona.edad:
            diferencia = otra_persona.edad - self.edad
            return f"{otra_persona.nombre} es mayor que {self.nombre} por {diferencia} año(s)"
        else:
            return f"{self.nombre} y {otra_persona.nombre} tienen la misma edad ({self.edad} años)"
    
    @classmethod
    def comparar_dos_personas(cls, persona1, persona2):
        """
        Método de clase para comparar dos personas.
        
        Args:
            persona1 (Persona): Primera persona
            persona2 (Persona): Segunda persona
            
        Returns:
            str: Resultado de la comparación
        """
        return persona1.comparar_edad_con(persona2)
    
    def obtener_generacion(self):
        """
        Determina la generación a la que pertenece la persona.
        
        Returns:
            str: Generación correspondiente
        """
        año_nacimiento = self.calcular_año_nacimiento()
        
        if año_nacimiento >= 1997:
            return "Generación Z"
        elif año_nacimiento >= 1981:
            return "Millennial"
        elif año_nacimiento >= 1965:
            return "Generación X"
        elif año_nacimiento >= 1946:
            return "Baby Boomer"
        else:
            return "Generación Silenciosa"
    
    def to_dict(self):
        """
        Convierte los datos de la persona a un diccionario.
        
        Returns:
            dict: Datos de la persona en formato diccionario
        """
        return {
            'id': self.id_persona,
            'nombre': self.nombre,
            'edad': self.edad,
            'correo_electronico': self.correo_electronico,
            'es_mayor_de_edad': self.es_mayor_de_edad(),
            'categoria_edad': self.obtener_categoria_edad(),
            'año_nacimiento': self.calcular_año_nacimiento(),
            'generacion': self.obtener_generacion(),
            'fecha_creacion': self.fecha_creacion.isoformat()
        }
    
    @classmethod
    def from_dict(cls, datos):
        """
        Crea una instancia de Persona desde un diccionario.
        
        Args:
            datos (dict): Diccionario con los datos de la persona
            
        Returns:
            Persona: Nueva instancia de Persona
        """
        return cls(datos['nombre'], datos['edad'], datos['correo_electronico'])
    
    @classmethod
    def obtener_estadisticas_generales(cls):
        """
        Obtiene estadísticas generales de todas las personas creadas.
        
        Returns:
            dict: Estadísticas generales
        """
        if not cls.personas_creadas:
            return {"mensaje": "No hay personas registradas"}
        
        edades = [p.edad for p in cls.personas_creadas]
        correos_validos = sum(1 for p in cls.personas_creadas if p.validar_correo())
        mayores_edad = sum(1 for p in cls.personas_creadas if p.es_mayor_de_edad())
        
        return {
            'total_personas': len(cls.personas_creadas),
            'edad_promedio': sum(edades) / len(edades),
            'edad_minima': min(edades),
            'edad_maxima': max(edades),
            'correos_validos': correos_validos,
            'porcentaje_correos_validos': (correos_validos / len(cls.personas_creadas)) * 100,
            'mayores_de_edad': mayores_edad,
            'porcentaje_mayores_edad': (mayores_edad / len(cls.personas_creadas)) * 100
        }
    
    def __str__(self):
        """
        Representación en cadena de la persona.
        
        Returns:
            str: Cadena descriptiva de la persona
        """
        return f"Persona(ID:{self.id_persona}, {self.nombre}, {self.edad} años, {self.correo_electronico})"
    
    def __repr__(self):
        """
        Representación oficial de la persona.
        
        Returns:
            str: Representación oficial
        """
        return f"Persona('{self.nombre}', {self.edad}, '{self.correo_electronico}')"
    
    def __eq__(self, other):
        """
        Compara si dos personas son iguales.
        
        Args:
            other: Otra persona a comparar
            
        Returns:
            bool: True si son iguales, False en caso contrario
        """
        if not isinstance(other, Persona):
            return False
        return (self.nombre == other.nombre and 
                self.edad == other.edad and 
                self.correo_electronico == other.correo_electronico)
    
    def __lt__(self, other):
        """
        Compara si una persona es menor que otra (por edad).
        
        Args:
            other (Persona): Otra persona a comparar
            
        Returns:
            bool: True si esta persona es menor, False en caso contrario
        """
        if not isinstance(other, Persona):
            raise ValueError("Solo se puede comparar con otra instancia de Persona")
        return self.edad < other.edad


# Funciones auxiliares para demostración
def demo_clase_persona():
    """
    Función de demostración de la clase Persona.
    """
    print("🎓 BOOTCAMP INGENIERÍA DE DATOS - CLASE 05")
    print("👥 Programación Orientada a Objetos (POO)")
    print("🧑‍💻 Demostración de la Clase Persona")
    print("=" * 60)
    
    # Crear personas de ejemplo
    print("\n📝 1. CREANDO PERSONAS")
    print("-" * 30)
    
    try:
        # Persona 1
        persona1 = Persona("Ana García López", 25, "ana.garcia@email.com")
        print(f"✅ Persona 1 creada: {persona1}")
        
        # Persona 2
        persona2 = Persona("Carlos Mendoza", 17, "carlos.mendoza@gmail.com")
        print(f"✅ Persona 2 creada: {persona2}")
        
        # Persona 3
        persona3 = Persona("María Elena Ruiz", 45, "maria.ruiz@empresa.com")
        print(f"✅ Persona 3 creada: {persona3}")
        
    except ValueError as e:
        print(f"❌ Error al crear persona: {e}")
        return
    
    # Mostrar datos de las personas
    print(f"\n👁️ 2. MOSTRANDO DATOS DE LAS PERSONAS")
    print("-" * 45)
    
    print(f"\n🔸 PERSONA 1:")
    persona1.mostrar_datos()
    
    print(f"\n🔸 PERSONA 2:")
    persona2.mostrar_datos()
    
    print(f"\n🔸 PERSONA 3:")
    persona3.mostrar_datos()
    
    # Validación de correos
    print(f"\n📧 3. VALIDACIÓN DE CORREOS ELECTRÓNICOS")
    print("-" * 45)
    
    correos_prueba = [
        "test@ejemplo.com",
        "correo_invalido",
        "usuario@dominio",
        "test.email+tag@ejemplo.org",
        "@dominio.com",
        "usuario@@ejemplo.com"
    ]
    
    for correo in correos_prueba:
        persona_temp = Persona("Test", 25, "temp@temp.com")
        persona_temp.correo_electronico = correo
        valido = persona_temp.validar_correo()
        estado = "✅ Válido" if valido else "❌ Inválido"
        print(f"   {correo:<25} → {estado}")
    
    # Actualización de datos
    print(f"\n🔄 4. ACTUALIZANDO DATOS")
    print("-" * 30)
    
    print(f"Actualizando datos de {persona1.nombre}:")
    cambios = persona1.actualizar_datos(
        nombre="Ana García Rodríguez",
        edad=26,
        correo_electronico="ana.garcia.nueva@email.com"
    )
    
    if cambios:
        print(f"📋 Cambios realizados: {len(cambios)} campos actualizados")
    
    # Verificación de mayoría de edad
    print(f"\n🔞 5. VERIFICACIÓN DE MAYORÍA DE EDAD")
    print("-" * 45)
    
    for persona in [persona1, persona2, persona3]:
        mayor = persona.es_mayor_de_edad()
        estado = "✅ Mayor de edad" if mayor else "❌ Menor de edad"
        print(f"   {persona.nombre:<20} ({persona.edad} años) → {estado}")
    
    # EJERCICIO PLUS: Comparación de edades
    print(f"\n⚖️ 6. COMPARACIÓN DE EDADES (EJERCICIO PLUS)")
    print("-" * 50)
    
    comparacion1 = persona1.comparar_edad_con(persona2)
    print(f"   {comparacion1}")
    
    comparacion2 = persona2.comparar_edad_con(persona3)
    print(f"   {comparacion2}")
    
    comparacion3 = Persona.comparar_dos_personas(persona1, persona3)
    print(f"   {comparacion3}")
    
    # Funcionalidades adicionales
    print(f"\n🌟 7. FUNCIONALIDADES ADICIONALES")
    print("-" * 40)
    
    print(f"📅 Año de nacimiento de {persona1.nombre}: {persona1.calcular_año_nacimiento()}")
    print(f"🏷️ Categoría de edad: {persona1.obtener_categoria_edad()}")
    print(f"🌍 Generación: {persona1.obtener_generacion()}")
    
    # Estadísticas generales
    print(f"\n📊 8. ESTADÍSTICAS GENERALES")
    print("-" * 35)
    
    stats = Persona.obtener_estadisticas_generales()
    print(f"   👥 Total personas creadas: {stats['total_personas']}")
    print(f"   📈 Edad promedio: {stats['edad_promedio']:.1f} años")
    print(f"   🔝 Edad máxima: {stats['edad_maxima']} años")
    print(f"   🔻 Edad mínima: {stats['edad_minima']} años")
    print(f"   📧 Correos válidos: {stats['correos_validos']}/{stats['total_personas']} ({stats['porcentaje_correos_validos']:.1f}%)")
    print(f"   🔞 Mayores de edad: {stats['mayores_de_edad']}/{stats['total_personas']} ({stats['porcentaje_mayores_edad']:.1f}%)")


def crear_persona_interactiva():
    """
    Función para crear una persona de forma interactiva.
    
    Returns:
        Persona: Nueva instancia de Persona o None si se cancela
    """
    print(f"\n➕ CREAR NUEVA PERSONA")
    print("=" * 30)
    
    try:
        # Solicitar datos
        print("Ingresa los datos de la nueva persona:")
        
        nombre = input("👤 Nombre completo: ").strip()
        if not nombre:
            print("❌ Operación cancelada")
            return None
        
        edad_str = input("🎂 Edad: ").strip()
        if not edad_str:
            print("❌ Operación cancelada")
            return None
        
        try:
            edad = int(edad_str)
        except ValueError:
            print("❌ La edad debe ser un número entero")
            return None
        
        correo = input("📧 Correo electrónico: ").strip()
        if not correo:
            print("❌ Operación cancelada")
            return None
        
        # Crear persona
        persona = Persona(nombre, edad, correo)
        
        print(f"\n✅ Persona creada exitosamente:")
        persona.mostrar_datos()
        
        return persona
        
    except ValueError as e:
        print(f"❌ Error al crear persona: {e}")
        return None
    except KeyboardInterrupt:
        print(f"\n❌ Operación cancelada por el usuario")
        return None


def menu_principal():
    """
    Menú principal para interactuar con la clase Persona.
    """
    personas = []
    
    while True:
        print(f"\n" + "="*50)
        print("👥 SISTEMA DE GESTIÓN DE PERSONAS")
        print("🎓 Clase 05 - Programación Orientada a Objetos")
        print("="*50)
        print("Selecciona una opción:")
        print("1. 🎬 Demo completa de la clase Persona")
        print("2. ➕ Crear nueva persona")
        print("3. 👁️ Mostrar todas las personas")
        print("4. 🔍 Buscar persona por nombre")
        print("5. 🔄 Actualizar datos de una persona")
        print("6. ⚖️ Comparar edades de dos personas")
        print("7. 📊 Ver estadísticas generales")
        print("8. 💾 Exportar personas a JSON")
        print("9. 📥 Importar personas desde JSON")
        print("0. 🚪 Salir")
        print("-" * 50)
        
        try:
            opcion = input("👉 Ingresa tu opción (0-9): ").strip()
            
            if opcion == "0":
                print("👋 ¡Gracias por usar el sistema de gestión de personas!")
                break
            elif opcion == "1":
                demo_clase_persona()
            elif opcion == "2":
                persona = crear_persona_interactiva()
                if persona:
                    personas.append(persona)
            elif opcion == "3":
                if not personas:
                    print("📋 No hay personas registradas")
                else:
                    print(f"\n👥 PERSONAS REGISTRADAS ({len(personas)}):")
                    for i, persona in enumerate(personas, 1):
                        print(f"{i}. {persona}")
            elif opcion == "4":
                if not personas:
                    print("📋 No hay personas registradas")
                else:
                    nombre_buscar = input("🔍 Ingresa el nombre a buscar: ").strip().lower()
                    encontradas = [p for p in personas if nombre_buscar in p.nombre.lower()]
                    
                    if encontradas:
                        print(f"✅ Se encontraron {len(encontradas)} persona(s):")
                        for persona in encontradas:
                            persona.mostrar_datos()
                            print("-" * 30)
                    else:
                        print("❌ No se encontraron personas con ese nombre")
            elif opcion == "5":
                if not personas:
                    print("📋 No hay personas registradas")
                else:
                    print("Selecciona la persona a actualizar:")
                    for i, persona in enumerate(personas, 1):
                        print(f"{i}. {persona.nombre}")
                    
                    try:
                        indice = int(input("Número: ")) - 1
                        if 0 <= indice < len(personas):
                            persona = personas[indice]
                            print(f"Actualizando datos de {persona.nombre}")
                            
                            nuevo_nombre = input(f"Nuevo nombre (actual: {persona.nombre}): ").strip()
                            nueva_edad = input(f"Nueva edad (actual: {persona.edad}): ").strip()
                            nuevo_correo = input(f"Nuevo correo (actual: {persona.correo_electronico}): ").strip()
                            
                            persona.actualizar_datos(
                                nombre=nuevo_nombre if nuevo_nombre else None,
                                edad=int(nueva_edad) if nueva_edad else None,
                                correo_electronico=nuevo_correo if nuevo_correo else None
                            )
                        else:
                            print("❌ Número inválido")
                    except ValueError:
                        print("❌ Ingresa un número válido")
            elif opcion == "6":
                if len(personas) < 2:
                    print("❌ Necesitas al menos 2 personas para comparar")
                else:
                    print("Selecciona la primera persona:")
                    for i, persona in enumerate(personas, 1):
                        print(f"{i}. {persona.nombre} ({persona.edad} años)")
                    
                    try:
                        indice1 = int(input("Primera persona: ")) - 1
                        indice2 = int(input("Segunda persona: ")) - 1
                        
                        if 0 <= indice1 < len(personas) and 0 <= indice2 < len(personas):
                            if indice1 != indice2:
                                resultado = personas[indice1].comparar_edad_con(personas[indice2])
                                print(f"⚖️ {resultado}")
                            else:
                                print("❌ Debes seleccionar dos personas diferentes")
                        else:
                            print("❌ Números inválidos")
                    except ValueError:
                        print("❌ Ingresa números válidos")
            elif opcion == "7":
                if Persona.personas_creadas:
                    stats = Persona.obtener_estadisticas_generales()
                    print(f"\n📊 ESTADÍSTICAS GENERALES:")
                    for key, value in stats.items():
                        if isinstance(value, float):
                            print(f"   {key}: {value:.2f}")
                        else:
                            print(f"   {key}: {value}")
                else:
                    print("📋 No hay datos para mostrar estadísticas")
            elif opcion == "8":
                if not personas:
                    print("📋 No hay personas para exportar")
                else:
                    try:
                        datos = [persona.to_dict() for persona in personas]
                        with open("personas.json", "w", encoding="utf-8") as archivo:
                            json.dump(datos, archivo, indent=2, ensure_ascii=False)
                        print(f"✅ {len(personas)} persona(s) exportada(s) a 'personas.json'")
                    except Exception as e:
                        print(f"❌ Error al exportar: {e}")
            elif opcion == "9":
                try:
                    with open("personas.json", "r", encoding="utf-8") as archivo:
                        datos = json.load(archivo)
                    
                    personas_importadas = []
                    for dato in datos:
                        persona = Persona.from_dict(dato)
                        personas_importadas.append(persona)
                    
                    personas.extend(personas_importadas)
                    print(f"✅ {len(personas_importadas)} persona(s) importada(s) desde 'personas.json'")
                    
                except FileNotFoundError:
                    print("❌ No se encontró el archivo 'personas.json'")
                except Exception as e:
                    print(f"❌ Error al importar: {e}")
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
    print("🎓 BOOTCAMP INGENIERÍA DE DATOS - CLASE 05")
    print("👥 Programación Orientada a Objetos (POO)")
    print("🧑‍💻 Sistema Completo de Gestión de Personas")
    
    menu_principal()