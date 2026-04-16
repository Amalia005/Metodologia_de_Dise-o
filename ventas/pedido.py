from abc import ABC, abstractmethod

# ==========================================
# PATRÓN STATE — Comportamiento
# SRP: cada estado tiene su propia clase
# LSP: todos los estados son intercambiables
# ==========================================

class EstadoPedido(ABC):
    """Interfaz base para todos los estados del pedido."""
    @abstractmethod
    def validar(self, pedido) -> None:
        pass

    @abstractmethod
    def asignar(self, pedido, repartidor_id: str) -> None:
        pass

    @abstractmethod
    def cancelar(self, pedido) -> None:
        pass

    @abstractmethod
    def nombre(self) -> str:
        pass


class EstadoCreado(EstadoPedido):
    def validar(self, pedido) -> None:
        print(f"[Estado] Pedido {pedido.id} validado correctamente.")
        pedido._estado = EstadoValidado()

    def asignar(self, pedido, repartidor_id: str) -> None:
        print(f"[Error] Pedido {pedido.id} no puede asignarse sin validar primero.")

    def cancelar(self, pedido) -> None:
        print(f"[Estado] Pedido {pedido.id} cancelado.")
        pedido._estado = EstadoCancelado()

    def nombre(self) -> str:
        return "Creado"


class EstadoValidado(EstadoPedido):
    def validar(self, pedido) -> None:
        print(f"[Error] Pedido {pedido.id} ya está validado.")

    def asignar(self, pedido, repartidor_id: str) -> None:
        pedido.repartidor_asignado = repartidor_id
        print(f"[Estado] Pedido {pedido.id} asignado a {repartidor_id}.")
        pedido._estado = EstadoAsignado()

    def cancelar(self, pedido) -> None:
        print(f"[Estado] Pedido {pedido.id} cancelado.")
        pedido._estado = EstadoCancelado()

    def nombre(self) -> str:
        return "Validado"


class EstadoAsignado(EstadoPedido):
    def validar(self, pedido) -> None:
        print(f"[Error] Pedido {pedido.id} ya fue validado y asignado.")

    def asignar(self, pedido, repartidor_id: str) -> None:
        pedido.repartidor_asignado = repartidor_id
        print(f"[Estado] Pedido {pedido.id} reasignado a {repartidor_id}.")

    def cancelar(self, pedido) -> None:
        print(f"[Estado] Pedido {pedido.id} cancelado.")
        pedido._estado = EstadoCancelado()

    def nombre(self) -> str:
        return "Asignado"


class EstadoCancelado(EstadoPedido):
    def validar(self, pedido) -> None:
        print(f"[Error] Pedido {pedido.id} está cancelado, no puede continuar.")

    def asignar(self, pedido, repartidor_id: str) -> None:
        print(f"[Error] Pedido {pedido.id} está cancelado, no puede asignarse.")

    def cancelar(self, pedido) -> None:
        print(f"[Error] Pedido {pedido.id} ya está cancelado.")

    def nombre(self) -> str:
        return "Cancelado"


# ==========================================
# ENTIDAD: Pedido — Aggregate Root
# OCP: los estados se extienden sin modificar Pedido
# DIP: Pedido depende de EstadoPedido (abstracción)
# ==========================================

class Pedido:
    def __init__(self, id_pedido: str, canal: str):
        self.id = id_pedido
        self.canal = canal
        self.datos_origen = None
        self.datos_destino = None
        self.tipo_carga = None
        self.repartidor_asignado = None
        self._estado: EstadoPedido = EstadoCreado()

    @property
    def estado(self) -> str:
        return self._estado.nombre()

    def validar(self) -> None:
        self._estado.validar(self)

    def asignar(self, repartidor_id: str) -> None:
        self._estado.asignar(self, repartidor_id)

    def cancelar(self) -> None:
        self._estado.cancelar(self)

    def __str__(self):
        return (f"Pedido {self.id} | Canal: {self.canal} "
                f"| Estado: {self.estado} "
                f"| Repartidor: {self.repartidor_asignado or 'N/A'}")