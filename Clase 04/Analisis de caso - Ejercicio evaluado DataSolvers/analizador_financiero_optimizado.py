from collections import defaultdict, Counter
from typing import List, Dict, Set, Tuple, Union
import statistics
from datetime import datetime, date
import json


class AnalizadorFinancieroOptimizado:
    """
    Clase optimizada para análisis financiero con estructuras de datos avanzadas
    y sentencias iterativas eficientes.
    """
    
    def __init__(self):
        """Inicializa el analizador con estructuras auxiliares."""
        self.categorias_unicas = set()
        self.historial_analisis = []
        self.cache_resultados = {}
    
    # ==================== FUNCIONES BÁSICAS OPTIMIZADAS ====================
    
    def calcular_total_ingresos(self, transacciones: List[Union[int, float]]) -> float:
        """
        OPTIMIZADO: Calcula el total de ingresos usando la función built-in sum()
        
        Mejoras implementadas:
        - Uso de sum() en lugar de bucle manual (más eficiente)
        - Type hints para mejor documentación
        - Validación de entrada
        - Registro en historial
        
        Args:
            transacciones: Lista de valores de ingresos
            
        Returns:
            Total de ingresos
            
        Raises:
            ValueError: Si la lista está vacía o contiene valores inválidos
        """
        if not transacciones:
            raise ValueError("La lista de transacciones no puede estar vacía")
        
        # Validar que todos los valores sean numéricos
        if not all(isinstance(x, (int, float)) for x in transacciones):
            raise ValueError("Todas las transacciones deben ser números")
        
        # OPTIMIZACIÓN: Usar sum() built-in es más eficiente que bucle manual
        total = sum(transacciones)
        
        # Registrar análisis en historial
        self._registrar_analisis("calcular_total_ingresos", {
            "total_transacciones": len(transacciones),
            "resultado": total
        })
        
        return total
    
    def filtrar_ingresos_altos(self, transacciones: List[Union[int, float]], 
                              umbral: Union[int, float]) -> List[Union[int, float]]:
        """
        OPTIMIZADO: Filtra ingresos usando list comprehension
        
        Mejoras implementadas:
        - List comprehension en lugar de bucle manual (más eficiente)
        - Validación de entrada
        - Type hints
        
        Args:
            transacciones: Lista de valores de ingresos
            umbral: Valor mínimo para considerar ingreso alto
            
        Returns:
            Lista de ingresos mayores al umbral
        """
        if not transacciones:
            return []
        
        if not isinstance(umbral, (int, float)):
            raise ValueError("El umbral debe ser un número")
        
        # OPTIMIZACIÓN: List comprehension es más eficiente que bucle manual
        ingresos_altos = [ingreso for ingreso in transacciones if ingreso > umbral]
        
        self._registrar_analisis("filtrar_ingresos_altos", {
            "umbral": umbral,
            "total_encontrados": len(ingresos_altos),
            "porcentaje": (len(ingresos_altos) / len(transacciones)) * 100
        })
        
        return ingresos_altos
    
    def agrupar_por_categoria(self, transacciones: List[Union[int, float]], 
                             categorias: List[str]) -> Dict[str, List[Union[int, float]]]:
        """
        OPTIMIZADO: Agrupa ingresos usando defaultdict
        
        Mejoras implementadas:
        - defaultdict para evitar verificaciones de existencia de claves
        - Validación de longitudes
        - Actualización automática de categorías únicas
        
        Args:
            transacciones: Lista de valores de ingresos
            categorias: Lista de categorías correspondientes
            
        Returns:
            Diccionario con categorías como claves y listas de ingresos como valores
        """
        if len(transacciones) != len(categorias):
            raise ValueError("Las listas de transacciones y categorías deben tener la misma longitud")
        
        # OPTIMIZACIÓN: defaultdict evita verificar si la clave existe
        agrupado = defaultdict(list)
        
        for categoria, ingreso in zip(categorias, transacciones):
            agrupado[categoria].append(ingreso)
            # Actualizar set de categorías únicas automáticamente
            self.categorias_unicas.add(categoria)
        
        # Convertir a dict regular para retorno
        resultado = dict(agrupado)
        
        self._registrar_analisis("agrupar_por_categoria", {
            "categorias_encontradas": len(resultado),
            "total_transacciones": len(transacciones)
        })
        
        return resultado
    
    # ==================== FUNCIONES AVANZADAS CON SETS ====================
    
    def obtener_categorias_unicas(self, categorias: List[str]) -> Set[str]:
        """
        NUEVO: Utiliza set para obtener categorías únicas de forma eficiente
        
        Beneficios de usar set:
        - O(1) para búsquedas y eliminación de duplicados
        - Automáticamente elimina duplicados
        - Más eficiente que usar list para verificar unicidad
        
        Args:
            categorias: Lista de categorías (puede tener duplicados)
            
        Returns:
            Set con categorías únicas
        """
        categorias_set = set(categorias)
        self.categorias_unicas.update(categorias_set)
        
        return categorias_set
    
    def verificar_categoria_existe(self, categoria: str) -> bool:
        """
        NUEVO: Verificación O(1) si una categoría existe usando set
        
        Args:
            categoria: Categoría a verificar
            
        Returns:
            True si la categoría existe, False en caso contrario
        """
        return categoria in self.categorias_unicas
    
    def encontrar_categorias_comunes(self, lista1: List[str], lista2: List[str]) -> Set[str]:
        """
        NUEVO: Encuentra categorías comunes entre dos listas usando intersección de sets
        
        Args:
            lista1: Primera lista de categorías
            lista2: Segunda lista de categorías
            
        Returns:
            Set con categorías que aparecen en ambas listas
        """
        set1 = set(lista1)
        set2 = set(lista2)
        
        # Intersección es muy eficiente con sets
        return set1 & set2
    
    # ==================== ANÁLISIS ESTADÍSTICO AVANZADO ====================
    
    def analisis_estadistico_completo(self, transacciones: List[Union[int, float]]) -> Dict[str, float]:
        """
        NUEVO: Análisis estadístico completo usando funciones optimizadas
        
        Args:
            transacciones: Lista de valores de ingresos
            
        Returns:
            Diccionario con estadísticas completas
        """
        if not transacciones:
            return {}
        
        # Usar funciones built-in optimizadas del módulo statistics
        stats = {
            'total': sum(transacciones),
            'promedio': statistics.mean(transacciones),
            'mediana': statistics.median(transacciones),
            'minimo': min(transacciones),
            'maximo': max(transacciones),
            'rango': max(transacciones) - min(transacciones),
            'cantidad': len(transacciones)
        }
        
        # Agregar desviación estándar si hay suficientes datos
        if len(transacciones) > 1:
            stats['desviacion_estandar'] = statistics.stdev(transacciones)
            stats['varianza'] = statistics.variance(transacciones)
        
        return stats
    
    def analizar_por_categoria_avanzado(self, transacciones: List[Union[int, float]], 
                                       categorias: List[str]) -> Dict[str, Dict[str, Union[int, float]]]:
        """
        NUEVO: Análisis estadístico completo por categoría
        
        Args:
            transacciones: Lista de valores de ingresos
            categorias: Lista de categorías correspondientes
            
        Returns:
            Diccionario anidado con estadísticas por categoría
        """
        agrupado = self.agrupar_por_categoria(transacciones, categorias)
        
        resultado = {}
        for categoria, valores in agrupado.items():
            resultado[categoria] = self.analisis_estadistico_completo(valores)
            # Agregar información específica de categoría
            resultado[categoria]['participacion_porcentual'] = (
                len(valores) / len(transacciones) * 100
            )
        
        return resultado
    
    # ==================== FUNCIONES DE RENDIMIENTO ====================
    
    def filtros_multiples_optimizado(self, transacciones: List[Union[int, float]], 
                                   **filtros) -> List[Union[int, float]]:
        """
        NUEVO: Aplica múltiples filtros de forma eficiente usando generator expressions
        
        Args:
            transacciones: Lista de valores de ingresos
            **filtros: Filtros a aplicar (ej: minimo=1000, maximo=5000)
            
        Returns:
            Lista filtrada
        """
        resultado = transacciones
        
        # Aplicar filtros usando generator expressions (memory efficient)
        if 'minimo' in filtros:
            resultado = [x for x in resultado if x >= filtros['minimo']]
        
        if 'maximo' in filtros:
            resultado = [x for x in resultado if x <= filtros['maximo']]
        
        if 'multiplo_de' in filtros:
            resultado = [x for x in resultado if x % filtros['multiplo_de'] == 0]
        
        return resultado
    
    def ranking_categorias(self, transacciones: List[Union[int, float]], 
                          categorias: List[str], criterio: str = 'total') -> List[Tuple[str, float]]:
        """
        NUEVO: Crea ranking de categorías según diferentes criterios
        
        Args:
            transacciones: Lista de valores de ingresos
            categorias: Lista de categorías correspondientes
            criterio: 'total', 'promedio', 'cantidad', 'maximo'
            
        Returns:
            Lista ordenada de tuplas (categoria, valor)
        """
        agrupado = self.agrupar_por_categoria(transacciones, categorias)
        
        # Diccionario de funciones para cada criterio
        criterios = {
            'total': sum,
            'promedio': lambda x: sum(x) / len(x),
            'cantidad': len,
            'maximo': max,
            'minimo': min
        }
        
        if criterio not in criterios:
            raise ValueError(f"Criterio '{criterio}' no válido. Opciones: {list(criterios.keys())}")
        
        func_criterio = criterios[criterio]
        
        # Crear ranking usando list comprehension y sorted
        ranking = [(categoria, func_criterio(valores)) 
                  for categoria, valores in agrupado.items()]
        
        # Ordenar de mayor a menor
        return sorted(ranking, key=lambda x: x[1], reverse=True)
    
    # ==================== FUNCIONES DE UTILIDAD ====================
    
    def _registrar_analisis(self, funcion: str, metadata: Dict):
        """
        Registra cada análisis realizado para auditoría
        
        Args:
            funcion: Nombre de la función ejecutada
            metadata: Información adicional del análisis
        """
        registro = {
            'timestamp': datetime.now().isoformat(),
            'funcion': funcion,
            'metadata': metadata
        }
        self.historial_analisis.append(registro)
    
    def obtener_historial_analisis(self, limite: int = 10) -> List[Dict]:
        """
        Obtiene el historial de análisis realizados
        
        Args:
            limite: Número máximo de registros a retornar
            
        Returns:
            Lista con los últimos análisis realizados
        """
        return self.historial_analisis[-limite:]
    
    def limpiar_cache(self):
        """Limpia el cache de resultados."""
        self.cache_resultados.clear()
    
    def exportar_estadisticas(self, transacciones: List[Union[int, float]], 
                             categorias: List[str], archivo: str = "estadisticas.json"):
        """
        NUEVO: Exporta estadísticas completas a archivo JSON
        
        Args:
            transacciones: Lista de valores de ingresos
            categorias: Lista de categorías correspondientes
            archivo: Nombre del archivo de salida
        """
        estadisticas = {
            'resumen_general': self.analisis_estadistico_completo(transacciones),
            'analisis_por_categoria': self.analizar_por_categoria_avanzado(transacciones, categorias),
            'ranking_por_total': self.ranking_categorias(transacciones, categorias, 'total'),
            'ranking_por_promedio': self.ranking_categorias(transacciones, categorias, 'promedio'),
            'categorias_unicas': list(self.categorias_unicas),
            'fecha_analisis': datetime.now().isoformat(),
            'total_transacciones': len(transacciones)
        }
        
        with open(archivo, 'w', encoding='utf-8') as f:
            json.dump(estadisticas, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Estadísticas exportadas a {archivo}")
    
    def comparar_rendimiento(self, transacciones: List[Union[int, float]]):
        """
        NUEVO: Compara el rendimiento entre métodos optimizados y tradicionales
        
        Args:
            transacciones: Lista de valores para testing
        """
        import time
        
        print("🏃‍♂️ COMPARACIÓN DE RENDIMIENTO")
        print("=" * 40)
        
        # Método tradicional (bucle manual)
        start = time.time()
        total_tradicional = 0
        for t in transacciones:
            total_tradicional += t
        tiempo_tradicional = time.time() - start
        
        # Método optimizado (sum built-in)
        start = time.time()
        total_optimizado = sum(transacciones)
        tiempo_optimizado = time.time() - start
        
        print(f"Método tradicional: {tiempo_tradicional:.6f}s")
        print(f"Método optimizado: {tiempo_optimizado:.6f}s")
        
        if tiempo_tradicional > 0:
            mejora = (tiempo_tradicional - tiempo_optimizado) / tiempo_tradicional * 100
            print(f"Mejora de rendimiento: {mejora:.2f}%")
        
        print(f"Resultados iguales: {total_tradicional == total_optimizado}")


# Demostración del código optimizado
if __name__ == "__main__":
    print("🚀 DATASOLVERS - CÓDIGO OPTIMIZADO")
    print("=" * 50)
    
    # Crear instancia del analizador optimizado
    analizador = AnalizadorFinancieroOptimizado()
    
    # Datos de prueba más realistas
    transacciones = [1000, 1500, 750, 2000, 500, 1200, 1800, 300, 2500, 1100, 
                    3000, 450, 1750, 900, 2200, 650, 1900, 400, 2800, 1300]
    categorias = ["Ventas", "Servicios", "Ventas", "Servicios", "Productos",
                 "Ventas", "Servicios", "Productos", "Servicios", "Ventas",
                 "Consultoria", "Productos", "Ventas", "Consultoria", "Servicios",
                 "Productos", "Consultoria", "Ventas", "Servicios", "Consultoria"]
    
    print(f"📊 Analizando {len(transacciones)} transacciones en {len(set(categorias))} categorías")
    
    # Demostrar funciones optimizadas
    print(f"\n💰 Total ingresos: ${analizador.calcular_total_ingresos(transacciones):,.2f}")
    
    ingresos_altos = analizador.filtrar_ingresos_altos(transacciones, 1500)
    print(f"💎 Ingresos > $1,500: {len(ingresos_altos)} transacciones")
    
    # Demostrar funciones avanzadas con sets
    categorias_unicas = analizador.obtener_categorias_unicas(categorias)
    print(f"🏷️ Categorías únicas: {categorias_unicas}")
    
    # Análisis estadístico completo
    stats = analizador.analisis_estadistico_completo(transacciones)
    print(f"\n📈 ESTADÍSTICAS GENERALES:")
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"   {key}: ${value:,.2f}")
        else:
            print(f"   {key}: {value}")
    
    # Ranking de categorías
    ranking = analizador.ranking_categorias(transacciones, categorias, 'total')
    print(f"\n🏆 RANKING POR TOTAL:")
    for i, (categoria, total) in enumerate(ranking, 1):
        print(f"   {i}. {categoria}: ${total:,.2f}")
    
    print(f"\n✅ Análisis optimizado completado")
    print(f"📋 Registros en historial: {len(analizador.historial_analisis)}")