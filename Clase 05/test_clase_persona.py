# Tests unitarios para la clase Persona
# Clase 05: Programación Orientada a Objetos (POO)

import unittest
import sys
import os
from io import StringIO
from clase_persona import Persona


class TestClasePersona(unittest.TestCase):
    """
    Suite de tests para la clase Persona
    """
    
    def setUp(self):
        """Configuración inicial para cada test"""
        # Limpiar el contador de personas para cada test
        Persona.contador_personas = 0
        Persona.personas_creadas = []
        
        # Datos de prueba válidos
        self.nombre_valido = "Ana García López"
        self.edad_valida = 25
        self.correo_valido = "ana.garcia@email.com"
    
    def test_crear_persona_valida(self):
        """Test: Crear persona con datos válidos"""
        persona = Persona(self.nombre_valido, self.edad_valida, self.correo_valido)
        
        self.assertEqual(persona.nombre, self.nombre_valido)
        self.assertEqual(persona.edad, self.edad_valida)
        self.assertEqual(persona.correo_electronico, self.correo_valido)
        self.assertEqual(persona.id_persona, 1)
        self.assertEqual(Persona.contador_personas, 1)
    
    def test_validacion_nombre(self):
        """Test: Validación de nombres"""
        # Nombres válidos
        nombres_validos = [
            "Ana García",
            "José María Pérez",
            "María José",
            "Carlos Alberto"
        ]
        
        for nombre in nombres_validos:
            persona = Persona(nombre, self.edad_valida, self.correo_valido)
            self.assertEqual(persona.nombre, nombre)
        
        # Nombres inválidos
        nombres_invalidos = [
            "",  # Vacío
            "   ",  # Solo espacios
            "A",  # Muy corto
            "Ana123",  # Con números
            "Ana@García",  # Con símbolos
            None  # None
        ]
        
        for nombre in nombres_invalidos:
            with self.assertRaises(ValueError):
                Persona(nombre, self.edad_valida, self.correo_valido)
    
    def test_validacion_edad(self):
        """Test: Validación de edades"""
        # Edades válidas
        edades_validas = [0, 1, 18, 25, 65, 100, 150]
        
        for edad in edades_validas:
            persona = Persona(self.nombre_valido, edad, self.correo_valido)
            self.assertEqual(persona.edad, edad)
        
        # Edades inválidas
        edades_invalidas = [-1, -10, 151, 200, "25", None, 25.5]
        
        for edad in edades_invalidas:
            with self.assertRaises(ValueError):
                Persona(self.nombre_valido, edad, self.correo_valido)
    
    def test_validacion_correo(self):
        """Test: Validación de correos electrónicos"""
        # Correos válidos
        correos_validos = [
            "test@ejemplo.com",
            "usuario.nombre@dominio.org",
            "test+tag@ejemplo.net",
            "usuario123@test123.com",
            "a@b.co"
        ]
        
        persona = Persona(self.nombre_valido, self.edad_valida, "temp@temp.com")
        
        for correo in correos_validos:
            persona.correo_electronico = correo
            self.assertTrue(persona.validar_correo(), f"Correo debería ser válido: {correo}")
        
        # Correos inválidos
        correos_invalidos = [
            "correo_sin_arroba",
            "correo@",
            "@dominio.com",
            "correo@@ejemplo.com",
            "correo.ejemplo.com",
            "correo@ejemplo",
            "",
            None
        ]
        
        for correo in correos_invalidos:
            persona.correo_electronico = correo
            self.assertFalse(persona.validar_correo(), f"Correo debería ser inválido: {correo}")
    
    def test_crear_persona_correo_invalido(self):
        """Test: No se debe poder crear persona con correo inválido"""
        with self.assertRaises(ValueError):
            Persona(self.nombre_valido, self.edad_valida, "correo_invalido")
    
    def test_actualizar_datos(self):
        """Test: Actualización de datos"""
        persona = Persona(self.nombre_valido, self.edad_valida, self.correo_valido)
        
        # Actualizar nombre
        nuevo_nombre = "Ana García Rodríguez"
        cambios = persona.actualizar_datos(nombre=nuevo_nombre)
        self.assertEqual(persona.nombre, nuevo_nombre)
        self.assertIn('nombre', cambios)
        
        # Actualizar edad
        nueva_edad = 26
        cambios = persona.actualizar_datos(edad=nueva_edad)
        self.assertEqual(persona.edad, nueva_edad)
        self.assertIn('edad', cambios)
        
        # Actualizar correo válido
        nuevo_correo = "ana.nueva@email.com"
        cambios = persona.actualizar_datos(correo_electronico=nuevo_correo)
        self.assertEqual(persona.correo_electronico, nuevo_correo)
        self.assertIn('correo_electronico', cambios)
        
        # Intentar actualizar con correo inválido
        correo_original = persona.correo_electronico
        cambios = persona.actualizar_datos(correo_electronico="correo_invalido")
        self.assertEqual(persona.correo_electronico, correo_original)  # No debe cambiar
        self.assertEqual(cambios, {})  # No debe haber cambios
    
    def test_es_mayor_de_edad(self):
        """Test: Verificación de mayoría de edad"""
        # Menor de edad
        persona_menor = Persona(self.nombre_valido, 17, self.correo_valido)
        self.assertFalse(persona_menor.es_mayor_de_edad())
        
        # Exactamente 18 años
        persona_18 = Persona(self.nombre_valido, 18, self.correo_valido)
        self.assertTrue(persona_18.es_mayor_de_edad())
        
        # Mayor de edad
        persona_mayor = Persona(self.nombre_valido, 25, self.correo_valido)
        self.assertTrue(persona_mayor.es_mayor_de_edad())
    
    def test_comparar_edad_con(self):
        """Test: Comparación de edades (Ejercicio PLUS)"""
        persona1 = Persona("Ana García", 25, "ana@email.com")
        persona2 = Persona("Carlos Pérez", 30, "carlos@email.com")
        persona3 = Persona("María López", 25, "maria@email.com")
        
        # Persona1 menor que persona2
        resultado = persona1.comparar_edad_con(persona2)
        self.assertIn("Carlos Pérez es mayor que Ana García", resultado)
        self.assertIn("5 año(s)", resultado)
        
        # Persona2 mayor que persona1
        resultado = persona2.comparar_edad_con(persona1)
        self.assertIn("Carlos Pérez es mayor que Ana García", resultado)
        
        # Misma edad
        resultado = persona1.comparar_edad_con(persona3)
        self.assertIn("tienen la misma edad", resultado)
        
        # Error al comparar con tipo incorrecto
        with self.assertRaises(ValueError):
            persona1.comparar_edad_con("no es una persona")
    
    def test_metodo_comparar_dos_personas(self):
        """Test: Método de clase para comparar dos personas"""
        persona1 = Persona("Ana García", 25, "ana@email.com")
        persona2 = Persona("Carlos Pérez", 30, "carlos@email.com")
        
        resultado = Persona.comparar_dos_personas(persona1, persona2)
        self.assertIn("Carlos Pérez es mayor que Ana García", resultado)
    
    def test_obtener_categoria_edad(self):
        """Test: Categorización por edad"""
        casos = [
            (5, "Niño/a"),
            (12, "Niño/a"),
            (15, "Adolescente"),
            (17, "Adolescente"),
            (20, "Joven Adulto"),
            (29, "Joven Adulto"),
            (35, "Adulto"),
            (59, "Adulto"),
            (65, "Adulto Mayor"),
            (80, "Adulto Mayor")
        ]
        
        for edad, categoria_esperada in casos:
            persona = Persona(self.nombre_valido, edad, self.correo_valido)
            self.assertEqual(persona.obtener_categoria_edad(), categoria_esperada)
    
    def test_calcular_año_nacimiento(self):
        """Test: Cálculo de año de nacimiento"""
        from datetime import datetime
        año_actual = datetime.now().year
        
        persona = Persona(self.nombre_valido, 25, self.correo_valido)
        año_nacimiento = persona.calcular_año_nacimiento()
        self.assertEqual(año_nacimiento, año_actual - 25)
    
    def test_obtener_generacion(self):
        """Test: Determinación de generación"""
        from datetime import datetime
        año_actual = datetime.now().year
        
        # Casos aproximados (puede variar según el año actual)
        casos_generacion = [
            (20, "Generación Z"),  # Nacido ~2004
            (30, "Millennial"),    # Nacido ~1994
            (45, "Generación X"),  # Nacido ~1979
            (60, "Baby Boomer"),   # Nacido ~1964
            (80, "Generación Silenciosa")  # Nacido ~1944
        ]
        
        for edad, _ in casos_generacion:
            persona = Persona(self.nombre_valido, edad, self.correo_valido)
            generacion = persona.obtener_generacion()
            self.assertIsInstance(generacion, str)
            self.assertGreater(len(generacion), 0)
    
    def test_to_dict(self):
        """Test: Conversión a diccionario"""
        persona = Persona(self.nombre_valido, self.edad_valida, self.correo_valido)
        datos = persona.to_dict()
        
        campos_esperados = [
            'id', 'nombre', 'edad', 'correo_electronico', 
            'es_mayor_de_edad', 'categoria_edad', 'año_nacimiento', 
            'generacion', 'fecha_creacion'
        ]
        
        for campo in campos_esperados:
            self.assertIn(campo, datos)
        
        self.assertEqual(datos['nombre'], self.nombre_valido)
        self.assertEqual(datos['edad'], self.edad_valida)
        self.assertEqual(datos['correo_electronico'], self.correo_valido)
    
    def test_from_dict(self):
        """Test: Creación desde diccionario"""
        datos = {
            'nombre': self.nombre_valido,
            'edad': self.edad_valida,
            'correo_electronico': self.correo_valido
        }
        
        persona = Persona.from_dict(datos)
        self.assertEqual(persona.nombre, self.nombre_valido)
        self.assertEqual(persona.edad, self.edad_valida)
        self.assertEqual(persona.correo_electronico, self.correo_valido)
    
    def test_estadisticas_generales(self):
        """Test: Estadísticas generales de la clase"""
        # Sin personas
        stats = Persona.obtener_estadisticas_generales()
        self.assertIn("mensaje", stats)
        
        # Con personas
        persona1 = Persona("Ana García", 25, "ana@email.com")
        persona2 = Persona("Carlos Pérez", 30, "carlos@email.com")
        persona3 = Persona("María López", 17, "maria@email.com")
        
        stats = Persona.obtener_estadisticas_generales()
        
        self.assertEqual(stats['total_personas'], 3)
        self.assertAlmostEqual(stats['edad_promedio'], (25 + 30 + 17) / 3)
        self.assertEqual(stats['edad_minima'], 17)
        self.assertEqual(stats['edad_maxima'], 30)
        self.assertEqual(stats['mayores_de_edad'], 2)
    
    def test_metodos_especiales(self):
        """Test: Métodos especiales (__str__, __repr__, __eq__, __lt__)"""
        persona1 = Persona("Ana García", 25, "ana@email.com")
        persona2 = Persona("Ana García", 25, "ana@email.com")
        persona3 = Persona("Carlos Pérez", 30, "carlos@email.com")
        
        # __str__
        str_persona = str(persona1)
        self.assertIn("Ana García", str_persona)
        self.assertIn("25", str_persona)
        
        # __repr__
        repr_persona = repr(persona1)
        self.assertIn("Persona(", repr_persona)
        
        # __eq__
        self.assertEqual(persona1, persona2)  # Mismos datos
        self.assertNotEqual(persona1, persona3)  # Datos diferentes
        self.assertNotEqual(persona1, "no es persona")  # Tipo diferente
        
        # __lt__
        self.assertTrue(persona1 < persona3)  # 25 < 30
        self.assertFalse(persona3 < persona1)  # 30 > 25
        
        with self.assertRaises(ValueError):
            persona1 < "no es persona"
    
    def test_dias_hasta_cumpleanos(self):
        """Test: Cálculo de días hasta cumpleaños"""
        persona = Persona(self.nombre_valido, self.edad_valida, self.correo_valido)
        
        # Test con fecha válida
        dias = persona.dias_hasta_cumpleanos("25/12")  # Navidad
        self.assertIsInstance(dias, int)
        self.assertGreaterEqual(dias, 0)
        self.assertLessEqual(dias, 365)
        
        # Test con fecha inválida
        dias_invalid = persona.dias_hasta_cumpleanos("fecha_invalida")
        self.assertIsNone(dias_invalid)
    
    def test_contador_personas(self):
        """Test: Contador de personas de clase"""
        inicial = Persona.contador_personas
        
        persona1 = Persona("Persona 1", 25, "persona1@email.com")
        self.assertEqual(Persona.contador_personas, inicial + 1)
        
        persona2 = Persona("Persona 2", 30, "persona2@email.com")
        self.assertEqual(Persona.contador_personas, inicial + 2)
        
        # Verificar que están en la lista
        self.assertIn(persona1, Persona.personas_creadas)
        self.assertIn(persona2, Persona.personas_creadas)


