import unittest
from unittest.mock import patch
import json
import os
from analizador_financiero_base import AnalizadorFinanciero
from analizador_financiero_optimizado import AnalizadorFinancieroOptimizado


class TestAnalizadorFinancieroBase(unittest.TestCase):
    """
    Pruebas para la versión base del Analizador Financiero
    """
    
    def setUp(self):
        """Configuración inicial para cada prueba"""
        self.analizador = AnalizadorFinanciero()
        self.transacciones_test = [1000, 1500, 750, 2000, 500]
        self.categorias_test = ["Ventas", "Servicios", "Ventas", "Servicios", "Productos"]
    
    def test_calcular_total_ingresos_base(self):
        """Prueba el cálculo de total de ingresos - versión base"""
        resultado = self.analizador.calcular_total_ingresos(self.transacciones_test)
        esperado = 5750
        self.assertEqual(resultado, esperado)
        
    def test_calcular_total_ingresos_lista_vacia(self):
        """Prueba con lista vacía - versión base"""
        resultado = self.analizador.calcular_total_ingresos([])
        self.assertEqual(resultado, 0)
    
    def test_filtrar_ingresos_altos_base(self):
        """Prueba el filtrado de ingresos altos - versión base"""
        resultado = self.analizador.filtrar_ingresos_altos(self.transacciones_test, 1000)
        esperado = [1000, 1500, 2000]
        self.assertEqual(resultado, esperado)
    
    def test_filtrar_ingresos_altos_umbral_alto(self):
        """Prueba con umbral muy alto - versión base"""
        resultado = self.analizador.filtrar_ingresos_altos(self.transacciones_test, 3000)
        self.assertEqual(resultado, [])
    
    def test_agrupar_por_categoria_base(self):
        """Prueba agrupación por categoría - versión base"""
        resultado = self.analizador.agrupar_por_categoria(self.transacciones_test, self.categorias_test)
        esperado = {
            "Ventas": [1000, 750],
            "Servicios": [1500, 2000],
            "Productos": [500]
        }
        self.assertEqual(resultado, esperado)


