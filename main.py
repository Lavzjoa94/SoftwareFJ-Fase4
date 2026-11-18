# =============================================================================
# SISTEMA INTEGRAL DE GESTIÓN DE CLIENTES, SERVICIOS Y RESERVAS
# EMPRESA SOFTWARE FJ
# FASE 4 - PROGRAMACIÓN ORIENTADA A OBJETOS
# =============================================================================

"""
Este sistema permite gestionar clientes, servicios y reservas
sin utilizar bases de datos.

Conceptos aplicados:

- Abstracción
- Encapsulación
- Herencia
- Polimorfismo
- Sobrecarga simulada
- Excepciones personalizadas
- Encadenamiento de excepciones
- Manejo de logs
- Manejo avanzado de excepciones
"""

from abc import ABC, abstractmethod
import logging


# =============================================================================
# CONFIGURACIÓN DEL SISTEMA DE LOGS
# =============================================================================
# Todos los eventos importantes del sistema serán almacenados
# en el archivo software_fj.log.
#
# Se registran:
# - Clientes creados.
# - Servicios creados.
# - Reservas creadas.
# - Confirmaciones.
# - Cancelaciones.
# - Procesamientos.
# - Errores.
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
    """
    Excepción base del sistema.

    Todas las excepciones personalizadas
    heredan de esta clase.
    """
    pass


class ValidationError(SoftwareFJError):
    """
    Se utiliza cuando los datos ingresados
    no cumplen las reglas de validación.
    """
    pass


class OperationError(SoftwareFJError):
    """
    Se genera cuando se intenta realizar
    una operación no permitida según el
    estado actual del sistema.
    """
    pass


# =============================================================================
# CLASE ABSTRACTA ENTIDAD
# =============================================================================
# Representa cualquier entidad del sistema.
#
# Todas las clases derivadas deben implementar
# el método validar().
# =============================================================================

class Entidad(ABC):

    @abstractmethod
    def validar(self):
        pass


# =============================================================================
# CLASE CLIENTE
# =============================================================================
# Representa los clientes registrados en Software FJ.
#
# Implementa:
# - Encapsulación.
# - Validación de datos.
# - Registro en logs.
# =============================================================================

class Cliente(Entidad):

    def __init__(self, nombre, correo, telefono):

        # Atributos privados.
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

        # Validación del nombre.
        if len(self.__nombre.strip()) < 3:
            raise ValidationError(
                "El nombre debe tener al menos 3 caracteres."
            )

        # Validación del correo electrónico.
        if "@" not in self.__correo:
            raise ValidationError(
                "Correo electrónico inválido."
            )

        # Validación del teléfono.
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
#
# Toda clase derivada debe implementar:
# - calcular_costo()
# - describir()
#
# Esta clase demuestra abstracción y polimorfismo.
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

    # =========================================================================
    # SOBRECARGA SIMULADA
    # =========================================================================
    # Utiliza parámetros opcionales para calcular un costo
    # aplicando descuentos e impuestos.
    # =========================================================================

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
# Permite reservar salas para reuniones,
# capacitaciones o eventos.
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
# Permite alquilar equipos tecnológicos.
#
# El costo depende del número de días.
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
# Servicio profesional contratado por horas.
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
#
# Funcionalidades:
# - Confirmar reserva.
# - Cancelar reserva.
# - Procesar reserva.
# - Validar duración.
# - Controlar estados.
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

    # Confirma una reserva.
    def confirmar(self):

        if self.estado == "CONFIRMADA":
            raise OperationError(
                "La reserva ya fue confirmada."
            )

        self.estado = "CONFIRMADA"

        logger.info(
            f"Reserva confirmada para {self.cliente.nombre}"
        )

    # Cancela una reserva.
    def cancelar(self):

        if self.estado == "CANCELADA":
            raise OperationError(
                "La reserva ya fue cancelada."
            )

        self.estado = "CANCELADA"

        logger.info(
            f"Reserva cancelada para {self.cliente.nombre}"
        )

    # Procesa una reserva confirmada.
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

    # =========================================================================
    # ENCADENAMIENTO DE EXCEPCIONES
    # =========================================================================
    # Demuestra la utilización de:
    #
    # raise ValidationError(...) from e
    #
    # exigida por la actividad.
    # =========================================================================

    def validar_duracion_texto(self, valor):

        try:

            return int(valor)

        except ValueError as e:

            raise ValidationError(
                "La duración debe ser un número entero."
            ) from e

    def __str__(self):

        return (
            f"Cliente: {self.cliente.nombre} | "
            f"Servicio: {self.servicio.nombre} | "
            f"Estado: {self.estado}"
        )


# =============================================================================
# PRUEBAS DEL SISTEMA
# =============================================================================
# En esta sección se ejecutan pruebas válidas e inválidas
# para demostrar el funcionamiento del sistema.
# =============================================================================

if __name__ == "__main__":

    try:

        # ---------------------------------------------------------------------
        # CREACIÓN DE CLIENTE
        # ---------------------------------------------------------------------

        cliente = Cliente(
            "Luis Villada",
            "luis@email.com",
            "3001234567"
        )

        # ---------------------------------------------------------------------
        # CREACIÓN DE SERVICIO
        # ---------------------------------------------------------------------

        sala = ReservaSala(
            "Sala Premium",
            100,
            20
        )

        # ---------------------------------------------------------------------
        # CREACIÓN DE RESERVA
        # ---------------------------------------------------------------------

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

        # ---------------------------------------------------------------------
        # SOBRECARGA SIMULADA
        # ---------------------------------------------------------------------

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

        # ---------------------------------------------------------------------
        # TRY / EXCEPT / ELSE
        # ---------------------------------------------------------------------

        print("\n--- PRUEBA TRY / EXCEPT / ELSE ---")

        try:

            Cliente(
                "Carlos",
                "carlos@email.com",
                "3019998888"
            )

        except ValidationError as e:

            print(f"Error: {e}")

        else:

            print(
                "Cliente registrado correctamente."
            )

        # ---------------------------------------------------------------------
        # ENCADENAMIENTO DE EXCEPCIONES
        # ---------------------------------------------------------------------

        print("\n--- PRUEBA DE ENCADENAMIENTO DE EXCEPCIONES ---")

        try:

            reserva.validar_duracion_texto("abc")

        except ValidationError as e:

            print(
                f"Error encadenado: {e}"
            )

        # ---------------------------------------------------------------------
        # VALIDACIONES INVÁLIDAS
        # ---------------------------------------------------------------------

        print("\n--- PRUEBAS DE VALIDACIÓN DE DATOS ---")

        try:

            Cliente(
                "Lu",
                "luis@email.com",
                "3001234567"
            )

        except ValidationError as e:

            print(
                f"Validación nombre: {e}"
            )

        try:

            Cliente(
                "Luis Villada",
                "correoinvalido",
                "3001234567"
            )

        except ValidationError as e:

            print(
                f"Validación correo: {e}"
            )

        try:

            Cliente(
                "Luis Villada",
                "luis@email.com",
                "123"
            )

        except ValidationError as e:

            print(
                f"Validación teléfono: {e}"
            )

        try:

            Reserva(
                cliente,
                sala,
                0
            )

        except ValidationError as e:

            print(
                f"Validación reserva: {e}"
            )

        # ---------------------------------------------------------------------
        # TRY / EXCEPT / FINALLY
        # ---------------------------------------------------------------------

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