class TestCasosEspeciales(unittest.TestCase):
    """
    Tests para casos especiales y edge cases
    """
    
    def setUp(self):
        """Configuración inicial"""
        Persona.contador_personas = 0
        Persona.personas_creadas = []
    
    def test_nombres_con_caracteres_especiales(self):
        """Test: Nombres con caracteres especiales válidos"""
        nombres_especiales = [
            "José María",
            "María José",
            "François",
            "Sofía",
            "Ángel",
            "Niña"
        ]
        
        for nombre in nombres_especiales:
            persona = Persona(nombre, 25, "test@email.com")
            self.assertEqual(persona.nombre, nombre)
    
    def test_formateo_nombre(self):
        """Test: Formateo automático de nombres"""
        casos = [
            ("ana garcia", "Ana Garcia"),
            ("CARLOS PÉREZ", "Carlos Pérez"),
            ("mArÍa jOsÉ", "María José"),
            ("  luis   alberto  ", "Luis Alberto")
        ]
        
        for entrada, esperado in casos:
            persona = Persona(entrada, 25, "test@email.com")
            self.assertEqual(persona.nombre, esperado)
    
    def test_edades_extremas(self):
        """Test: Edades en los límites"""
        # Edad mínima
        persona_bebe = Persona("Bebé", 0, "bebe@email.com")
        self.assertEqual(persona_bebe.edad, 0)
        self.assertEqual(persona_bebe.obtener_categoria_edad(), "Niño/a")
        
        # Edad máxima
        persona_mayor = Persona("Centenario", 150, "mayor@email.com")
        self.assertEqual(persona_mayor.edad, 150)
        self.assertEqual(persona_mayor.obtener_categoria_edad(), "Adulto Mayor")
    
    def test_correos_casos_limite(self):
        """Test: Correos en casos límite"""
        persona = Persona("Test", 25, "a@b.co")  # Correo mínimo válido
        
        # Correo muy largo (pero válido)
        correo_largo = "a" * 50 + "@" + "b" * 50 + ".com"
        persona.correo_electronico = correo_largo
        self.assertTrue(persona.validar_correo())
        
        # Correo demasiado largo (inválido)
        correo_muy_largo = "a" * 200 + "@" + "b" * 100 + ".com"
        persona.correo_electronico = correo_muy_largo
        self.assertFalse(persona.validar_correo())