class TestAnalizadorFinancieroOptimizado(unittest.TestCase):
    """
    Pruebas para la versión optimizada del Analizador Financiero
    """
    
    def setUp(self):
        """Configuración inicial para cada prueba"""
        self.analizador = AnalizadorFinancieroOptimizado()
        self.transacciones_test = [1000, 1500, 750, 2000, 500, 1200, 1800]
        self.categorias_test = ["Ventas", "Servicios", "Ventas", "Servicios", "Productos", "Ventas", "Servicios"]
        self.transacciones_grandes = list(range(1, 10001))  # Para pruebas de rendimiento
    
    # ================ PRUEBAS DE FUNCIONES BÁSICAS OPTIMIZADAS ================
    
    def test_calcular_total_ingresos_optimizado(self):
        """Prueba el cálculo optimizado de total de ingresos"""
        resultado = self.analizador.calcular_total_ingresos(self.transacciones_test)
        esperado = sum(self.transacciones_test)  # 9750
        self.assertEqual(resultado, esperado)
    
    def test_calcular_total_ingresos_validacion(self):
        """Prueba validaciones en cálculo de total"""
        # Lista vacía debe lanzar error
        with self.assertRaises(ValueError):
            self.analizador.calcular_total_ingresos([])
        
        # Valores no numéricos deben lanzar error
        with self.assertRaises(ValueError):
            self.analizador.calcular_total_ingresos([1000, "abc", 1500])
    
    def test_filtrar_ingresos_altos_optimizado(self):
        """Prueba el filtrado optimizado de ingresos altos"""
        resultado = self.analizador.filtrar_ingresos_altos(self.transacciones_test, 1200)
        esperado = [1500, 2000, 1800]
        self.assertEqual(resultado, esperado)
    
    def test_filtrar_ingresos_altos_tipos_datos(self):
        """Prueba filtrado con diferentes tipos de datos"""
        # Mezcla de int y float
        transacciones_mixtas = [1000, 1500.5, 750, 2000.0, 500]
        resultado = self.analizador.filtrar_ingresos_altos(transacciones_mixtas, 1000)
        esperado = [1000, 1500.5, 2000.0]
        self.assertEqual(resultado, esperado)
    
    def test_agrupar_por_categoria_optimizado(self):
        """Prueba agrupación optimizada por categoría"""
        resultado = self.analizador.agrupar_por_categoria(self.transacciones_test, self.categorias_test)
        esperado = {
            "Ventas": [1000, 750, 1200],
            "Servicios": [1500, 2000, 1800],
            "Productos": [500]
        }
        self.assertEqual(resultado, esperado)
    
    def test_agrupar_por_categoria_validacion(self):
        """Prueba validaciones en agrupación por categoría"""
        # Listas de diferente longitud deben lanzar error
        with self.assertRaises(ValueError):
            self.analizador.agrupar_por_categoria([1000, 1500], ["Ventas"])
    
    # ================ PRUEBAS DE FUNCIONES AVANZADAS CON SETS ================
    
    def test_obtener_categorias_unicas(self):
        """Prueba obtención de categorías únicas usando sets"""
        categorias_con_duplicados = ["Ventas", "Servicios", "Ventas", "Productos", "Servicios", "Ventas"]
        resultado = self.analizador.obtener_categorias_unicas(categorias_con_duplicados)
        esperado = {"Ventas", "Servicios", "Productos"}
        self.assertEqual(resultado, esperado)
    
    def test_verificar_categoria_existe(self):
        """Prueba verificación de existencia de categoría"""
        # Primero agregar categorías
        self.analizador.obtener_categorias_unicas(self.categorias_test)
        
        self.assertTrue(self.analizador.verificar_categoria_existe("Ventas"))
        self.assertTrue(self.analizador.verificar_categoria_existe("Servicios"))
        self.assertFalse(self.analizador.verificar_categoria_existe("NoExiste"))
    
    def test_encontrar_categorias_comunes(self):
        """Prueba búsqueda de categorías comunes entre listas"""
        lista1 = ["Ventas", "Servicios", "Productos"]
        lista2 = ["Servicios", "Consultoria", "Productos", "Marketing"]
        resultado = self.analizador.encontrar_categorias_comunes(lista1, lista2)
        esperado = {"Servicios", "Productos"}
        self.assertEqual(resultado, esperado)
    
    # ================ PRUEBAS DE ANÁLISIS ESTADÍSTICO ================
    
    def test_analisis_estadistico_completo(self):
        """Prueba análisis estadístico completo"""
        resultado = self.analizador.analisis_estadistico_completo(self.transacciones_test)
        
        # Verificar que contiene todas las estadísticas esperadas
        campos_esperados = ['total', 'promedio', 'mediana', 'minimo', 'maximo', 
                          'rango', 'cantidad', 'desviacion_estandar', 'varianza']
        for campo in campos_esperados:
            self.assertIn(campo, resultado)
        
        # Verificar algunos cálculos específicos
        self.assertEqual(resultado['total'], sum(self.transacciones_test))
        self.assertEqual(resultado['cantidad'], len(self.transacciones_test))
        self.assertEqual(resultado['minimo'], min(self.transacciones_test))
        self.assertEqual(resultado['maximo'], max(self.transacciones_test))
    
    def test_analisis_estadistico_lista_vacia(self):
        """Prueba análisis estadístico con lista vacía"""
        resultado = self.analizador.analisis_estadistico_completo([])
        self.assertEqual(resultado, {})
    
    def test_analisis_estadistico_un_elemento(self):
        """Prueba análisis estadístico con un solo elemento"""
        resultado = self.analizador.analisis_estadistico_completo([1000])
        
        # Con un solo elemento, no debe haber desviación estándar ni varianza
        self.assertNotIn('desviacion_estandar', resultado)
        self.assertNotIn('varianza', resultado)
        self.assertEqual(resultado['total'], 1000)
        self.assertEqual(resultado['promedio'], 1000)
    
    def test_analizar_por_categoria_avanzado(self):
        """Prueba análisis avanzado por categoría"""
        resultado = self.analizador.analizar_por_categoria_avanzado(
            self.transacciones_test, self.categorias_test
        )
        
        # Verificar que todas las categorías están presentes
        categorias_esperadas = set(self.categorias_test)
        self.assertEqual(set(resultado.keys()), categorias_esperadas)
        
        # Verificar que cada categoría tiene estadísticas completas
        for categoria, stats in resultado.items():
            self.assertIn('total', stats)
            self.assertIn('promedio', stats)
            self.assertIn('participacion_porcentual', stats)
    
    # ================ PRUEBAS DE FUNCIONES DE RENDIMIENTO ================
    
    def test_filtros_multiples_optimizado(self):
        """Prueba aplicación de múltiples filtros"""
        # Filtrar valores entre 800 y 1600
        resultado = self.analizador.filtros_multiples_optimizado(
            self.transacciones_test, 
            minimo=800, 
            maximo=1600
        )
        esperado = [1000, 1500, 1200]
        self.assertEqual(resultado, esperado)
        
        # Filtrar múltiplos de 500
        resultado_multiplos = self.analizador.filtros_multiples_optimizado(
            self.transacciones_test,
            multiplo_de=500
        )
        esperado_multiplos = [1000, 1500, 2000, 500]
        self.assertEqual(resultado_multiplos, esperado_multiplos)
    
    def test_ranking_categorias(self):
        """Prueba ranking de categorías por diferentes criterios"""
        # Ranking por total
        ranking_total = self.analizador.ranking_categorias(
            self.transacciones_test, self.categorias_test, 'total'
        )
        
        # Servicios debería estar primero (1500 + 2000 + 1800 = 5300)
        self.assertEqual(ranking_total[0][0], 'Servicios')
        
        # Ranking por cantidad
        ranking_cantidad = self.analizador.ranking_categorias(
            self.transacciones_test, self.categorias_test, 'cantidad'
        )
        
        # Servicios y Ventas deberían empatar con 3 transacciones cada uno
        primeros_dos = [item[0] for item in ranking_cantidad[:2]]
        self.assertIn('Servicios', primeros_dos)
        self.assertIn('Ventas', primeros_dos)
    
    def test_ranking_categorias_criterio_invalido(self):
        """Prueba ranking con criterio inválido"""
        with self.assertRaises(ValueError):
            self.analizador.ranking_categorias(
                self.transacciones_test, self.categorias_test, 'criterio_inexistente'
            )
    
    # ================ PRUEBAS DE HISTORIAL Y AUDITORÍA ================
    
    def test_registro_historial_analisis(self):
        """Prueba que se registre el historial de análisis"""
        # Realizar algunas operaciones
        self.analizador.calcular_total_ingresos(self.transacciones_test)
        self.analizador.filtrar_ingresos_altos(self.transacciones_test, 1000)
        
        # Verificar que se registraron en el historial
        historial = self.analizador.obtener_historial_analisis()
        self.assertGreaterEqual(len(historial), 2)
        
        # Verificar estructura del registro
        registro = historial[0]
        self.assertIn('timestamp', registro)
        self.assertIn('funcion', registro)
        self.assertIn('metadata', registro)
    
    def test_obtener_historial_analisis_limite(self):
        """Prueba límite en obtención de historial"""
        # Realizar múltiples operaciones
        for i in range(5):
            self.analizador.calcular_total_ingresos([1000 + i])
        
        # Obtener solo los últimos 3
        historial = self.analizador.obtener_historial_analisis(3)
        self.assertEqual(len(historial), 3)
    
    # ================ PRUEBAS DE EXPORTACIÓN ================
    
    def test_exportar_estadisticas(self):
        """Prueba exportación de estadísticas a JSON"""
        archivo_test = "test_estadisticas.json"
        
        try:
            self.analizador.exportar_estadisticas(
                self.transacciones_test, 
                self.categorias_test, 
                archivo_test
            )
            
            # Verificar que el archivo se creó
            self.assertTrue(os.path.exists(archivo_test))
            
            # Verificar contenido del archivo
            with open(archivo_test, 'r', encoding='utf-8') as f:
                datos = json.load(f)
            
            # Verificar estructura
            campos_esperados = ['resumen_general', 'analisis_por_categoria', 
                              'ranking_por_total', 'ranking_por_promedio',
                              'categorias_unicas', 'fecha_analisis', 'total_transacciones']
            for campo in campos_esperados:
                self.assertIn(campo, datos)
                
        finally:
            # Limpiar archivo de prueba
            if os.path.exists(archivo_test):
                os.remove(archivo_test)
    
    # ================ PRUEBAS DE RENDIMIENTO ================
    
    def test_comparacion_rendimiento_grandes_datasets(self):
        """Prueba que las funciones optimizadas manejen grandes datasets"""
        # Crear dataset grande
        transacciones_grandes = list(range(1, 50001))  # 50,000 elementos
        
        # Esto no debería tomar mucho tiempo ni fallar
        import time
        start = time.time()
        total = self.analizador.calcular_total_ingresos(transacciones_grandes)
        tiempo = time.time() - start
        
        # Verificar resultado correcto
        esperado = sum(transacciones_grandes)
        self.assertEqual(total, esperado)
        
        # El tiempo debería ser razonable (menos de 1 segundo)
        self.assertLess(tiempo, 1.0)
    
    def test_filtrado_grandes_datasets(self):
        """Prueba filtrado en datasets grandes"""
        transacciones_grandes = list(range(1, 10001))
        umbral = 5000
        
        resultado = self.analizador.filtrar_ingresos_altos(transacciones_grandes, umbral)
        
        # Verificar que todos los resultados sean mayores al umbral
        self.assertTrue(all(x > umbral for x in resultado))
        
        # Verificar cantidad esperada
        esperado_cantidad = len([x for x in transacciones_grandes if x > umbral])
        self.assertEqual(len(resultado), esperado_cantidad)


