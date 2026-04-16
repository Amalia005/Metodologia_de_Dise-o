from typing import List, Dict
from ventas.pedido import Pedido
from ventas.builder import PedidoBuilder
from operaciones.repartidor import Repartidor
from operaciones.asignador import AsignadorService
from soporte.incidencia import Incidencia

# ==========================================
# PATRÓN FACADE — Estructural
# SRP: unifica el acceso a todos los
#      subsistemas desde un solo punto
# ==========================================

class LogisticaFacade:
    def __init__(self, asignador: AsignadorService):
        self._pedidos: Dict[str, Pedido] = {}
        self._incidencias: List[Incidencia] = []
        self._asignador = asignador
        self._contador_incidencias = 0

    # CU1: Crear pedido
    def crear_pedido(self, id_pedido: str, canal: str,
                     origen: str, punto_origen: str,
                     destino: str, destinatario: str,
                     contacto: str, tipo_carga: str,
                     peso: float) -> Pedido:
        pedido = (PedidoBuilder(id_pedido, canal)
                  .con_origen(origen, punto_origen)
                  .con_destino(destino, destinatario, contacto)
                  .con_carga(tipo_carga, peso)
                  .build())
        self._pedidos[pedido.id] = pedido
        print(f"[Facade] Pedido {pedido.id} creado desde canal {canal}.")
        return pedido

    # CU2: Validar pedido
    def validar_pedido(self, id_pedido: str) -> None:
        pedido = self._pedidos.get(id_pedido)
        if pedido:
            pedido.validar()
        else:
            print(f"[Facade] Pedido {id_pedido} no encontrado.")

    # CU3: Asignar repartidor
    def asignar_repartidor(self, id_pedido: str) -> None:
        pedido = self._pedidos.get(id_pedido)
        if not pedido:
            print(f"[Facade] Pedido {id_pedido} no encontrado.")
            return
        repartidor = self._asignador.ejecutar_asignacion()
        if repartidor:
            pedido.asignar(repartidor.id)
        else:
            print(f"[Facade] No se pudo asignar repartidor al pedido {id_pedido}.")

    # CU4: Registrar y gestionar incidencia
    def registrar_incidencia(self, id_pedido: str, descripcion: str) -> None:
        self._contador_incidencias += 1
        incidencia = Incidencia(
            f"INC-{self._contador_incidencias:03d}",
            id_pedido,
            descripcion
        )
        self._incidencias.append(incidencia)
        print(f"[Facade] Incidencia {incidencia.id} registrada para pedido {id_pedido}.")

    def gestionar_incidencia(self, id_incidencia: str, resolucion: str) -> None:
        for inc in self._incidencias:
            if inc.id == id_incidencia:
                inc.analizar()
                inc.resolver(resolucion)
                return
        print(f"[Facade] Incidencia {id_incidencia} no encontrada.")

    # Reporte final
    def mostrar_estado(self) -> None:
        print("\n========= ESTADO DEL SISTEMA =========")
        print("--- Pedidos ---")
        for pedido in self._pedidos.values():
            print(f"  {pedido}")
        print("--- Incidencias ---")
        for inc in self._incidencias:
            print(f"  {inc}")
        print("=======================================\n")