from models.pedido import PedidoBuilder
from repositories.pedido_repository import PedidoRepository

repo = PedidoRepository()


class PedidoService:

    def crear_pedido(self, datos):
        """Crea un pedido nuevo usando el patrón Builder."""
        if not datos.get('origen') or not datos.get('destinatario'):
            raise ValueError("Faltan datos mínimos: origen y destinatario son obligatorios.")

        builder = PedidoBuilder()
        pedido = builder.set_origen(datos.get('origen')) \
                        .set_destinatario(datos.get('destinatario')) \
                        .set_canal(datos.get('canal', 'Web')) \
                        .build()

        repo.guardar(pedido)
        return pedido

    def cambiar_estado(self, pedido_id, nuevo_estado):
        """Cambia el estado de un pedido aplicando el patrón State."""
        pedido = repo.buscar_por_id(pedido_id)

        if pedido is None:
            raise KeyError(f"Pedido con id '{pedido_id}' no encontrado.")

        pedido.cambiar_estado(nuevo_estado)
        repo.guardar(pedido)
        return pedido