class TestComparacionRendimiento(unittest.TestCase):
    """
    Pruebas específicas para comparar rendimiento entre versiones
    """
    
    def setUp(self):
        """Configuración para pruebas de rendimiento"""
        self.analizador_base = AnalizadorFinanciero()
        self.analizador_optimizado = AnalizadorFinancieroOptimizado()
        self.transacciones_grandes = list(range(1, 10001))
        self.categorias_grandes = [f"Categoria_{i%10}" for i in range(1, 10001)]
    
    def test_rendimiento_calculo_total(self):
        """Compara rendimiento en cálculo de total"""
        import time
        
        # Versión base
        start = time.time()
        total_base = self.analizador_base.calcular_total_ingresos(self.transacciones_grandes)
        tiempo_base = time.time() - start
        
        # Versión optimizada
        start = time.time()
        total_opt = self.analizador_optimizado.calcular_total_ingresos(self.transacciones_grandes)
        tiempo_opt = time.time() - start
        
        # Los resultados deben ser iguales
        self.assertEqual(total_base, total_opt)
        
        # La versión optimizada debería ser más rápida o igual
        self.assertLessEqual(tiempo_opt, tiempo_base * 1.1)  # 10% de tolerancia
    
    def test_rendimiento_filtrado(self):
        """Compara rendimiento en filtrado"""
        import time
        
        umbral = 5000
        
        # Versión base
        start = time.time()
        filtrado_base = self.analizador_base.filtrar_ingresos_altos(self.transacciones_grandes, umbral)
        tiempo_base = time.time() - start
        
        # Versión optimizada
        start = time.time()
        filtrado_opt = self.analizador_optimizado.filtrar_ingresos_altos(self.transacciones_grandes, umbral)
        tiempo_opt = time.time() - start
        
        # Los resultados deben ser iguales
        self.assertEqual(filtrado_base, filtrado_opt)
        
        # La versión optimizada debería ser más rápida o igual
        self.assertLessEqual(tiempo_opt, tiempo_base * 1.1)


