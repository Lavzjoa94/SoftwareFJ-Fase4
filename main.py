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
# Todos los eventos importantes serán almacenados en el archivo:
# software_fj.log
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


# =============================================================================
# CLASE ABSTRACTA ENTIDAD
# =============================================================================
# Representa una entidad genérica del sistema.
# Todas las clases hijas deben implementar el método validar().
# =============================================================================

class Entidad(ABC):

    @abstractmethod
    def validar(self):
        pass


# =============================================================================
# CLASE CLIENTE
# =============================================================================
# Representa los clientes registrados en el sistema.
# Implementa encapsulación mediante atributos privados.
# =============================================================================

class Cliente(Entidad):

    def __init__(self, nombre, correo, telefono):

        self.__nombre = nombre
        self.__correo = correo
        self.__telefono = telefono

        self.validar()

        logger.info(
            f"Cliente registrado: {self.__nombre}"
        )

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
# Define el comportamiento común para todos los servicios.
# Toda clase hija debe implementar:
# - calcular_costo()
# - describir()
# =============================================================================

class Servicio(ABC):

    def __init__(self, nombre, precio_base):

        self.nombre = nombre
        self.precio_base = precio_base

        self.validar()

        logger.info(
            f"Servicio creado: {self.nombre}"
        )

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
# Permite gestionar reservas de salas para reuniones,
# capacitaciones y eventos.
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
# Permite alquilar equipos tecnológicos durante
# un número determinado de días.
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

    equipo = AlquilerEquipo(
        "Computador",
        50,
        3
    )

    print(cliente)

    print("\n--- SERVICIOS DISPONIBLES ---")

    print(sala.describir())
    print("Costo:", sala.calcular_costo())

    print()

    print(equipo.describir())
    print("Costo:", equipo.calcular_costo())