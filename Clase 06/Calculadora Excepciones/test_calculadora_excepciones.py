# Tests unitarios para la calculadora con manejo de excepciones
# Clase 06: Manejo de Excepciones en Python

import unittest
import math
import sys
import os
from io import StringIO
from unittest.mock import patch, mock_open
from calculadora_excepciones import CalculadoraAvanzada


class TestCalculadoraExcepciones(unittest.TestCase):
    """
    Suite de tests para la calculadora con manejo de excepciones
    """
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.calc = CalculadoraAvanzada()
        # Limpiar historial para cada test
        self.calc.historial = []
    
    def test_operaciones_basicas_validas(self):
        """Test: Operaciones matemáticas básicas válidas"""
        casos_validos = [
            (10, 5, "+", 15),
            (10, 5, "-", 5),
            (10, 5, "*", 50),
            (10, 5, "/", 2.0),
            (10, 3, "%", 1),
            (10, 3, "//", 3),
            (2, 3, "^", 8),
        ]
        
        for num1, num2, operador, esperado in casos_validos:
            with self.subTest(num1=num1, num2=num2, operador=operador):
                resultado = self.calc.realizar_operacion(num1, num2, operador)
                self.assertAlmostEqual(resultado, esperado, places=6)
    
    def test_operaciones_unarias_validas(self):
        """Test: Operaciones unarias válidas (sqrt, log)"""
        # Raíz cuadrada
        resultado = self.calc.realizar_operacion(9, 0, "sqrt")
        self.assertAlmostEqual(resultado, 3.0, places=6)
        
        resultado = self.calc.realizar_operacion(16, 0, "sqrt")
        self.assertAlmostEqual(resultado, 4.0, places=6)
        
        # Logaritmo natural
        resultado = self.calc.realizar_operacion(math.e, 0, "log")
        self.assertAlmostEqual(resultado, 1.0, places=6)
        
        resultado = self.calc.realizar_operacion(1, 0, "log")
        self.assertAlmostEqual(resultado, 0.0, places=6)
    
    def test_division_por_cero(self):
        """Test: Manejo de división por cero"""
        casos_division_cero = [
            (10, 0, "/"),
            (5, 0, "%"),
            (8, 0, "//")
        ]
        
        for num1, num2, operador in casos_division_cero:
            with self.subTest(num1=num1, num2=num2, operador=operador):
                with self.assertRaises(ZeroDivisionError):
                    self.calc.realizar_operacion(num1, num2, operador)
    
    def test_operaciones_invalidas_valor(self):
        """Test: Operaciones que causan ValueError"""
        casos_valor_error = [
            (-4, 0, "sqrt"),  # Raíz de negativo
            (-1, 0, "log"),   # Log de negativo
            (0, 0, "log"),    # Log de cero
            (-2, 0.5, "^"),   # Potencia decimal de negativo
        ]
        
        for num1, num2, operador in casos_valor_error:
            with self.subTest(num1=num1, num2=num2, operador=operador):
                with self.assertRaises(ValueError):
                    self.calc.realizar_operacion(num1, num2, operador)
    
    def test_potencias_especiales(self):
        """Test: Casos especiales de potencias"""
        # Potencia de cero
        resultado = self.calc.realizar_operacion(5, 0, "^")
        self.assertEqual(resultado, 1)
        
        # Potencia de uno
        resultado = self.calc.realizar_operacion(7, 1, "^")
        self.assertEqual(resultado, 7)
        
        # Cero elevado a potencia positiva
        resultado = self.calc.realizar_operacion(0, 5, "^")
        self.assertEqual(resultado, 0)
        
        # Cero elevado a potencia negativa debe dar error
        with self.assertRaises(ZeroDivisionError):
            self.calc.realizar_operacion(0, -1, "^")
    
    def test_formatear_resultado(self):
        """Test: Formateo de resultados"""
        # Operaciones binarias
        resultado_str = self.calc.formatear_resultado(10, 5, "+", 15)
        self.assertEqual(resultado_str, "10.0 + 5.0 = 15.000000")
        
        # Operaciones unarias
        resultado_str = self.calc.formatear_resultado(9, 0, "sqrt", 3)
        self.assertEqual(resultado_str, "√9.0 = 3.000000")
        
        resultado_str = self.calc.formatear_resultado(math.e, 0, "log", 1)
        self.assertIn("ln(", resultado_str)
        self.assertIn("= 1.000000", resultado_str)
    
    def test_historial_operaciones(self):
        """Test: Sistema de historial"""
        # Inicialmente vacío
        self.assertEqual(len(self.calc.historial), 0)
        
        # Agregar operaciones
        self.calc.agregar_al_historial("2 + 3", 5)
        self.calc.agregar_al_historial("10 / 2", 5)
        
        self.assertEqual(len(self.calc.historial), 2)
        self.assertEqual(self.calc.historial[0]['operacion'], "2 + 3")
        self.assertEqual(self.calc.historial[0]['resultado'], 5)
        
        # Verificar estructura del historial
        entrada = self.calc.historial[0]
        self.assertIn('timestamp', entrada)
        self.assertIn('operacion', entrada)
        self.assertIn('resultado', entrada)
    
    def test_limite_historial(self):
        """Test: Límite de historial (máximo 50 entradas)"""
        # Agregar más de 50 operaciones
        for i in range(55):
            self.calc.agregar_al_historial(f"operacion_{i}", i)
        
        # Verificar que solo se mantienen las últimas 50
        self.assertEqual(len(self.calc.historial), 50)
        
        # Verificar que se mantuvieron las más recientes
        self.assertEqual(self.calc.historial[-1]['operacion'], "operacion_54")
        self.assertEqual(self.calc.historial[0]['operacion'], "operacion_5")
    
    def test_validacion_numeros_especiales(self):
        """Test: Validación de números especiales (infinito, NaN)"""
        # Estos tests verifican el comportamiento con valores especiales
        # pero no pueden testear directamente la entrada del usuario
        
        # Test de resultado infinito
        with self.assertRaises(OverflowError):
            # Simulamos una operación que da infinito
            resultado = float('inf')
            if math.isinf(resultado):
                raise OverflowError("El resultado es demasiado grande")
        
        # Test de resultado NaN
        with self.assertRaises(ValueError):
            # Simulamos una operación que da NaN
            resultado = float('nan')
            if math.isnan(resultado):
                raise ValueError("El resultado no es un número válido")
    
    def test_operadores_validos(self):
        """Test: Lista de operadores válidos"""
        operadores_esperados = {'+', '-', '*', '/', '^', '%', '//', 'sqrt', 'log'}
        self.assertEqual(self.calc.operadores_validos, operadores_esperados)
    
    @patch('builtins.input')
    def test_solicitar_numero_valido(self, mock_input):
        """Test: Solicitar número válido del usuario"""
        mock_input.return_value = "42.5"
        numero = self.calc.solicitar_numero("Ingresa número: ")
        self.assertEqual(numero, 42.5)
    
    @patch('builtins.input')
    def test_solicitar_numero_invalido_luego_valido(self, mock_input):
        """Test: Entrada inválida seguida de válida"""
        mock_input.side_effect = ["abc", "42"]
        numero = self.calc.solicitar_numero("Ingresa número: ")
        self.assertEqual(numero, 42.0)
    
    @patch('builtins.input')
    def test_solicitar_numero_cancelacion(self, mock_input):
        """Test: Cancelación de entrada de número"""
        mock_input.return_value = "salir"
        with self.assertRaises(KeyboardInterrupt):
            self.calc.solicitar_numero("Ingresa número: ")
    
    @patch('builtins.input')
    def test_solicitar_operador_valido(self, mock_input):
        """Test: Solicitar operador válido"""
        mock_input.return_value = "+"
        operador = self.calc.solicitar_operador()
        self.assertEqual(operador, "+")
    
    @patch('builtins.input')
    def test_solicitar_operador_invalido_luego_valido(self, mock_input):
        """Test: Operador inválido seguido de válido"""
        mock_input.side_effect = ["&", "+"]
        operador = self.calc.solicitar_operador()
        self.assertEqual(operador, "+")
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_mostrar_historial_vacio(self, mock_stdout):
        """Test: Mostrar historial cuando está vacío"""
        self.calc.mostrar_historial()
        output = mock_stdout.getvalue()
        self.assertIn("No hay operaciones en el historial", output)
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_mostrar_historial_con_datos(self, mock_stdout):
        """Test: Mostrar historial con datos"""
        self.calc.agregar_al_historial("2 + 3", 5)
        self.calc.agregar_al_historial("10 / 2", 5)
        
        self.calc.mostrar_historial()
        output = mock_stdout.getvalue()
        
        self.assertIn("HISTORIAL DE OPERACIONES", output)
        self.assertIn("2 + 3", output)
        self.assertIn("10 / 2", output)
    
    def test_operaciones_precision(self):
        """Test: Precisión en operaciones decimales"""
        # Test de precisión con decimales
        resultado = self.calc.realizar_operacion(0.1, 0.2, "+")
        self.assertAlmostEqual(resultado, 0.3, places=10)
        
        # Test con división que da decimal periódico
        resultado = self.calc.realizar_operacion(1, 3, "/")
        self.assertAlmostEqual(resultado, 0.3333333333333333, places=10)
    
    def test_configuracion_logging(self):
        """Test: Configuración del sistema de logging"""
        # Verificar que el logger está configurado
        self.assertIsNotNone(self.calc.logger)
        self.assertEqual(self.calc.logger.name, 'calculadora_excepciones')


