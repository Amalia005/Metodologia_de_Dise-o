from models.repartidor import Repartidor

# Base de datos simulada en memoria
repartidores_db = {
    "REP-01": {
        "id": "REP-01",
        "capacidad_maxima": 2,
        "pedidos_asignados": 0,
        "disponible": True
    },
    "REP-02": {
        "id": "REP-02",
        "capacidad_maxima": 2,
        "pedidos_asignados": 0,
        "disponible": True
    }
}

class RepartidorRepository:
    def guardar(self, repartidor_dict):
        repartidores_db[repartidor_dict['id']] = repartidor_dict
        return repartidor_dict

    def buscar_todos(self):
        # Convertimos los diccionarios a objetos Repartidor para que el Strategy
        # pueda invocar sus métodos de negocio (tiene_capacidad, etc.)
        return [Repartidor.from_dict(datos) for datos in repartidores_db.values()]

    def buscar_por_id(self, repartidor_id):
        datos = repartidores_db.get(repartidor_id)
        if datos:
            return Repartidor.from_dict(datos)
        return None

    def actualizar(self, repartidor_obj: Repartidor):
        # Actualiza la base de datos convirtiendo el objeto modificado a diccionario
        dict_data = repartidor_obj.to_dict()
        repartidores_db[repartidor_obj.id] = dict_data
        return dict_data
