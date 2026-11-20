# ARCHIVO 3: Clases del sistema.
# Aquí se conectan las excepciones.py y log_manager.py mediante import.
# main.py podrá usar estas clases gracias a: from modelos import ...

# MÓDULO DE MODELOS Y LÓGICA DE NEGOCIO (POO)
# ==========================================

from abc import ABC, abstractmethod # Herramientas de Python para crear clases y métodos abstractos
from datetime import datetime       # Librería para manejo de fechas y tiempos
from excepciones import ClienteInvalidoError, ServicioNoDisponibleError, ReservaInvalidaError
from log_manager import logger      # Importa el sistema de logs configurado previamente

# 1. CLASE ABSTRACTA BASE
class EntidadBase(ABC):
    """Clase abstracta general que representa cualquier entidad con identificador único."""
    def __init__(self, identificador: str):
        self._identificador = identificador # Atributo protegido

    @property
    def identificador(self):
        """Permite consultar de forma segura el identificador."""
        return self._identificador

    @abstractmethod
    def obtener_detalles(self) -> str:
        """Método abstracto que obliga a las clases hijas a implementar una descripción."""
        pass


# 2. CLASE CLIENTE CON ENCAPSULAMIENTO Y VALIDACIONES
class Cliente(EntidadBase):
    """Representa a un cliente de la empresa con validaciones estrictas en sus datos."""
    def __init__(self, identificador: str, nombre: str, correo: str, telefono: str):
        super().__init__(identificador) # Hereda el identificador de la clase base
        self.nombre = nombre       # Asigna validando mediante el setter
        self.correo = correo       # Asigna validando mediante el setter
        self.telefono = telefono   # Asigna validando mediante el setter

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        # Valida que el nombre no esté vacío ni lleno de espacios en blanco
        if not valor or not valor.strip():
            logger.error(f"Intento de registrar cliente con nombre inválido: '{valor}'")
            raise ClienteInvalidoError("El nombre del cliente no puede estar vacío.")
        self._nombre = valor.strip()

    @property
    def correo(self):
        return self._correo

    @correo.setter
    def correo(self, valor):
        # Valida que el correo contenga '@' y '.' básico
        if not valor or "@" not in valor or "." not in valor:
            logger.error(f"Intento de registrar cliente con correo inválido: '{valor}'")
            raise ClienteInvalidoError(f"El correo electrónico '{valor}' no tiene un formato válido.")
        self._correo = valor.strip()

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        # Valida que el teléfono tenga al menos 7 dígitos numéricos
        if not valor or not valor.isdigit() or len(valor) < 7:
            logger.error(f"Intento de registrar cliente con teléfono inválido: '{valor}'")
            raise ClienteInvalidoError(f"El teléfono '{valor}' debe contener solo dígitos y al menos 7 caracteres.")
        self._telefono = valor.strip()

    def obtener_detalles(self) -> str:
        """Implementa el método abstracto heredado de EntidadBase."""
        return f"Cliente [ID: {self.identificador}] - Nombre: {self.nombre}, Correo: {self.correo}, Teléfono: {self.telefono}"


# 3. CLASE ABSTRACTA SERVICIO Y POLIMORFISMO
class Servicio(EntidadBase, ABC):
    """Clase abstracta para los servicios que ofrece Software FJ."""
    def __init__(self, identificador: str, nombre_servicio: str, tarifa_base: float):
        super().__init__(identificador)
        self.nombre_servicio = nombre_servicio
        # Evitamos que se creen servicios con tarifas negativas o iguales a cero.
        # Esto permite que la operación 10 pruebe una excepción real.
        if tarifa_base <= 0:
            logger.error(f"Tarifa inválida para el servicio {identificador}: {tarifa_base}")
            raise ServicioNoDisponibleError("La tarifa del servicio debe ser mayor que cero.")
        self.tarifa_base = tarifa_base

    # Método con parámetros opcionales (simula sobrecarga de métodos)
    def calcular_costo(self, duracion_horas: float, descuento: float = 0.0, aplicar_impuesto: bool = True) -> float:
        """Calcula el costo total aplicando tarifa, duración, descuentos opcionales e IVA."""
        if duracion_horas <= 0:
            logger.error(f"Cálculo de costo fallido para servicio {self.identificador}: duración inválida ({duracion_horas}h)")
            raise ServicioNoDisponibleError("La duración del servicio debe ser mayor a 0 horas.")
        
        # El descuento se expresa como decimal: 0.10 equivale al 10 %.
        if not 0 <= descuento <= 1:
            logger.error(f"Descuento inválido para servicio {self.identificador}: {descuento}")
            raise ServicioNoDisponibleError("El descuento debe estar entre 0 y 1.")
        subtotal = self.tarifa_base * duracion_horas
        monto_descuento = subtotal * descuento
        total_parcial = subtotal - monto_descuento
        
        # Aplica 19% de impuesto si el parámetro es True
        impuestos = total_parcial * 0.19 if aplicar_impuesto else 0.0
        total_final = total_parcial + impuestos
        return round(total_final, 2)