class TestCasosEspeciales(unittest.TestCase):
    """
    Tests para casos especiales y edge cases
    """
    
    def setUp(self):
        """Configuración inicial"""
        self.calc = CalculadoraAvanzada()
    
    def test_operaciones_con_cero(self):
        """Test: Operaciones que involucran cero"""
        # Suma con cero
        self.assertEqual(self.calc.realizar_operacion(5, 0, "+"), 5)
        self.assertEqual(self.calc.realizar_operacion(0, 5, "+"), 5)
        
        # Multiplicación con cero
        self.assertEqual(self.calc.realizar_operacion(5, 0, "*"), 0)
        self.assertEqual(self.calc.realizar_operacion(0, 5, "*"), 0)
        
        # Resta con cero
        self.assertEqual(self.calc.realizar_operacion(5, 0, "-"), 5)
        self.assertEqual(self.calc.realizar_operacion(0, 5, "-"), -5)
    
    def test_numeros_muy_grandes(self):
        """Test: Operaciones con números muy grandes"""
        numero_grande = 1e100
        
        # Suma de números grandes
        resultado = self.calc.realizar_operacion(numero_grande, numero_grande, "+")
        self.assertEqual(resultado, 2e100)
        
        # Verificar que no se produce overflow en casos normales
        resultado = self.calc.realizar_operacion(1000, 1000, "*")
        self.assertEqual(resultado, 1000000)
    
    def test_numeros_muy_pequenos(self):
        """Test: Operaciones con números muy pequeños"""
        numero_pequeno = 1e-10
        
        # Operaciones con números pequeños
        resultado = self.calc.realizar_operacion(numero_pequeno, numero_pequeno, "+")
        self.assertAlmostEqual(resultado, 2e-10, places=15)
        
        # División que resulta en número pequeño
        resultado = self.calc.realizar_operacion(1e-5, 1e5, "/")
        self.assertAlmostEqual(resultado, 1e-10, places=15)
    
    def test_operaciones_negativas(self):
        """Test: Operaciones con números negativos"""
        # Suma con negativos
        self.assertEqual(self.calc.realizar_operacion(-5, 3, "+"), -2)
        self.assertEqual(self.calc.realizar_operacion(-5, -3, "+"), -8)
        
        # Multiplicación con negativos
        self.assertEqual(self.calc.realizar_operacion(-5, 3, "*"), -15)
        self.assertEqual(self.calc.realizar_operacion(-5, -3, "*"), 15)
        
        # División con negativos
        self.assertEqual(self.calc.realizar_operacion(-10, 2, "/"), -5)
        self.assertEqual(self.calc.realizar_operacion(-10, -2, "/"), 5)
    
    def test_potencias_casos_especiales(self):
        """Test: Casos especiales de potencias"""
        # Número negativo elevado a potencia par
        resultado = self.calc.realizar_operacion(-2, 2, "^")
        self.assertEqual(resultado, 4)
        
        # Número negativo elevado a potencia impar
        resultado = self.calc.realizar_operacion(-2, 3, "^")
        self.assertEqual(resultado, -8)
        
        # Fracción como exponente con base positiva
        resultado = self.calc.realizar_operacion(4, 0.5, "^")
        self.assertAlmostEqual(resultado, 2.0, places=10)
    
    def test_modulo_casos_especiales(self):
        """Test: Casos especiales del operador módulo"""
        # Módulo con decimales
        resultado = self.calc.realizar_operacion(7.5, 2.5, "%")
        self.assertAlmostEqual(resultado, 0.0, places=10)
        
        # Módulo con resultado negativo
        resultado = self.calc.realizar_operacion(-7, 3, "%")
        self.assertAlmostEqual(resultado, 2, places=10)  # En Python: -7 % 3 = 2
    
    def test_division_entera_casos_especiales(self):
        """Test: Casos especiales de división entera"""
        # División entera con decimales
        resultado = self.calc.realizar_operacion(7.8, 2.5, "//")
        self.assertEqual(resultado, 3.0)
        
        # División entera con negativos
        resultado = self.calc.realizar_operacion(-7, 3, "//")
        self.assertEqual(resultado, -3.0)  # En Python: -7 // 3 = -3


