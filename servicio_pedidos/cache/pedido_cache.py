import time

# ==========================================
# CACHÉ EN MEMORIA — Estado de pedidos
# Invalidación inmediata por cambio de estado
# (no usa TTL ni expiración por tiempo).
# ==========================================


class PedidoCache:
    """Caché simple en memoria {pedido_id: pedido_dict}.
    Se invalida automáticamente cuando el patrón State
    ejecuta una transición de estado sobre el pedido."""

    def __init__(self):
        self._cache = {}

    def obtener(self, pedido_id):
        """Retorna el pedido cacheado o None. Loguea HIT/MISS."""
        if pedido_id in self._cache:
            print(f"  [CACHE HIT] Pedido {pedido_id} servido desde caché")
            return self._cache[pedido_id]
        print(f"  [CACHE MISS] Pedido {pedido_id} no encontrado en caché")
        return None

    def guardar(self, pedido_id, pedido_dict):
        """Almacena un pedido en el caché."""
        self._cache[pedido_id] = pedido_dict

    def invalidar(self, pedido_id):
        """Elimina un pedido del caché (disparado por cambio de estado)."""
        if pedido_id in self._cache:
            del self._cache[pedido_id]
            print(f"  [CACHE INVALIDADO] Pedido {pedido_id} eliminado del caché")


# Instancia singleton del caché
pedido_cache = PedidoCache()
