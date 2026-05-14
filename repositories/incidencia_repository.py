# Base de datos simulada en memoria (objetos de dominio)
incidencias_db = {}


class IncidenciaRepository:

    def guardar(self, incidencia):
        """Guarda un objeto Incidencia en memoria."""
        incidencias_db[incidencia.id] = incidencia
        return incidencia

    def buscar_por_id(self, incidencia_id):
        """Busca una incidencia por su ID. Retorna None si no existe."""
        return incidencias_db.get(incidencia_id)