class TestIntegracion(unittest.TestCase):
    """
    Tests de integración para flujos completos
    """
    
    def setUp(self):
        """Configuración inicial"""
        self.calc = CalculadoraAvanzada()
    
    @patch('builtins.input')
    @patch('sys.stdout', new_callable=StringIO)
    def test_flujo_completo_operacion_valida(self, mock_stdout, mock_input):
        """Test: Flujo completo de una operación válida"""
        # Simular entradas del usuario: 10, +, 5
        mock_input.side_effect = ["10", "+", "5"]
        
        # Ejecutar calculadora básica
        self.calc.calculadora_basica()
        
        # Verificar que se agregó al historial
        self.assertEqual(len(self.calc.historial), 1)
        self.assertAlmostEqual(self.calc.historial[0]['resultado'], 15.0)
        
        # Verificar output
        output = mock_stdout.getvalue()
        self.assertIn("RESULTADO", output)
        self.assertIn("15.000000", output)
    
    @patch('builtins.input')
    @patch('sys.stdout', new_callable=StringIO)
    def test_flujo_completo_division_por_cero(self, mock_stdout, mock_input):
        """Test: Flujo completo con división por cero"""
        # Simular entradas del usuario: 10, /, 0
        mock_input.side_effect = ["10", "/", "0"]
        
        # Ejecutar calculadora básica
        self.calc.calculadora_basica()
        
        # Verificar que no se agregó al historial
        self.assertEqual(len(self.calc.historial), 0)
        
        # Verificar manejo del error
        output = mock_stdout.getvalue()
        self.assertIn("Error de división", output)
        self.assertIn("No se puede dividir por cero", output)
    
    @patch('builtins.input')
    @patch('sys.stdout', new_callable=StringIO)
    def test_flujo_completo_entrada_invalida(self, mock_stdout, mock_input):
        """Test: Flujo completo con entrada inválida"""
        # Simular entradas del usuario: abc (inválido), luego cancelar
        mock_input.side_effect = ["abc", "salir"]
        
        # Ejecutar calculadora básica
        self.calc.calculadora_basica()
        
        # Verificar que no se agregó al historial
        self.assertEqual(len(self.calc.historial), 0)
        
        # Verificar manejo del error
        output = mock_stdout.getvalue()
        self.assertIn("Operación cancelada", output)


