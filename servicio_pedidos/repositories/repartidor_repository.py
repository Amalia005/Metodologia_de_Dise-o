from models.repartidor import Repartidor

# Base de datos simulada en memoria (objetos de dominio)
repartidores_db = {
    "REP-01": Repartidor("REP-01", capacidad_maxima=2),
    "REP-02": Repartidor("REP-02", capacidad_maxima=2),
}


class RepartidorRepository:

    def guardar(self, repartidor):
        """Guarda un objeto Repartidor en memoria."""
        repartidores_db[repartidor.id] = repartidor
        return repartidor

    def buscar_todos(self):
        """Retorna todos los repartidores como objetos de dominio."""
        return list(repartidores_db.values())

    def buscar_por_id(self, repartidor_id):
        """Busca un repartidor por su ID. Retorna None si no existe."""
        return repartidores_db.get(repartidor_id)

    def actualizar(self, repartidor):
        """Actualiza un repartidor existente en memoria."""
        repartidores_db[repartidor.id] = repartidor
        return repartidor
