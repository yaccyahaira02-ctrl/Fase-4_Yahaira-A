# ARCHIVO 4: Punto de entrada del programa.
# Para ejecutar todo el proyecto, abra una terminal en esta carpeta y escriba:
# python main.py
# No es necesario ejecutar los otros tres archivos por separado.

# SCRIPT PRINCIPAL Y SIMULACIÓN DE 10 OPERACIONES
# ===========================================

from modelos import Cliente, ReservaSala, AlquilerEquipo, AsesoriaEspecializada, Reserva
from excepciones import SoftwareFJError
from log_manager import logger

def ejecutar_simulacion():
    print("=" * 60)
    print(" INICIO DE SIMULACIÓN - SISTEMA INTEGRAL SOFTWARE FJ ")
    print("=" * 60 + "\n")

    # Operación 1: Registro válido de un cliente y creación de servicio correcto
    try:
        print("--- Operación 1: Registro válido de Cliente y Sala ---")
        cli1 = Cliente("C001", "Carlos Pérez", "carlos.perez@email.com", "3104567890")
        sala1 = ReservaSala("S001", 50000.0, 15)
        print(cli1.obtener_detalles())
        print(sala1.obtener_detalles())
        logger.info("Operación 1 ejecutada con éxito.")
    except SoftwareFJError as err:
        print(f"Error controlado: {err}")

    # Operación 2: Intento fallido de registro de cliente con correo inválido (Prueba try/except)
    try:
        print("--- Operación 2: Intento fallido de registro (correo inválido) ---")
        cli_malo = Cliente("C002", "Ana Gómez", "correo-sin-arroba", "3201234567")
    except SoftwareFJError as err:
        print(f"-> Excepción capturada correctamente: {err}")

    # Operación 3: Creación de servicio de Alquiler de Equipo y cálculo de costos
    try:
        print("--- Operación 3: Alquiler de equipo y cálculo de costos con descuento ---")
        cli2 = Cliente("C003", "María Rodríguez", "maria.rodriguez@email.com", "3159876543")
        equipo1 = AlquilerEquipo("E001", 30000.0, "Proyector Láser 4K")
        reserva1 = Reserva(cli2, equipo1, duracion_horas=4.0, descuento=0.10)
        reserva1.procesar_reserva()
    except SoftwareFJError as err:
        print(f"Error en operación 3: {err}")

    # Operación 4: Asesoría especializada y prueba try/except/else/finally
    try:
        print("--- Operación 4: Asesoría especializada (Flujo try/except/else/finally) ---")
        cli3 = Cliente("C004", "Luis Torres", "luis.torres@email.com", "3112223344")
        asesoria1 = AsesoriaEspecializada("A001", 120000.0, "Seguridad Informática y Redes")
        reserva2 = Reserva(cli3, asesoria1, duracion_horas=2.5)
        reserva2.procesar_reserva()
    except SoftwareFJError as err:
        print(f"Error en operación 4: {err}")

    # Operación 5: Intento fallido de reserva con duración negativa (Excepción personalizada)
    try:
        print("--- Operación 5: Reserva fallida por duración negativa ---")
        reserva_erronea = Reserva(cli1, sala1, duracion_horas=-3.0)
        reserva_erronea.procesar_reserva()
    except SoftwareFJError as err:
        print(f"-> Excepción de reserva capturada con éxito: {err}")

    # Operación 6: Cancelación de una reserva existente
    try:
        print("--- Operación 6: Cancelación de reserva ---")
        reserva1.cancelar_reserva()
    except SoftwareFJError as err:
        print(f"Error al cancelar: {err}")

    # Operación 7: Validación de teléfono incorrecto en cliente
    try:
        print("--- Operación 7: Validación de teléfono inválido ---")
        cli_tel = Cliente("C005", "Sofia Ruiz", "sofia@email.com", "abc1234")
    except SoftwareFJError as err:
        print(f"-> Excepción de teléfono capturada: {err}")

    # Operación 8: Creación de sala con tarifa base estándar y alta capacidad
    try:
        print("--- Operación 8: Creación de Sala Ejecutiva y reserva rápida ---")
        sala_exec = ReservaSala("S002", 90000.0, 30)
        reserva3 = Reserva(cli3, sala_exec, duracion_horas=3.0, descuento=0.05)
        reserva3.procesar_reserva()
    except SoftwareFJError as err:
        print(f"Error en operación 8: {err}")

    # Operación 9: Validación de nombre de cliente vacío
    try:
        print("--- Operación 9: Validación de nombre vacío ---")
        cli_vacio = Cliente("C006", "   ", "vacio@email.com", "3100000000")
    except SoftwareFJError as err:
        print(f"-> Excepción de nombre capturada: {err}")

    # Operación 10: Operación múltiple con encadenamiento de excepciones
    try:
        print("--- Operación 10: Prueba de robustez y registro en logs ---")
        sala_fallida = ReservaSala("S999", -5000.0, 10)
    except SoftwareFJError as err:
        logger.error(f"Operación 10 detectó una tarifa inválida: {err}")
        print(f"-> Sistema estable ante anomalía en tarifa: {err}")

    print("\n" + "=" * 60)
    print(" SIMULACIÓN FINALIZADA. REVISE EL ARCHIVO 'logs/sistema_fj.log'. ")
    print("=" * 60)

if __name__ == "__main__":
    ejecutar_simulacion()