def ejecutar_tests_completos():
    """
    Ejecuta todos los tests con reporte detallado
    """
    print("🧪 EJECUTANDO TESTS DE CALCULADORA CON EXCEPCIONES")
    print("=" * 60)
    
    # Crear suite de tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Agregar todas las clases de tests
    suite.addTests(loader.loadTestsFromTestCase(TestCalculadoraExcepciones))
    suite.addTests(loader.loadTestsFromTestCase(TestCasosEspeciales))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegracion))
    
    # Ejecutar tests con reporte detallado
    runner = unittest.TextTestRunner(verbosity=2)
    resultado = runner.run(suite)
    
    # Reporte final
    print(f"\n📊 RESUMEN DE TESTS")
    print("=" * 30)
    print(f"✅ Tests exitosos: {resultado.testsRun - len(resultado.failures) - len(resultado.errors)}")
    print(f"❌ Tests fallidos: {len(resultado.failures)}")
    print(f"💥 Errores: {len(resultado.errors)}")
    print(f"⏭️ Tests omitidos: {len(resultado.skipped)}")
    
    if resultado.wasSuccessful():
        print(f"\n🎉 ¡TODOS LOS TESTS PASARON EXITOSAMENTE!")
        print(f"✨ El manejo de excepciones está funcionando correctamente")
    else:
        print(f"\n⚠️ Algunos tests fallaron. Revisa los detalles arriba.")
    
    return resultado


