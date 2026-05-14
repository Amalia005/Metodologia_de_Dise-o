import uuid

class Pedido:
    def __init__(self):
        self.id = str(uuid.uuid4()) # Genera un ID único automático
        self.origen = None
        self.destinatario = None
        self.canal = None
        self.estado = "Creado"

    def to_dict(self):
        return {
            "id": self.id,
            "origen": self.origen,
            "destinatario": self.destinatario,
            "canal": self.canal,
            "estado": self.estado
        }

class PedidoBuilder:
    def __init__(self):
        self.pedido = Pedido()

    def set_origen(self, origen):
        self.pedido.origen = origen
        return self

    def set_destinatario(self, destinatario):
        self.pedido.destinatario = destinatario
        return self

    def set_canal(self, canal):
        self.pedido.canal = canal
        return self

    def build(self):
        return self.pedido