class TestCasosEspeciales(unittest.TestCase):
    """
    Pruebas para casos especiales y edge cases
    """
    
    def setUp(self):
        """Configuración para casos especiales"""
        self.analizador = AnalizadorFinancieroOptimizado()
    
    def test_valores_extremos(self):
        """Prueba con valores muy grandes y muy pequeños"""
        transacciones_extremas = [0.01, 1000000, 0.001, 999999.99]
        
        total = self.analizador.calcular_total_ingresos(transacciones_extremas)
        self.assertAlmostEqual(total, 1999999.901, places=2)
        
        # Filtrar valores grandes
        grandes = self.analizador.filtrar_ingresos_altos(transacciones_extremas, 500000)
        self.assertEqual(len(grandes), 2)
    
    def test_valores_negativos(self):
        """Prueba con valores negativos (pérdidas)"""
        transacciones_mixtas = [1000, -500, 1500, -200, 2000]
        
        total = self.analizador.calcular_total_ingresos(transacciones_mixtas)
        self.assertEqual(total, 3800)
        
        # Filtrar solo positivos
        positivos = self.analizador.filtrar_ingresos_altos(transacciones_mixtas, 0)
        self.assertEqual(positivos, [1000, 1500, 2000])
    
    def test_valores_duplicados(self):
        """Prueba con valores duplicados"""
        transacciones_duplicadas = [1000, 1000, 1500, 1500, 1500]
        categorias_duplicadas = ["A", "A", "B", "B", "B"]
        
        agrupado = self.analizador.agrupar_por_categoria(transacciones_duplicadas, categorias_duplicadas)
        
        self.assertEqual(agrupado["A"], [1000, 1000])
        self.assertEqual(agrupado["B"], [1500, 1500, 1500])
    
    def test_categoria_vacia_o_none(self):
        """Prueba con categorías vacías o None"""
        transacciones = [1000, 1500]
        categorias_problematicas = ["", "Normal"]
        
        # Esto debería funcionar, pero la categoría vacía se manejará
        agrupado = self.analizador.agrupar_por_categoria(transacciones, categorias_problematicas)
        self.assertIn("", agrupado)
        self.assertIn("Normal", agrupado)


