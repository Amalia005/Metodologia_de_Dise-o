from abc import ABC, abstractmethod
from typing import List
from operaciones.repartidor import Repartidor

# ==========================================
# PATRÓN STRATEGY — Comportamiento
# OCP: se pueden agregar nuevas estrategias
#      sin modificar el asignador
# DIP: AsignadorService depende de la
#      abstracción EstrategiaAsignacion
# ==========================================

class EstrategiaAsignacion(ABC):
    """Interfaz base para estrategias de asignación."""
    @abstractmethod
    def asignar(self, repartidores: List[Repartidor]) -> Repartidor:
        pass


class AsignarPorDisponibilidad(EstrategiaAsignacion):
    """Asigna el primer repartidor disponible."""
    def asignar(self, repartidores: List[Repartidor]) -> Repartidor:
        for repartidor in repartidores:
            if repartidor.tiene_capacidad():
                return repartidor
        return None


class AsignarPorMenorCarga(EstrategiaAsignacion):
    """Asigna el repartidor con menos pedidos asignados."""
    def asignar(self, repartidores: List[Repartidor]) -> Repartidor:
        disponibles = [r for r in repartidores if r.tiene_capacidad()]
        if not disponibles:
            return None
        return min(disponibles, key=lambda r: r.pedidos_asignados)


# ==========================================
# SERVICIO: AsignadorService
# SRP: solo se encarga de la lógica de asignación
# ==========================================

class AsignadorService:
    def __init__(self, estrategia: EstrategiaAsignacion):
        self._estrategia = estrategia
        self._repartidores: List[Repartidor] = []

    def agregar_repartidor(self, repartidor: Repartidor) -> None:
        self._repartidores.append(repartidor)

    def ejecutar_asignacion(self) -> Repartidor:
        repartidor = self._estrategia.asignar(self._repartidores)
        if repartidor:
            repartidor.asignar_pedido()
            print(f"[Asignador] Repartidor seleccionado: {repartidor.id}")
        else:
            print("[Asignador] No hay repartidores disponibles.")
        return repartidor