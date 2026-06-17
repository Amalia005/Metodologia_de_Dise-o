import time
from models.pedido import PedidoBuilder
from repositories.pedido_repository import PedidoRepository
from cache.pedido_cache import pedido_cache
from messaging import cola_asignacion, topico_entregado

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
        """Cambia el estado de un pedido aplicando el patrón State.

        Efectos secundarios según el nuevo estado:
        - Validado: publica mensaje en cola 'asignación-repartidor'
        - Entregado: publica evento en tópico 'pedido-entregado'
        - Cancelado: no publica ningún evento
        - Cualquier transición: invalida el caché del pedido
        """
        pedido = repo.buscar_por_id(pedido_id)

        if pedido is None:
            raise KeyError(f"Pedido con id '{pedido_id}' no encontrado.")

        pedido.cambiar_estado(nuevo_estado)
        repo.guardar(pedido)

        # Invalidar caché tras cambio de estado
        pedido_cache.invalidar(pedido_id)

        # Publicar eventos según el nuevo estado
        if nuevo_estado == "Validado":
            cola_asignacion.publicar(pedido_id)
        elif nuevo_estado == "Entregado":
            topico_entregado.publicar(pedido_id)
        # Cancelado NO publica ningún evento

        return pedido

    def obtener_pedido(self, pedido_id):
        """Obtiene un pedido, consultando caché primero y luego SQLite.
        Loguea tiempos de respuesta para demostrar la eficacia del caché."""
        inicio = time.time()

        # 1. Intentar desde caché
        cached = pedido_cache.obtener(pedido_id)
        if cached is not None:
            elapsed_ms = (time.time() - inicio) * 1000
            print(f"[TIMING] GET /pedidos/{pedido_id} → {elapsed_ms:.3f}ms (desde caché)")
            return cached

        # 2. No estaba en caché → consultar SQLite
        pedido = repo.buscar_por_id(pedido_id)
        if pedido is None:
            raise KeyError(f"Pedido con id '{pedido_id}' no encontrado.")

        pedido_dict = pedido.to_dict()

        # 3. Guardar en caché para próximas consultas
        pedido_cache.guardar(pedido_id, pedido_dict)

        elapsed_ms = (time.time() - inicio) * 1000
        print(f"[TIMING] GET /pedidos/{pedido_id} → {elapsed_ms:.3f}ms (desde SQLite)")
        return pedido_dict