# 4. CLASES DERIVADAS ESPECIALIZADAS (Herencia y Polimorfismo)
class ReservaSala(Servicio):
    def __init__(self, identificador: str, tarifa_base: float, capacidad: int):
        super().__init__(identificador, "Reserva de Sala", tarifa_base)
        self.capacidad = capacidad

    def obtener_detalles(self) -> str:
        return f"Servicio: {self.nombre_servicio} (Capacidad: {self.capacidad} personas) - Tarifa Base: ${self.tarifa_base}/h"


class AlquilerEquipo(Servicio):
    def __init__(self, identificador: str, tarifa_base: float, tipo_equipo: str):
        super().__init__(identificador, "Alquiler de Equipo", tarifa_base)
        self.tipo_equipo = tipo_equipo

    def obtener_detalles(self) -> str:
        return f"Servicio: {self.nombre_servicio} [Equipo: {self.tipo_equipo}] - Tarifa Base: ${self.tarifa_base}/h"


class AsesoriaEspecializada(Servicio):
    def __init__(self, identificador: str, tarifa_base: float, area_experiencia: str):
        super().__init__(identificador, "Asesoría Especializada", tarifa_base)
        self.area_experiencia = area_experiencia

    def obtener_detalles(self) -> str:
        return f"Servicio: {self.nombre_servicio} [Área: {self.area_experiencia}] - Tarifa Base: ${self.tarifa_base}/h"


# 5. CLASE RESERVA (Gestión integral con manejo avanzado de excepciones)
class Reserva:
    contador_reservas = 1 # Variable de clase para numerar automáticamente las reservas

    def __init__(self, cliente: Cliente, servicio: Servicio, duracion_horas: float, descuento: float = 0.0):
        self.codigo_reserva = f"RES-{Reserva.contador_reservas:03d}"
        Reserva.contador_reservas += 1
        # Verificamos que se reciban objetos del tipo esperado.
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("Debe seleccionar un cliente válido.")
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("Debe seleccionar un servicio válido.")
        self.cliente = cliente
        self.servicio = servicio
        self.duracion_horas = duracion_horas
        self.descuento = descuento
        self.estado = "Creada"
        self.costo_total = 0.0

    def procesar_reserva(self):
        """Procesa la reserva aplicando manejo robusto de excepciones (try/except/else/finally)."""
        try:
            logger.info(f"Iniciando procesamiento de reserva {self.codigo_reserva} para cliente {self.cliente.identificador}")
            if self.duracion_horas <= 0:
                raise ReservaInvalidaError("No se puede procesar una reserva con duración menor o igual a cero.")
            
            # Calcula el costo usando los métodos polimórficos de los servicios
            self.costo_total = self.servicio.calcular_costo(self.duracion_horas, self.descuento)
            self.estado = "Confirmada"
            logger.info(f"Reserva {self.codigo_reserva} confirmada exitosamente. Total: ${self.costo_total}")
            
        except Exception as e:
            # Captura cualquier error, cambia el estado y realiza encadenamiento de excepciones
            self.estado = "Fallida"
            logger.error(f"Error procesando la reserva {self.codigo_reserva}: {str(e)}")
            raise ReservaInvalidaError(f"Falla crítica en reserva {self.codigo_reserva}") from e
            
        else:
            # Se ejecuta únicamente si NO hubo ninguna excepción
            print(f"-> [ÉXITO] Reserva {self.codigo_reserva} procesada correctamente para {self.cliente.nombre}. Total a pagar: ${self.costo_total}")
            
        finally:
            # Se ejecuta SIEMPRE al final, sin importar si hubo éxito o error
            print(f"-> [FINALLY] Finalizada ejecución de procesamiento para reserva {self.codigo_reserva} (Estado actual: {self.estado})\n")

    def cancelar_reserva(self):
        """Permite cambiar el estado de una reserva a cancelada."""
        if self.estado == "Cancelada":
            logger.warning(f"Intento de cancelar la reserva {self.codigo_reserva} que ya estaba cancelada.")
            print(f"La reserva {self.codigo_reserva} ya se encontraba cancelada.")
        else:
            self.estado = "Cancelada"
            logger.info(f"Reserva {self.codigo_reserva} cancelada por solicitud del usuario.")
            print(f"-> [CANCELADA] La reserva {self.codigo_reserva} ha sido cancelada con éxito.")

# ==========================================
