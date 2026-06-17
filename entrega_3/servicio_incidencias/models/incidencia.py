import uuid
from datetime import datetime


class Incidencia:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.pedido_id = None
        self.tipo = None
        self.descripcion = None
        self.fecha = datetime.now().isoformat()
        # Campos opcionales según tipo de incidencia (ej. foto_url, direccion_corregida)
        # Aprovecha el esquema flexible de MongoDB para almacenar campos distintos por tipo
        self.datos_extra = {}

    def to_dict(self):
        resultado = {
            "id": self.id,
            "pedido_id": self.pedido_id,
            "tipo": self.tipo,
            "descripcion": self.descripcion,
            "fecha": self.fecha,
        }
        # Los campos opcionales se agregan al mismo nivel del documento
        resultado.update(self.datos_extra)
        return resultado
