from abc import ABC, abstractmethod
from typing import List, Optional
from models.repartidor import Repartidor

# ==========================================
# PATRÓN STRATEGY — Capa de Servicios
# OCP: Permite añadir nuevas estrategias de
#      asignación sin alterar el servicio principal.
# DIP: Depende de abstracciones y no de
#      implementaciones concretas.
# ==========================================

class EstrategiaAsignacion(ABC):
    """Interfaz base para las estrategias de asignación de repartidores."""
    @abstractmethod
    def asignar(self, repartidores: List[Repartidor]) -> Optional[Repartidor]:
        pass


class AsignarPorDisponibilidad(EstrategiaAsignacion):
    """Asigna al primer repartidor que tenga capacidad disponible."""
    def asignar(self, repartidores: List[Repartidor]) -> Optional[Repartidor]:
        for repartidor in repartidores:
            if repartidor.tiene_capacidad():
                return repartidor
        return None


class AsignarPorMenorCarga(EstrategiaAsignacion):
    """Asigna al repartidor disponible que tenga la menor cantidad de pedidos asignados."""
    def asignar(self, repartidores: List[Repartidor]) -> Optional[Repartidor]:
        disponibles = [r for r in repartidores if r.tiene_capacidad()]
        if not disponibles:
            return None
        return min(disponibles, key=lambda r: r.pedidos_asignados)
