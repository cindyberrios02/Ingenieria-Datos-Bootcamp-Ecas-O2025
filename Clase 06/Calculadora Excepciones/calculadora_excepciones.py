# Clase 06: Manejo de Excepciones en Python
# Calculadora básica con manejo robusto de errores y funcionalidades avanzadas

import math
import logging
from datetime import datetime
from typing import Union, Tuple, Optional


class CalculadoraAvanzada:
    """
    Calculadora avanzada con manejo completo de excepciones y funcionalidades extras.
    """
    
    def __init__(self):
        """Inicializa la calculadora con configuración de logging y historial."""
        self.historial = []
        self.configurar_logging()
        self.operadores_validos = {'+', '-', '*', '/', '^', '%', '//', 'sqrt', 'log'}
    
    def configurar_logging(self):
        """Configura el sistema de logging para registrar operaciones y errores."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('calculadora.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def solicitar_numero(self, mensaje: str) -> float:
        """
        Solicita un número al usuario con validación robusta.
        
        Args:
            mensaje (str): Mensaje a mostrar al usuario
            
        Returns:
            float: Número validado del usuario
            
        Raises:
            ValueError: Si la entrada no es un número válido
            KeyboardInterrupt: Si el usuario cancela la operación
        """
        while True:
            try:
                entrada = input(mensaje).strip()
                
                # Verificar si el usuario quiere cancelar
                if entrada.lower() in ['salir', 'exit', 'quit', 'cancelar']:
                    raise KeyboardInterrupt("Operación cancelada por el usuario")
                
                # Validar entrada vacía
                if not entrada:
                    raise ValueError("No puedes dejar esto vacío")
                
                # Intentar convertir a número
                numero = float(entrada)
                
                # Validar que no sea infinito o NaN
                if math.isinf(numero):
                    raise ValueError("El número no puede ser infinito")
                if math.isnan(numero):
                    raise ValueError("Entrada inválida (NaN)")
                
                self.logger.info(f"Número válido ingresado: {numero}")
                return numero
                
            except ValueError as e:
                if "could not convert" in str(e):
                    print(f"❌ Error: '{entrada}' no es un número válido. Intenta de nuevo.")
                else:
                    print(f"❌ Error: {e}")
                print("💡 Tip: Puedes escribir 'salir' para cancelar")
                continue
    
    def solicitar_operador(self) -> str:
        """
        Solicita el operador al usuario con validación.
        
        Returns:
            str: Operador validado
            
        Raises:
            ValueError: Si el operador no es válido
            KeyboardInterrupt: Si el usuario cancela la operación
        """
        print(f"\n🔢 Operadores disponibles:")
        print(f"   +  : Suma")
        print(f"   -  : Resta")
        print(f"   *  : Multiplicación")
        print(f"   /  : División")
        print(f"   ^  : Potencia")
        print(f"   %  : Módulo (resto)")
        print(f"   // : División entera")
        print(f"   sqrt: Raíz cuadrada (solo primer número)")
        print(f"   log: Logaritmo natural (solo primer número)")
        
        while True:
            try:
                operador = input("\n🔸 Ingresa la operación: ").strip()
                
                # Verificar cancelación
                if operador.lower() in ['salir', 'exit', 'quit', 'cancelar']:
                    raise KeyboardInterrupt("Operación cancelada por el usuario")
                
                # Validar entrada vacía
                if not operador:
                    raise ValueError("Debes ingresar un operador")
                
                # Validar operador
                if operador not in self.operadores_validos:
                    operadores_str = ', '.join(sorted(self.operadores_validos))
                    raise ValueError(f"Operador '{operador}' no válido. Usa: {operadores_str}")
                
                self.logger.info(f"Operador válido seleccionado: {operador}")
                return operador
                
            except ValueError as e:
                print(f"❌ Error: {e}")
                print("💡 Tip: Puedes escribir 'salir' para cancelar")
                continue
    
    def realizar_operacion(self, num1: float, num2: float, operador: str) -> float:
        """
        Realiza la operación matemática especificada.
        
        Args:
            num1 (float): Primer número
            num2 (float): Segundo número
            operador (str): Operador matemático
            
        Returns:
            float: Resultado de la operación
            
        Raises:
            ZeroDivisionError: Para divisiones por cero
            ValueError: Para operaciones inválidas (raíz negativa, log de negativo)
            OverflowError: Para resultados demasiado grandes
        """
        try:
            if operador == "+":
                resultado = num1 + num2
                
            elif operador == "-":
                resultado = num1 - num2
                
            elif operador == "*":
                resultado = num1 * num2
                
            elif operador == "/":
                if num2 == 0:
                    raise ZeroDivisionError("No se puede dividir por cero")
                resultado = num1 / num2
                
            elif operador == "^":
                # Validar potencias problemáticas
                if num1 == 0 and num2 < 0:
                    raise ZeroDivisionError("No se puede elevar 0 a una potencia negativa")
                if num1 < 0 and not num2.is_integer():
                    raise ValueError("No se puede elevar un número negativo a una potencia decimal")
                resultado = num1 ** num2
                
            elif operador == "%":
                if num2 == 0:
                    raise ZeroDivisionError("No se puede calcular módulo con divisor cero")
                resultado = num1 % num2
                
            elif operador == "//":
                if num2 == 0:
                    raise ZeroDivisionError("No se puede hacer división entera por cero")
                resultado = num1 // num2
                
            elif operador == "sqrt":
                if num1 < 0:
                    raise ValueError("No se puede calcular la raíz cuadrada de un número negativo")
                resultado = math.sqrt(num1)
                
            elif operador == "log":
                if num1 <= 0:
                    raise ValueError("No se puede calcular logaritmo de un número menor o igual a cero")
                resultado = math.log(num1)
            
            # Validar resultado
            if math.isinf(resultado):
                raise OverflowError("El resultado es demasiado grande")
            if math.isnan(resultado):
                raise ValueError("El resultado no es un número válido")
            
            self.logger.info(f"Operación exitosa: {num1} {operador} {num2} = {resultado}")
            return resultado
            
        except (ZeroDivisionError, ValueError, OverflowError) as e:
            self.logger.error(f"Error en operación: {num1} {operador} {num2} - {e}")
            raise
    
    def formatear_resultado(self, num1: float, num2: float, operador: str, resultado: float) -> str:
        """
        Formatea el resultado de manera amigable.
        
        Args:
            num1, num2 (float): Números de la operación
            operador (str): Operador usado
            resultado (float): Resultado de la operación
            
        Returns:
            str: Resultado formateado
        """
        if operador in ['sqrt', 'log']:
            if operador == 'sqrt':
                return f"√{num1} = {resultado:.6f}"
            else:  # log
                return f"ln({num1}) = {resultado:.6f}"
        else:
            return f"{num1} {operador} {num2} = {resultado:.6f}"
    
    def agregar_al_historial(self, operacion: str, resultado: float):
        """
        Agrega una operación al historial.
        
        Args:
            operacion (str): Descripción de la operación
            resultado (float): Resultado obtenido
        """
        entrada_historial = {
            'timestamp': datetime.now(),
            'operacion': operacion,
            'resultado': resultado
        }
        self.historial.append(entrada_historial)
        
        # Limitar historial a últimas 50 operaciones
        if len(self.historial) > 50:
            self.historial.pop(0)
    
    def mostrar_historial(self):
        """Muestra el historial de operaciones."""
        if not self.historial:
            print("📋 No hay operaciones en el historial")
            return
        
        print(f"\n📋 HISTORIAL DE OPERACIONES ({len(self.historial)} entradas)")
        print("=" * 60)
        
        for i, entrada in enumerate(self.historial[-10:], 1):  # Últimas 10
            timestamp = entrada['timestamp'].strftime("%H:%M:%S")
            print(f"{i:2d}. [{timestamp}] {entrada['operacion']} = {entrada['resultado']:.6f}")
    
    def calculadora_basica(self):
        """
        Función principal de la calculadora (cumple los requisitos básicos).
        """
        print("🧮 CALCULADORA BÁSICA")
        print("=" * 30)
        print("Realiza una operación matemática con manejo de excepciones")
        
        try:
            # Solicitar primer número
            num1 = self.solicitar_numero("🔸 Ingresa el primer número: ")
            
            # Solicitar operador
            operador = self.solicitar_operador()
            
            # Para operaciones unarias, no necesitamos segundo número
            if operador in ['sqrt', 'log']:
                num2 = 0  # No se usa, pero lo ponemos para consistencia
                print(f"\n🔄 Calculando {operador}({num1})...")
            else:
                # Solicitar segundo número
                num2 = self.solicitar_numero("🔸 Ingresa el segundo número: ")
                print(f"\n🔄 Calculando {num1} {operador} {num2}...")
            
            # Realizar operación
            resultado = self.realizar_operacion(num1, num2, operador)
            
            # Formatear y mostrar resultado
            operacion_str = self.formatear_resultado(num1, num2, operador, resultado)
            print(f"\n✅ RESULTADO:")
            print(f"   {operacion_str}")
            
            # Agregar al historial
            self.agregar_al_historial(operacion_str, resultado)
            
        except ValueError as ve:
            print(f"\n❌ Error de valor: {ve}")
            self.logger.error(f"ValueError: {ve}")
            
        except ZeroDivisionError as zde:
            print(f"\n❌ Error de división: {zde}")
            self.logger.error(f"ZeroDivisionError: {zde}")
            
        except OverflowError as oe:
            print(f"\n❌ Error de overflow: {oe}")
            self.logger.error(f"OverflowError: {oe}")
            
        except KeyboardInterrupt:
            print(f"\n⏹️ Operación cancelada por el usuario")
            self.logger.info("Operación cancelada por el usuario")
            
        except Exception as e:
            print(f"\n❌ Error inesperado: {e}")
            self.logger.error(f"Error inesperado: {e}")
            
        finally:
            print("\n🔚 Operación finalizada.")
    
    def calculadora_con_repeticion(self):
        """
        Calculadora con opción de repetir (Ejercicio PLUS).
        """
        print("🔄 CALCULADORA CON REPETICIÓN")
        print("=" * 35)
        print("Realiza múltiples operaciones hasta que decidas salir")
        
        operacion_numero = 0
        
        while True:
            try:
                operacion_numero += 1
                print(f"\n{'='*50}")
                print(f"🔢 OPERACIÓN #{operacion_numero}")
                print(f"{'='*50}")
                
                # Ejecutar una operación
                self.calculadora_basica()
                
                # Preguntar si continuar
                print(f"\n🤔 ¿Qué quieres hacer ahora?")
                print("1. ➕ Realizar otra operación")
                print("2. 📋 Ver historial")
                print("3. 🗑️ Limpiar historial")
                print("4. 🚪 Salir")
                
                while True:
                    try:
                        opcion = input("\n👉 Selecciona una opción (1-4): ").strip()
                        
                        if opcion == "1":
                            break  # Continuar con otra operación
                        elif opcion == "2":
                            self.mostrar_historial()
                            continue
                        elif opcion == "3":
                            self.historial.clear()
                            print("✅ Historial limpiado")
                            continue
                        elif opcion == "4":
                            print("\n👋 ¡Gracias por usar la calculadora!")
                            print(f"📊 Total de operaciones realizadas: {operacion_numero}")
                            if self.historial:
                                print("📋 Tu historial se ha guardado en 'calculadora.log'")
                            return
                        else:
                            print("❌ Opción no válida. Selecciona 1, 2, 3 o 4.")
                            continue
                            
                    except KeyboardInterrupt:
                        print("\n\n👋 ¡Hasta luego!")
                        return
                        
            except KeyboardInterrupt:
                print("\n\n👋 ¡Hasta luego!")
                return
            except Exception as e:
                print(f"\n❌ Error crítico: {e}")
                self.logger.critical(f"Error crítico en calculadora_con_repeticion: {e}")
                continue
    
    def modo_evaluacion_expresiones(self):
        """
        Modo avanzado que permite evaluar expresiones matemáticas completas.
        """
        print("🧠 MODO EVALUACIÓN DE EXPRESIONES")
        print("=" * 40)
        print("Evalúa expresiones matemáticas completas")
        print("Ejemplo: 2 + 3 * 4, (5 + 3) / 2, etc.")
        print("⚠️ ADVERTENCIA: Solo usa expresiones matemáticas simples")
        
        while True:
            try:
                expresion = input("\n🔸 Ingresa la expresión (o 'salir'): ").strip()
                
                if expresion.lower() in ['salir', 'exit', 'quit']:
                    break
                
                if not expresion:
                    print("❌ Debes ingresar una expresión")
                    continue
                
                # Validar caracteres permitidos (solo números, operadores y paréntesis)
                caracteres_permitidos = set("0123456789+-*/()%. ")
                if not all(c in caracteres_permitidos for c in expresion):
                    raise ValueError("La expresión contiene caracteres no permitidos")
                
                # Evaluar la expresión
                resultado = eval(expresion)
                
                print(f"✅ {expresion} = {resultado:.6f}")
                self.agregar_al_historial(expresion, resultado)
                
            except ZeroDivisionError:
                print("❌ Error: División por cero en la expresión")
            except SyntaxError:
                print("❌ Error: Sintaxis inválida en la expresión")
            except ValueError as e:
                print(f"❌ Error: {e}")
            except Exception as e:
                print(f"❌ Error al evaluar: {e}")
    
    def mostrar_estadisticas(self):
        """Muestra estadísticas del uso de la calculadora."""
        if not self.historial:
            print("📊 No hay estadísticas disponibles")
            return
        
        print(f"\n📊 ESTADÍSTICAS DE USO")
        print("=" * 30)
        
        # Contar operadores usados
        operadores_count = {}
        resultados = []
        
        for entrada in self.historial:
            operacion = entrada['operacion']
            resultado = entrada['resultado']
            resultados.append(resultado)
            
            # Extraer operador (simplificado)
            for op in self.operadores_validos:
                if op in operacion:
                    operadores_count[op] = operadores_count.get(op, 0) + 1
                    break
        
        print(f"📈 Total de operaciones: {len(self.historial)}")
        print(f"📊 Promedio de resultados: {sum(resultados)/len(resultados):.2f}")
        print(f"🔝 Resultado máximo: {max(resultados):.2f}")
        print(f"🔻 Resultado mínimo: {min(resultados):.2f}")
        
        if operadores_count:
            print(f"\n🔢 Operadores más usados:")
            for op, count in sorted(operadores_count.items(), key=lambda x: x[1], reverse=True):
                print(f"   {op}: {count} veces")


def demo_manejo_excepciones():
    """
    Función de demostración de diferentes tipos de excepciones.
    """
    print("🎓 DEMO: MANEJO DE EXCEPCIONES")
    print("=" * 40)
    print("Demostración de diferentes casos de error y su manejo")
    
    calc = CalculadoraAvanzada()
    
    casos_demo = [
        ("División por cero", 10, 0, "/"),
        ("Entrada no numérica", "abc", 5, "+"),
        ("Operador inválido", 5, 3, "&"),
        ("Raíz de negativo", -4, 0, "sqrt"),
        ("Logaritmo de negativo", -2, 0, "log"),
        ("Potencia problemática", -2, 0.5, "^"),
        ("Operación válida", 10, 5, "+")
    ]
    
    for descripcion, num1, num2, op in casos_demo:
        print(f"\n🧪 Caso: {descripcion}")
        print(f"   Operación: {num1} {op} {num2}")
        
        try:
            if isinstance(num1, str):
                # Simular error de conversión
                num1 = float(num1)
            
            if op not in calc.operadores_validos:
                raise ValueError(f"Operador '{op}' no válido")
            
            resultado = calc.realizar_operacion(num1, num2, op)
            print(f"   ✅ Resultado: {resultado:.6f}")
            
        except ValueError as e:
            print(f"   ❌ ValueError: {e}")
        except ZeroDivisionError as e:
            print(f"   ❌ ZeroDivisionError: {e}")
        except Exception as e:
            print(f"   ❌ Error: {e}")


def menu_principal():
    """
    Menú principal de la calculadora con todas las opciones.
    """
    calc = CalculadoraAvanzada()
    
    while True:
        print(f"\n" + "="*60)
        print("🧮 SISTEMA DE CALCULADORA AVANZADA")
        print("🎓 Clase 06 - Manejo de Excepciones en Python")
        print("="*60)
        print("Selecciona una opción:")
        print("1. 🔢 Calculadora básica (requisitos mínimos)")
        print("2. 🔄 Calculadora con repetición (PLUS)")
        print("3. 🧠 Evaluador de expresiones (avanzado)")
        print("4. 📋 Ver historial de operaciones")
        print("5. 📊 Mostrar estadísticas de uso")
        print("6. 🗑️ Limpiar historial")
        print("7. 🎓 Demo de manejo de excepciones")
        print("8. 💾 Exportar historial a archivo")
        print("0. 🚪 Salir")
        print("-" * 60)
        
        try:
            opcion = input("👉 Ingresa tu opción (0-8): ").strip()
            
            if opcion == "0":
                print("\n👋 ¡Gracias por usar la calculadora avanzada!")
                if calc.historial:
                    print("📋 Tu historial se guardó automáticamente")
                break
                
            elif opcion == "1":
                calc.calculadora_basica()
                
            elif opcion == "2":
                calc.calculadora_con_repeticion()
                
            elif opcion == "3":
                calc.modo_evaluacion_expresiones()
                
            elif opcion == "4":
                calc.mostrar_historial()
                
            elif opcion == "5":
                calc.mostrar_estadisticas()
                
            elif opcion == "6":
                if calc.historial:
                    calc.historial.clear()
                    print("✅ Historial limpiado exitosamente")
                else:
                    print("📋 El historial ya está vacío")
                    
            elif opcion == "7":
                demo_manejo_excepciones()
                
            elif opcion == "8":
                if calc.historial:
                    try:
                        with open("historial_calculadora.txt", "w", encoding="utf-8") as f:
                            f.write("HISTORIAL DE CALCULADORA\n")
                            f.write("=" * 50 + "\n\n")
                            for entrada in calc.historial:
                                timestamp = entrada['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
                                f.write(f"[{timestamp}] {entrada['operacion']} = {entrada['resultado']}\n")
                        print("✅ Historial exportado a 'historial_calculadora.txt'")
                    except Exception as e:
                        print(f"❌ Error al exportar: {e}")
                else:
                    print("📋 No hay historial para exportar")
                    
            else:
                print("❌ Opción no válida. Selecciona un número del 0 al 8.")
            
            if opcion != "0":
                input("\n⏸️ Presiona Enter para continuar...")
                
        except KeyboardInterrupt:
            print("\n\n👋 ¡Hasta luego!")
            break
        except Exception as e:
            print(f"\n❌ Error inesperado: {e}")
            input("\n⏸️ Presiona Enter para continuar...")


if __name__ == "__main__":
    print("🎓 BOOTCAMP INGENIERÍA DE DATOS - CLASE 06")
    print("🧮 Manejo de Excepciones con Calculadora Avanzada")
    print("🎯 Try, Except, Else, Finally en acción")
    
    menu_principal()