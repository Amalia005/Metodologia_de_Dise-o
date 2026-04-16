# ==========================================
# ENTIDAD: Incidencia
# SRP: solo gestiona el ciclo de vida
#      de una incidencia
# ==========================================

class Incidencia:
    def __init__(self, id_incidencia: str, id_pedido: str, descripcion: str):
        self.id = id_incidencia
        self.id_pedido = id_pedido
        self.descripcion = descripcion
        self.estado = "Abierta"
        self.resolucion = None

    def analizar(self) -> None:
        if self.estado == "Abierta":
            self.estado = "En análisis"
            print(f"[Incidencia] {self.id} en análisis.")
        else:
            print(f"[Incidencia] {self.id} no puede pasar a análisis desde {self.estado}.")

    def resolver(self, resolucion: str) -> None:
        if self.estado == "En análisis":
            self.resolucion = resolucion
            self.estado = "Resuelta"
            print(f"[Incidencia] {self.id} resuelta: {resolucion}")
        else:
            print(f"[Incidencia] {self.id} debe estar en análisis para resolverse.")

    def __str__(self):
        return (f"Incidencia {self.id} "
                f"| Pedido: {self.id_pedido} "
                f"| Estado: {self.estado} "
                f"| Resolución: {self.resolucion or 'Pendiente'}")