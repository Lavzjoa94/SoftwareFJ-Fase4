# =============================================================================
# SISTEMA INTEGRAL DE GESTIÓN DE CLIENTES, SERVICIOS Y RESERVAS
# EMPRESA SOFTWARE FJ
# FASE 4 - PROGRAMACIÓN ORIENTADA A OBJETOS
# =============================================================================

from abc import ABC, abstractmethod
import logging

# =============================================================================
# CONFIGURACIÓN DEL SISTEMA DE LOGS
# =============================================================================

logging.basicConfig(
    filename="software_fj.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    encoding="utf-8"
)

logger = logging.getLogger("SoftwareFJ")


# =============================================================================
# EXCEPCIONES PERSONALIZADAS
# =============================================================================

class SoftwareFJError(Exception):
    pass


class ValidationError(SoftwareFJError):
    pass


class OperationError(SoftwareFJError):
    pass


# =============================================================================
# CLASE ABSTRACTA ENTIDAD
# =============================================================================

class Entidad(ABC):

    @abstractmethod
    def validar(self):
        pass


# =============================================================================
# CLASE CLIENTE
# =============================================================================

class Cliente(Entidad):

    def __init__(self, nombre, correo, telefono):

        self.__nombre = nombre
        self.__correo = correo
        self.__telefono = telefono

        self.validar()

    @property
    def nombre(self):
        return self.__nombre

    @property
    def correo(self):
        return self.__correo

    @property
    def telefono(self):
        return self.__telefono

    def validar(self):

        if len(self.__nombre.strip()) < 3:
            raise ValidationError(
                "El nombre debe tener al menos 3 caracteres."
            )

        if "@" not in self.__correo:
            raise ValidationError(
                "Correo electrónico inválido."
            )

        if len(self.__telefono) < 10:
            raise ValidationError(
                "Número telefónico inválido."
            )

    def __str__(self):

        return (
            f"Cliente: {self.__nombre} | "
            f"Correo: {self.__correo} | "
            f"Teléfono: {self.__telefono}"
        )


# =============================================================================
# CLASE ABSTRACTA SERVICIO
# =============================================================================

class Servicio(ABC):

    def __init__(self, nombre, precio_base):

        self.nombre = nombre
        self.precio_base = precio_base

        self.validar()

    def validar(self):

        if len(self.nombre.strip()) < 3:
            raise ValidationError(
                "El nombre del servicio debe tener al menos 3 caracteres."
            )

        if self.precio_base <= 0:
            raise ValidationError(
                "El precio base debe ser mayor que cero."
            )

    @abstractmethod
    def calcular_costo(self):
        pass

    @abstractmethod
    def describir(self):
        pass


# =============================================================================
# SERVICIO DE RESERVA DE SALA
# =============================================================================

class ReservaSala(Servicio):

    def __init__(self, nombre, precio_base, capacidad):

        super().__init__(nombre, precio_base)

        self.capacidad = capacidad

    def calcular_costo(self):

        return self.precio_base + (self.capacidad * 5)

    def describir(self):

        return (
            f"Servicio: {self.nombre} | "
            f"Capacidad: {self.capacidad} personas"
        )


# =============================================================================
# SERVICIO DE ALQUILER DE EQUIPOS
# =============================================================================

class AlquilerEquipo(Servicio):

    def __init__(self, nombre, precio_base, dias):

        super().__init__(nombre, precio_base)

        self.dias = dias

    def calcular_costo(self):

        return self.precio_base * self.dias

    def describir(self):

        return (
            f"Servicio: {self.nombre} | "
            f"Días de alquiler: {self.dias}"
        )


# =============================================================================
# SERVICIO DE ASESORÍA ESPECIALIZADA
# =============================================================================

class Asesoria(Servicio):

    def __init__(self, nombre, precio_base, horas):

        super().__init__(nombre, precio_base)

        self.horas = horas

    def calcular_costo(self):

        return self.precio_base * self.horas

    def describir(self):

        return (
            f"Servicio: {self.nombre} | "
            f"Horas contratadas: {self.horas}"
        )


# =============================================================================
# CLASE RESERVA
# =============================================================================
# Relaciona un cliente con un servicio.
# Permite gestionar el estado de la reserva.
# =============================================================================

class Reserva:

    def __init__(self, cliente, servicio, duracion):

        if duracion <= 0:
            raise ValidationError(
                "La duración debe ser mayor que cero."
            )

        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion

        self.estado = "PENDIENTE"

    def confirmar(self):

        if self.estado == "CONFIRMADA":
            raise OperationError(
                "La reserva ya fue confirmada."
            )

        self.estado = "CONFIRMADA"

    def procesar(self):

        if self.estado != "CONFIRMADA":
            raise OperationError(
                "Solo se pueden procesar reservas confirmadas."
            )

        return self.servicio.calcular_costo()

    def __str__(self):

        return (
            f"Cliente: {self.cliente.nombre} | "
            f"Servicio: {self.servicio.nombre} | "
            f"Estado: {self.estado}"
        )


# =============================================================================
# PRUEBA DEL SISTEMA
# =============================================================================

if __name__ == "__main__":

    cliente = Cliente(
        "Luis Villada",
        "luis@email.com",
        "3001234567"
    )

    sala = ReservaSala(
        "Sala Premium",
        100,
        20
    )

    reserva = Reserva(
        cliente,
        sala,
        4
    )

    print(cliente)

    print("\n--- PRUEBA DE RESERVA ---")

    print(reserva)

    reserva.confirmar()

    print(reserva)

    print(
        "Costo:",
        reserva.procesar()
    )