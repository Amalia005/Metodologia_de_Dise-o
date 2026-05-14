from repositories.pedido_repository import PedidoRepository
from repositories.repartidor_repository import RepartidorRepository
from services.estrategia_asignacion import (
    EstrategiaAsignacion,
    AsignarPorMenorCarga,
    AsignarPorDisponibilidad
)

class AsignacionService:
    def __init__(self, estrategia: EstrategiaAsignacion = None):
        # DIP: Depende de la abstracción EstrategiaAsignacion
        self._estrategia = estrategia or AsignarPorMenorCarga()
        self._pedido_repo = PedidoRepository()
        self._repartidor_repo = RepartidorRepository()

    def set_estrategia(self, estrategia: EstrategiaAsignacion):
        self._estrategia = estrategia

    def asignar_pedido(self, pedido_id: str, tipo_estrategia: str = None):
        # Permite cambiar la estrategia dinámicamente si se solicita
        if tipo_estrategia == "disponibilidad":
            self._estrategia = AsignarPorDisponibilidad()
        elif tipo_estrategia == "menor_carga":
            self._estrategia = AsignarPorMenorCarga()

        # 1. Buscar el pedido
        pedido = self._pedido_repo.buscar_por_id(pedido_id)
        if not pedido:
            raise ValueError(f"Pedido con ID {pedido_id} no encontrado.")

        if pedido.get("estado") == "Asignado":
            raise ValueError(f"El pedido {pedido_id} ya tiene un repartidor asignado.")

        # 2. Obtener todos los repartidores (objetos de dominio)
        repartidores = self._repartidor_repo.buscar_todos()

        # 3. Aplicar el patrón Strategy para seleccionar el repartidor idóneo
        repartidor = self._estrategia.asignar(repartidores)
        if not repartidor:
            raise ValueError("No hay repartidores disponibles con capacidad en este momento.")

        # 4. Actualizar estado del repartidor (lógica de negocio interna)
        repartidor.asignar_pedido()
        self._repartidor_repo.actualizar(repartidor)

        # 5. Actualizar estado del pedido
        pedido["estado"] = "Asignado"
        pedido["repartidor_id"] = repartidor.id
        pedido_actualizado = self._pedido_repo.guardar(pedido)

        return pedido_actualizado
