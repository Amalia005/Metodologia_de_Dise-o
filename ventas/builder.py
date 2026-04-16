from ventas.pedido import Pedido

# ==========================================
# PATRÓN BUILDER — Creacional
# SRP: la construcción del pedido es
#      responsabilidad del Builder, no de Pedido
# ==========================================

class PedidoBuilder:
    """Construye un Pedido complejo paso a paso."""

    def __init__(self, id_pedido: str, canal: str):
        self._pedido = Pedido(id_pedido, canal)

    def con_origen(self, direccion: str, punto_origen: str):
        self._pedido.datos_origen = {
            "direccion": direccion,
            "punto_origen": punto_origen
        }
        return self

    def con_destino(self, direccion: str, destinatario: str, contacto: str):
        self._pedido.datos_destino = {
            "direccion": direccion,
            "destinatario": destinatario,
            "contacto": contacto
        }
        return self

    def con_carga(self, tipo: str, peso: float):
        self._pedido.tipo_carga = {
            "tipo": tipo,
            "peso": peso
        }
        return self

    def build(self) -> Pedido:
        return self._pedido