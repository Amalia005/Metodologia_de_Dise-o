import uuid
from abc import ABC, abstractmethod


# ==========================================
# PATRÓN STATE — Estados del pedido
# ==========================================

class EstadoPedido(ABC):
    """Clase abstracta que define el comportamiento de cada estado."""

    @abstractmethod
    def nombre(self) -> str:
        pass

    @abstractmethod
    def puede_transicionar_a(self, nuevo_estado: str) -> bool:
        pass


class EstadoCreado(EstadoPedido):
    def nombre(self) -> str:
        return "Creado"

    def puede_transicionar_a(self, nuevo_estado: str) -> bool:
        return nuevo_estado in ["Validado", "Cancelado"]


class EstadoValidado(EstadoPedido):
    def nombre(self) -> str:
        return "Validado"

    def puede_transicionar_a(self, nuevo_estado: str) -> bool:
        return nuevo_estado in ["Asignado", "Cancelado"]


class EstadoAsignado(EstadoPedido):
    def nombre(self) -> str:
        return "Asignado"

    def puede_transicionar_a(self, nuevo_estado: str) -> bool:
        return nuevo_estado in ["En Camino", "Cancelado"]


class EstadoEnCamino(EstadoPedido):
    def nombre(self) -> str:
        return "En Camino"

    def puede_transicionar_a(self, nuevo_estado: str) -> bool:
        return nuevo_estado in ["Entregado", "Cancelado"]


class EstadoEntregado(EstadoPedido):
    def nombre(self) -> str:
        return "Entregado"

    def puede_transicionar_a(self, nuevo_estado: str) -> bool:
        return False


class EstadoCancelado(EstadoPedido):
    def nombre(self) -> str:
        return "Cancelado"

    def puede_transicionar_a(self, nuevo_estado: str) -> bool:
        return False


ESTADOS = {
    "Creado": EstadoCreado,
    "Validado": EstadoValidado,
    "Asignado": EstadoAsignado,
    "En Camino": EstadoEnCamino,
    "Entregado": EstadoEntregado,
    "Cancelado": EstadoCancelado,
}


# ==========================================
# MODELO DE DOMINIO — Pedido
# ==========================================

class Pedido:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.origen = None
        self.destinatario = None
        self.canal = None
        self.repartidor_id = None
        self._estado = EstadoCreado()

    @property
    def estado(self):
        return self._estado.nombre()

    def cambiar_estado(self, nuevo_estado: str):
        """Cambia el estado del pedido si la transición es válida."""
        if nuevo_estado not in ESTADOS:
            raise ValueError(f"Estado '{nuevo_estado}' no es un estado válido.")

        if not self._estado.puede_transicionar_a(nuevo_estado):
            raise ValueError(
                f"No se puede pasar de '{self._estado.nombre()}' a '{nuevo_estado}'."
            )

        self._estado = ESTADOS[nuevo_estado]()

    def to_dict(self):
        return {
            "id": self.id,
            "origen": self.origen,
            "destinatario": self.destinatario,
            "canal": self.canal,
            "estado": self.estado,
            "repartidor_id": self.repartidor_id,
        }


# ==========================================
# PATRÓN BUILDER — Construcción de pedidos
# ==========================================

class PedidoBuilder:
    def __init__(self):
        self.pedido = Pedido()

    def set_origen(self, origen):
        self.pedido.origen = origen
        return self

    def set_destinatario(self, destinatario):
        self.pedido.destinatario = destinatario
        return self

    def set_canal(self, canal):
        self.pedido.canal = canal
        return self

    def build(self):
        return self.pedido