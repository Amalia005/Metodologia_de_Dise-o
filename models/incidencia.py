import uuid
from datetime import datetime


class Incidencia:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.pedido_id = None
        self.tipo = None
        self.descripcion = None
        self.fecha = datetime.now().isoformat()

    def to_dict(self):
        return {
            "id": self.id,
            "pedido_id": self.pedido_id,
            "tipo": self.tipo,
            "descripcion": self.descripcion,
            "fecha": self.fecha,
        }
