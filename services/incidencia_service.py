from models.incidencia import Incidencia
from repositories.incidencia_repository import IncidenciaRepository
from repositories.pedido_repository import PedidoRepository


class IncidenciaService:
    """Facade: encapsula la lógica de registrar una incidencia,
    validando que el pedido exista antes de crearla."""

    def __init__(self):
        self._incidencia_repo = IncidenciaRepository()
        self._pedido_repo = PedidoRepository()

    def registrar_incidencia(self, datos):
        """Registra una incidencia asociada a un pedido existente."""
        pedido_id = datos.get('pedido_id')
        tipo = datos.get('tipo')
        descripcion = datos.get('descripcion')

        if not pedido_id or not tipo:
            raise ValueError("Los campos 'pedido_id' y 'tipo' son obligatorios.")

        pedido = self._pedido_repo.buscar_por_id(pedido_id)
        if pedido is None:
            raise KeyError(f"Pedido con id '{pedido_id}' no encontrado.")

        incidencia = Incidencia()
        incidencia.pedido_id = pedido_id
        incidencia.tipo = tipo
        incidencia.descripcion = descripcion

        self._incidencia_repo.guardar(incidencia)
        return incidencia
