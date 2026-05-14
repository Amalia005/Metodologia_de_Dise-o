# Base de datos simulada en memoria
pedidos_db = {}


class PedidoRepository:

    def guardar(self, pedido):
        """Guarda un objeto Pedido en memoria."""
        pedidos_db[pedido.id] = pedido
        return pedido

    def buscar_por_id(self, pedido_id):
        """Busca un pedido por su ID. Retorna None si no existe."""
        return pedidos_db.get(pedido_id)