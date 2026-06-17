# ==========================================
# ENTIDAD: Repartidor
# SRP: solo gestiona datos del repartidor
# ==========================================

class Repartidor:
    def __init__(self, id_repartidor: str, capacidad_maxima: int = 2):
        self.id = id_repartidor
        self.capacidad_maxima = capacidad_maxima
        self.pedidos_asignados = 0
        self.disponible = True

    def tiene_capacidad(self) -> bool:
        return self.disponible and self.pedidos_asignados < self.capacidad_maxima

    def asignar_pedido(self) -> None:
        self.pedidos_asignados += 1
        if self.pedidos_asignados >= self.capacidad_maxima:
            self.disponible = False

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "capacidad_maxima": self.capacidad_maxima,
            "pedidos_asignados": self.pedidos_asignados,
            "disponible": self.disponible
        }

    @classmethod
    def from_dict(cls, data: dict):
        rep = cls(data["id"], data.get("capacidad_maxima", 2))
        rep.pedidos_asignados = data.get("pedidos_asignados", 0)
        rep.disponible = data.get("disponible", True)
        return rep

    def __str__(self):
        return (f"Repartidor {self.id} "
                f"| Pedidos: {self.pedidos_asignados}/{self.capacidad_maxima} "
                f"| Disponible: {self.disponible}")
