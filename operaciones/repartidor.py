# ==========================================
# ENTIDAD: Repartidor
# SRP: solo gestiona datos del repartidor
# SUPUESTO: capacidad es un número entero simple
# ==========================================

class Repartidor:
    def __init__(self, id_repartidor: str, capacidad_maxima: int):
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

    def __str__(self):
        return (f"Repartidor {self.id} "
                f"| Pedidos: {self.pedidos_asignados}/{self.capacidad_maxima} "
                f"| Disponible: {self.disponible}")