# Función para ejecutar pruebas con reporte detallado
def ejecutar_pruebas_completas():
    """
    Ejecuta todas las pruebas y genera un reporte detallado
    """
    print("🧪 EJECUTANDO SUITE COMPLETA DE PRUEBAS")
    print("=" * 60)
    
    # Crear suite de pruebas
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Agregar todas las clases de prueba
    suite.addTests(loader.loadTestsFromTestCase(TestAnalizadorFinancieroBase))
    suite.addTests(loader.loadTestsFromTestCase(TestAnalizadorFinancieroOptimizado))
    suite.addTests(loader.loadTestsFromTestCase(TestComparacionRendimiento))
    suite.addTests(loader.loadTestsFromTestCase(TestCasosEspeciales))
    
    # Ejecutar pruebas con reporte detallado
    runner = unittest.TextTestRunner(verbosity=2)
    resultado = runner.run(suite)
    
    # Reporte final
    print(f"\n📊 RESUMEN DE PRUEBAS")
    print("=" * 30)
    print(f"✅ Pruebas exitosas: {resultado.testsRun - len(resultado.failures) - len(resultado.errors)}")
    print(f"❌ Pruebas fallidas: {len(resultado.failures)}")
    print(f"💥 Errores: {len(resultado.errors)}")
    print(f"⏭️ Pruebas omitidas: {len(resultado.skipped)}")
    
    if resultado.wasSuccessful():
        print(f"\n🎉 ¡TODAS LAS PRUEBAS PASARON EXITOSAMENTE!")
    else:
        print(f"\n⚠️ Algunas pruebas fallaron. Revisa los detalles arriba.")
    
    return resultado


