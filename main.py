# =============================================================================
# SISTEMA INTEGRAL DE GESTIÓN DE CLIENTES, SERVICIOS Y RESERVAS
# EMPRESA SOFTWARE FJ
# FASE 4 - PROGRAMACIÓN ORIENTADA A OBJETOS
# =============================================================================

# Permite crear clases abstractas.
from abc import ABC, abstractmethod

# Permite registrar eventos en archivos de log.
import logging


# =============================================================================
# CONFIGURACIÓN DEL SISTEMA DE LOGS
# =============================================================================
# Todos los eventos importantes quedan almacenados en el archivo:
# software_fj.log

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

# Excepción base del sistema.
class SoftwareFJError(Exception):
    pass


# Excepción utilizada para errores de validación.
class ValidationError(SoftwareFJError):
    pass


# =============================================================================
# CLASE ABSTRACTA ENTIDAD
# =============================================================================

class Entidad(ABC):

    @abstractmethod
    def validar(self):
        pass


# =============================================================================
# PRUEBA DEL SISTEMA
# =============================================================================

if __name__ == "__main__":

    print("Configuración inicial completada")