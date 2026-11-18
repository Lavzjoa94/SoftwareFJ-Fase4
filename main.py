# =============================================================================
# SISTEMA INTEGRAL DE GESTIÓN DE CLIENTES, SERVICIOS Y RESERVAS
# EMPRESA SOFTWARE FJ
# FASE 4 - PROGRAMACIÓN ORIENTADA A OBJETOS
# =============================================================================

from abc import ABC, abstractmethod
import logging

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

    def calcular_costo_con_descuento(
        self,
        descuento=0,
        impuesto=0
    ):

        costo = self.precio_base

        if descuento > 0:
            costo -= costo * (descuento / 100)

        if impuesto > 0:
            costo += costo * (impuesto / 100)

        return round(costo, 2)

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

        logger.info(
            f"Reserva creada para {cliente.nombre}"
        )

    def confirmar(self):

        if self.estado == "CONFIRMADA":
            raise OperationError(
                "La reserva ya fue confirmada."
            )

        self.estado = "CONFIRMADA"

        logger.info(
            f"Reserva confirmada para {self.cliente.nombre}"
        )

    def cancelar(self):

        if self.estado == "CANCELADA":
            raise OperationError(
                "La reserva ya fue cancelada."
            )

        self.estado = "CANCELADA"

        logger.info(
            f"Reserva cancelada para {self.cliente.nombre}"
        )

    def procesar(self):

        if self.estado != "CONFIRMADA":
            raise OperationError(
                "Solo se pueden procesar reservas confirmadas."
            )

        costo = self.servicio.calcular_costo()

        logger.info(
            f"Reserva procesada correctamente. Costo: {costo}"
        )

        return costo

    def __str__(self):

        return (
            f"Cliente: {self.cliente.nombre} | "
            f"Servicio: {self.servicio.nombre} | "
            f"Estado: {self.estado}"
        )


# =============================================================================
# PRUEBAS DEL SISTEMA
# =============================================================================

if __name__ == "__main__":

    try:

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

        print("\n--- PRUEBA DE DESCUENTOS ---")

        print(
            "Costo con 10% descuento:",
            sala.calcular_costo_con_descuento(10)
        )

        print(
            "Costo con 10% descuento y 19% impuesto:",
            sala.calcular_costo_con_descuento(
                descuento=10,
                impuesto=19
            )
        )

        print("\n--- PRUEBA TRY / EXCEPT / ELSE ---")

        try:

            cliente_prueba = Cliente(
                "Carlos",
                "carlos@email.com",
                "3019998888"
            )

        except ValidationError as e:

            print(
                f"Error: {e}"
            )

        else:

            print(
                "Cliente registrado correctamente."
            )

        print("\n--- PRUEBA DE EXCEPCIONES ---")

        try:

            reserva.confirmar()

        except OperationError as e:

            print(
                f"Excepción controlada: {e}"
            )

        finally:

            print(
                "Bloque finally ejecutado."
            )

    except ValidationError as e:

        logger.error(str(e))

        print(
            f"Error de validación: {e}"
        )