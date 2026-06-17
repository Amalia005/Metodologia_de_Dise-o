import mongomock

# ==========================================
# REPOSITORIO DE INCIDENCIAS — Persistencia MongoDB
# Decisión arquitectónica: MongoDB (simulado con mongomock)
# para aprovechar esquema flexible de documentos.
# Cada incidencia se guarda como documento, permitiendo
# campos opcionales distintos según tipo (foto_url para
# paquete dañado, direccion_corregida para dirección
# incorrecta, etc.)
# ==========================================

# Cliente MongoDB simulado en memoria (misma interfaz que pymongo)
client = mongomock.MongoClient()
db = client.logistica_incidencias
collection = db.incidencias


class IncidenciaRepository:

    def guardar(self, incidencia):
        """Guarda una incidencia como documento MongoDB."""
        collection.insert_one(incidencia.to_dict())
        return incidencia

    def buscar_por_id(self, incidencia_id):
        """Busca una incidencia por su ID. Retorna el documento o None."""
        doc = collection.find_one({"id": incidencia_id}, {"_id": 0})
        return doc

    def buscar_todas(self):
        """Retorna todas las incidencias como lista de documentos."""
        return list(collection.find({}, {"_id": 0}))
