from models.incidencia import Incidencia
from repositories.incidencia_repository import IncidenciaRepository
from messaging.suscriptor_entregado import esta_habilitado


class IncidenciaService:
    """Servicio de gestión de incidencias.
    Valida que el pedido esté en estado Entregado (vía el set
    alimentado por el suscriptor del tópico) antes de permitir
    registrar una incidencia.
    Ya NO accede a PedidoRepository (es otro servicio)."""

    def __init__(self):
        self._repo = IncidenciaRepository()

    def registrar_incidencia(self, datos):
        """Registra una incidencia asociada a un pedido entregado.

        Soporta campos opcionales según tipo de incidencia:
        - 'paquete_dañado': acepta campo 'foto_url'
        - 'direccion_incorrecta': acepta campo 'direccion_corregida'
        """
        pedido_id = datos.get('pedido_id')
        tipo = datos.get('tipo')
        descripcion = datos.get('descripcion')

        if not pedido_id or not tipo:
            raise ValueError("Los campos 'pedido_id' y 'tipo' son obligatorios.")

        # Validar que el pedido esté habilitado (estado Entregado)
        if not esta_habilitado(pedido_id):
            raise ValueError(
                f"El pedido '{pedido_id}' no está en estado Entregado. "
                "Solo se pueden registrar incidencias para pedidos que ya fueron entregados."
            )

        incidencia = Incidencia()
        incidencia.pedido_id = pedido_id
        incidencia.tipo = tipo
        incidencia.descripcion = descripcion

        # Campos opcionales según tipo de incidencia (esquema flexible MongoDB)
        if tipo == "paquete_dañado" and datos.get('foto_url'):
            incidencia.datos_extra['foto_url'] = datos['foto_url']
        elif tipo == "direccion_incorrecta" and datos.get('direccion_corregida'):
            incidencia.datos_extra['direccion_corregida'] = datos['direccion_corregida']

        # Cualquier campo extra adicional que venga en los datos
        campos_conocidos = {'pedido_id', 'tipo', 'descripcion', 'foto_url', 'direccion_corregida'}
        for clave, valor in datos.items():
            if clave not in campos_conocidos and valor is not None:
                incidencia.datos_extra[clave] = valor

        self._repo.guardar(incidencia)
        return incidencia

    def listar_incidencias(self):
        """Retorna todas las incidencias registradas (para demos)."""
        return self._repo.buscar_todas()
