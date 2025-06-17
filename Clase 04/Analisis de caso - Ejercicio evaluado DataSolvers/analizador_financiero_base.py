class AnalizadorFinanciero:
    """
    Clase base para análisis financiero - Código original sin optimizar.
    """
    
    def calcular_total_ingresos(self, transacciones):
        """
        Calcula el total de ingresos en una lista de transacciones
        
        Args:
            transacciones (list): Lista de valores de ingresos
            
        Returns:
            float: Total de ingresos
        """
        total = 0
        for ingreso in transacciones:
            total += ingreso
        return total

    def filtrar_ingresos_altos(self, transacciones, umbral):
        """
        Filtra y retorna solo los ingresos mayores a un umbral dado
        
        Args:
            transacciones (list): Lista de valores de ingresos
            umbral (float): Valor mínimo para considerar ingreso alto
            
        Returns:
            list: Lista de ingresos mayores al umbral
        """
        ingresos_altos = []
        for ingreso in transacciones:
            if ingreso > umbral:
                ingresos_altos.append(ingreso)
        return ingresos_altos

    def agrupar_por_categoria(self, transacciones, categorias):
        """
        Agrupa ingresos en un diccionario por categorías
        
        Args:
            transacciones (list): Lista de valores de ingresos
            categorias (list): Lista de categorías correspondientes
            
        Returns:
            dict: Diccionario con categorías como claves y listas de ingresos como valores
        """
        agrupado = {}
        for categoria, ingreso in zip(categorias, transacciones):
            if categoria in agrupado:
                agrupado[categoria].append(ingreso)
            else:
                agrupado[categoria] = [ingreso]
        return agrupado


# Ejemplo de uso del código base
if __name__ == "__main__":
    print("📊 DATASOLVERS - CÓDIGO BASE ORIGINAL")
    print("=" * 50)
    
    # Crear instancia del analizador
    analizador = AnalizadorFinanciero()
    
    # Datos de prueba
    transacciones = [1000, 1500, 750, 2000, 500, 1200, 1800, 300, 2500, 1100]
    categorias = ["Ventas", "Servicios", "Ventas", "Servicios", "Productos", 
                  "Ventas", "Servicios", "Productos", "Servicios", "Ventas"]
    
    print(f"Transacciones: {transacciones}")
    print(f"Categorías: {categorias}")
    
    # Probar funciones
    total = analizador.calcular_total_ingresos(transacciones)
    print(f"\nTotal de ingresos: ${total:,.2f}")
    
    ingresos_altos = analizador.filtrar_ingresos_altos(transacciones, 1000)
    print(f"Ingresos mayores a $1,000: {ingresos_altos}")
    
    agrupado = analizador.agrupar_por_categoria(transacciones, categorias)
    print(f"Agrupado por categoría: {agrupado}")
    
    print("\n✅ Código base ejecutado correctamente")