def ejecutar_tests():
    """
    Ejecuta todos los tests con reporte detallado
    """
    print("🧪 EJECUTANDO TESTS DE LA CLASE PERSONA")
    print("=" * 50)
    
    # Crear suite de tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Agregar clases de tests
    suite.addTests(loader.loadTestsFromTestCase(TestClasePersona))
    suite.addTests(loader.loadTestsFromTestCase(TestCasosEspeciales))
    
    # Ejecutar tests
    runner = unittest.TextTestRunner(verbosity=2)
    resultado = runner.run(suite)
    
    # Reporte final
    print(f"\n📊 RESUMEN DE TESTS")
    print("=" * 25)
    print(f"✅ Tests exitosos: {resultado.testsRun - len(resultado.failures) - len(resultado.errors)}")
    print(f"❌ Tests fallidos: {len(resultado.failures)}")
    print(f"💥 Errores: {len(resultado.errors)}")
    print(f"⏭️ Tests omitidos: {len(resultado.skipped)}")
    
    if resultado.wasSuccessful():
        print(f"\n🎉 ¡TODOS LOS TESTS PASARON EXITOSAMENTE!")
        print(f"✨ La clase Persona está funcionando correctamente")
    else:
        print(f"\n⚠️ Algunos tests fallaron. Revisa los detalles arriba.")
    
    return resultado


if __name__ == "__main__":
    # Ejecutar tests
    resultado = ejecutar_tests()
    
    # Código de salida basado en el resultado
    sys.exit(0 if resultado.wasSuccessful() else 1)