from repositories.pedido_repository import PedidoRepository
from repositories.repartidor_repository import RepartidorRepository
from services.estrategia_asignacion import (
    EstrategiaAsignacion,
    AsignarPorMenorCarga,
    AsignarPorDisponibilidad
)


class AsignacionService:
    def __init__(self, estrategia: EstrategiaAsignacion = None):
        self._estrategia = estrategia or AsignarPorMenorCarga()
        self._pedido_repo = PedidoRepository()
        self._repartidor_repo = RepartidorRepository()

    def asignar_pedido(self, pedido_id: str, tipo_estrategia: str = None):
        if tipo_estrategia == "disponibilidad":
            self._estrategia = AsignarPorDisponibilidad()
        elif tipo_estrategia == "menor_carga":
            self._estrategia = AsignarPorMenorCarga()

        # 1. Buscar el pedido
        pedido = self._pedido_repo.buscar_por_id(pedido_id)
        if not pedido:
            raise ValueError(f"Pedido con ID {pedido_id} no encontrado.")

        if pedido.estado == "Asignado":
            raise ValueError(f"El pedido {pedido_id} ya tiene un repartidor asignado.")

        # 2. Obtener repartidores
        repartidores = self._repartidor_repo.buscar_todos()

        # 3. Aplicar patrón Strategy
        repartidor = self._estrategia.asignar(repartidores)
        if not repartidor:
            raise ValueError("No hay repartidores disponibles con capacidad.")

        # 4. Actualizar repartidor
        repartidor.asignar_pedido()
        self._repartidor_repo.actualizar(repartidor)

        # 5. Cambiar estado del pedido usando el patrón State
        pedido.cambiar_estado("Asignado")
        pedido.repartidor_id = repartidor.id
        self._pedido_repo.guardar(pedido)

        return pedido