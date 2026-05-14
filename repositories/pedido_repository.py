# Base de datos simulada en memoria
pedidos_db = {}

class PedidoRepository:
    def guardar(self, pedido):
        # Guardamos el diccionario del pedido
        pedidos_db[pedido['id']] = pedido
        return pedido
        
    def buscar_por_id(self, pedido_id):
        return pedidos_db.get(pedido_id)