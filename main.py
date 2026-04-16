from operaciones.repartidor import Repartidor
from operaciones.asignador import AsignadorService, AsignarPorMenorCarga
from soporte.facade import LogisticaFacade

# ==========================================
# SIMULACIÓN — 4 Casos de Uso
# ==========================================

if __name__ == "__main__":

    # --- Configuración inicial ---
    # SUPUESTO: los repartidores son enteros simples
    # con capacidad máxima de 2 pedidos cada uno
    estrategia = AsignarPorMenorCarga()
    asignador = AsignadorService(estrategia)
    asignador.agregar_repartidor(Repartidor("REP-01", capacidad_maxima=2))
    asignador.agregar_repartidor(Repartidor("REP-02", capacidad_maxima=2))

    sistema = LogisticaFacade(asignador)

    print("========= CASO DE USO 1: Crear Pedidos =========")
    sistema.crear_pedido(
        id_pedido="PED-001",
        canal="ecommerce",
        origen="Bodega Central",
        punto_origen="BOD-01",
        destino="Av. Libertad 123",
        destinatario="Benjamin Maldonado",
        contacto="+56912345678",
        tipo_carga="Electrónicos",
        peso=5.5
    )
    sistema.crear_pedido(
        id_pedido="PED-002",
        canal="tienda-fisica",
        origen="Sucursal Valparaíso",
        punto_origen="SUC-VP",
        destino="Calle Condell 456",
        destinatario="Catalina López",
        contacto="+56987654321",
        tipo_carga="Ropa",
        peso=2.0
    )

    print("\n========= CASO DE USO 2: Validar Pedidos =========")
    sistema.validar_pedido("PED-001")
    sistema.validar_pedido("PED-002")

    print("\n========= CASO DE USO 3: Asignar Repartidores =========")
    sistema.asignar_repartidor("PED-001")
    sistema.asignar_repartidor("PED-002")

    print("\n========= CASO DE USO 4: Gestionar Incidencias =========")
    sistema.registrar_incidencia("PED-001", "Cliente no se encontraba en el domicilio.")
    sistema.gestionar_incidencia("INC-001", "Se reprogramó la entrega para el día siguiente.")

    print("\n========= ESTADO FINAL DEL SISTEMA =========")
    sistema.mostrar_estado()