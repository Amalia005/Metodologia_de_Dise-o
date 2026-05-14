from models.pedido import PedidoBuilder
from repositories.pedido_repository import PedidoRepository

repo = PedidoRepository()

class PedidoService:
    def crear_pedido(self, datos):
        # Validar datos mínimos requeridos
        if not datos.get('origen') or not datos.get('destinatario'):
            raise ValueError("Faltan datos mínimos: origen y destinatario son obligatorios.")

        # Construir el pedido usando el Patrón Builder
        builder = PedidoBuilder()
        pedido_obj = builder.set_origen(datos.get('origen')) \
                            .set_destinatario(datos.get('destinatario')) \
                            .set_canal(datos.get('canal', 'Web')) \
                            .build()

        # Guardar en el repositorio (lo guardamos como diccionario para el JSON)
        pedido_guardado = repo.guardar(pedido_obj.to_dict())
        return pedido_guardado