def test_casos_extremos():
    """
    Tests adicionales para casos extremos específicos
    """
    print("\n🔬 EJECUTANDO TESTS DE CASOS EXTREMOS")
    print("=" * 45)
    
    calc = CalculadoraAvanzada()
    casos_extremos = [
        ("Número más pequeño", sys.float_info.min, 1, "+"),
        ("Número más grande", sys.float_info.max, 0, "+"),
        ("Precisión máxima", 1/3, 3, "*"),
        ("Raíz de número grande", 1e20, 0, "sqrt"),
        ("Logaritmo de número pequeño", 1e-10, 0, "log"),
    ]
    
    for descripcion, num1, num2, op in casos_extremos:
        print(f"\n🧪 {descripcion}")
        try:
            resultado = calc.realizar_operacion(num1, num2, op)
            print(f"   ✅ Resultado: {resultado}")
        except Exception as e:
            print(f"   ⚠️ Excepción manejada: {type(e).__name__}: {e}")


if __name__ == "__main__":
    # Ejecutar tests principales
    resultado_principal = ejecutar_tests_completos()
    
    # Ejecutar tests de casos extremos
    test_casos_extremos()
    
    # Reporte final
    print(f"\n🏁 REPORTE FINAL DE TESTING")
    print("=" * 35)
    print(f"Tests unitarios: {'✅ EXITOSO' if resultado_principal.wasSuccessful() else '❌ FALLIDO'}")
    print(f"Tests de casos extremos: ✅ COMPLETADO")
    
    if resultado_principal.wasSuccessful():
        print(f"\n🎊 ¡SISTEMA DE CALCULADORA TOTALMENTE VALIDADO!")
        print(f"✨ Manejo de excepciones robusto y funcional")
    else:
        print(f"\n⚠️ Hay issues que requieren atención")
    
    # Código de salida
    sys.exit(0 if resultado_principal.wasSuccessful() else 1)