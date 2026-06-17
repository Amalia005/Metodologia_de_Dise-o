import sqlite3
import os
from models.pedido import Pedido, ESTADOS

# ==========================================
# REPOSITORIO DE PEDIDOS — Persistencia SQLite
# Decisión arquitectónica: SQLite para consistencia
# fuerte vía transacciones, evitando estados
# contradictorios del pedido.
# Mantiene la misma interfaz (guardar, buscar_por_id)
# del repositorio original en memoria.
# ==========================================

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'pedidos.db')


class PedidoRepository:

    def __init__(self):
        self._init_db()

    def _get_connection(self):
        """Crea una conexión nueva a SQLite (thread-safe)."""
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        """Crea la tabla de pedidos si no existe."""
        conn = self._get_connection()
        conn.execute('''
            CREATE TABLE IF NOT EXISTS pedidos (
                id TEXT PRIMARY KEY,
                origen TEXT,
                destinatario TEXT,
                canal TEXT,
                estado TEXT NOT NULL DEFAULT 'Creado',
                repartidor_id TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def guardar(self, pedido):
        """Guarda o actualiza un pedido en SQLite (upsert)."""
        conn = self._get_connection()
        conn.execute('''
            INSERT OR REPLACE INTO pedidos (id, origen, destinatario, canal, estado, repartidor_id)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (pedido.id, pedido.origen, pedido.destinatario, pedido.canal,
              pedido.estado, pedido.repartidor_id))
        conn.commit()
        conn.close()
        return pedido

    def buscar_por_id(self, pedido_id):
        """Busca un pedido por su ID. Retorna None si no existe."""
        conn = self._get_connection()
        row = conn.execute('SELECT * FROM pedidos WHERE id = ?', (pedido_id,)).fetchone()
        conn.close()
        if row is None:
            return None
        return self._row_to_pedido(row)

    def _row_to_pedido(self, row):
        """Reconstruye un objeto Pedido a partir de una fila de SQLite,
        restaurando el estado correcto vía el patrón State."""
        pedido = Pedido.__new__(Pedido)
        pedido.id = row['id']
        pedido.origen = row['origen']
        pedido.destinatario = row['destinatario']
        pedido.canal = row['canal']
        pedido.repartidor_id = row['repartidor_id']
        estado_nombre = row['estado']
        pedido._estado = ESTADOS[estado_nombre]()
        return pedido