# Función para pruebas de integración
def pruebas_integracion_completa():
    """
    Ejecuta pruebas de integración con datos reales simulados
    """
    print("\n🔗 PRUEBAS DE INTEGRACIÓN")
    print("=" * 40)
    
    analizador = AnalizadorFinancieroOptimizado()
    
    # Datos simulados más realistas
    transacciones_reales = [
        1200.50, 850.75, 2300.00, 675.25, 1800.80,
        950.00, 1750.25, 420.50, 2100.75, 1350.00,
        3200.00, 580.25, 1920.50, 775.00, 2650.25
    ]
    
    categorias_reales = [
        "Software", "Hardware", "Consultoria", "Hardware", "Software",
        "Soporte", "Consultoria", "Hardware", "Software", "Soporte",
        "Consultoria", "Hardware", "Software", "Soporte", "Consultoria"
    ]
    
    print("📊 Datos de prueba:")
    print(f"   Transacciones: {len(transacciones_reales)}")
    print(f"   Categorías únicas: {len(set(categorias_reales))}")
    
    try:
        # Ejecutar análisis completo
        total = analizador.calcular_total_ingresos(transacciones_reales)
        print(f"✅ Total calculado: ${total:,.2f}")
        
        ingresos_altos = analizador.filtrar_ingresos_altos(transacciones_reales, 1500)
        print(f"✅ Ingresos > $1,500: {len(ingresos_altos)} encontrados")
        
        agrupado = analizador.agrupar_por_categoria(transacciones_reales, categorias_reales)
        print(f"✅ Agrupación exitosa: {len(agrupado)} categorías")
        
        stats = analizador.analisis_estadistico_completo(transacciones_reales)
        print(f"✅ Estadísticas generadas: {len(stats)} métricas")
        
        ranking = analizador.ranking_categorias(transacciones_reales, categorias_reales)
        print(f"✅ Ranking generado: Top categoría: {ranking[0][0]}")
        
        # Exportar resultados
        analizador.exportar_estadisticas(transacciones_reales, categorias_reales, "test_integracion.json")
        print(f"✅ Exportación exitosa")
        
        print(f"\n🎉 PRUEBAS DE INTEGRACIÓN COMPLETADAS EXITOSAMENTE")
        
    except Exception as e:
        print(f"❌ Error en pruebas de integración: {e}")
        return False
    
    finally:
        # Limpiar archivo de prueba
        if os.path.exists("test_integracion.json"):
            os.remove("test_integracion.json")
    
    return True


if __name__ == "__main__":
    # Ejecutar todas las pruebas
    resultado_pruebas = ejecutar_pruebas_completas()
    
    # Ejecutar pruebas de integración
    resultado_integracion = pruebas_integracion_completa()
    
    # Reporte final
    print(f"\n🏁 REPORTE FINAL")
    print("=" * 20)
    print(f"Pruebas unitarias: {'✅ EXITOSO' if resultado_pruebas.wasSuccessful() else '❌ FALLIDO'}")
    print(f"Pruebas integración: {'✅ EXITOSO' if resultado_integracion else '❌ FALLIDO'}")
    
    if resultado_pruebas.wasSuccessful() and resultado_integracion:
        print(f"\n🎊 ¡TODAS LAS PRUEBAS DEL SISTEMA DATASOLVERS COMPLETADAS!")
        print(f"✨ El código está listo para producción")
    else:
        print(f"\n⚠️ Hay problemas que necesitan ser resueltos antes de continuar")