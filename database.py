
import sqlite3

class DatabaseManager:
    """
    Gestiona la conexión y operaciones con la base de datos SQLite.
    """

    def __init__(self, db_name='sentinelpy.db'):
        """
        Inicializa el gestor de la base de datos.

        Args:
            db_name (str): Nombre del archivo de la base de datos SQLite.
        """
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def connect(self):
        """
        Establece la conexión con la base de datos.
        """
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            print(f"Conectado a la base de datos: {self.db_name}")
        except sqlite3.Error as e:
            print(f"Error al conectar a la base de datos: {e}")

    def disconnect(self):
        """
        Cierra la conexión con la base de datos.
        """
        if self.conn:
            self.conn.close()
            print("Conexión a la base de datos cerrada.")

    def create_table(self):
        """
        Crea la tabla 'audits' si no existe.
        """
        if not self.cursor:
            print("Error: No hay conexión a la base de datos.")
            return
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS audits (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fecha TEXT NOT NULL,
                    hostname TEXT NOT NULL,
                    ip TEXT NOT NULL,
                    cpu_local REAL,
                    disco_local REAL,
                    info_remota TEXT
                )
            """)
            self.conn.commit()
            print("Tabla 'audits' verificada/creada correctamente.")
        except sqlite3.Error as e:
            print(f"Error al crear la tabla: {e}")

    def insert_audit_result(self, fecha, hostname, ip, cpu_local, disco_local, info_remota):
        """
        Inserta un resultado de auditoría en la tabla 'audits'.

        Args:
            fecha (str): Fecha y hora de la auditoría.
            hostname (str): Nombre del host.
            ip (str): Dirección IP.
            cpu_local (float): Uso de CPU local.
            disco_local (float): Uso de disco local.
            info_remota (str): Información remota (uptime).
        """
        if not self.cursor:
            print("Error: No hay conexión a la base de datos.")
            return
        try:
            self.cursor.execute("""
                INSERT INTO audits (fecha, hostname, ip, cpu_local, disco_local, info_remota)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (fecha, hostname, ip, cpu_local, disco_local, info_remota))
            self.conn.commit()
            print(f"Resultado de auditoría insertado para {hostname}.")
        except sqlite3.Error as e:
            print(f"Error al insertar resultado de auditoría: {e}")

    def get_all_audits(self):
        """
        Obtiene todos los resultados de auditoría de la base de datos.

        Returns:
            list: Una lista de tuplas con todos los resultados de auditoría.
        """
        if not self.cursor:
            print("Error: No hay conexión a la base de datos.")
            return []
        try:
            self.cursor.execute("SELECT * FROM audits ORDER BY fecha DESC")
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error al obtener resultados de auditoría: {e}")
            return []

    def get_audit_history(self, hostname):
        """
        Obtiene el historial de auditorías para un hostname específico.

        Args:
            hostname (str): El nombre del host para el que se desea el historial.

        Returns:
            list: Una lista de tuplas con el historial de auditorías para el host.
        """
        if not self.cursor:
            print("Error: No hay conexión a la base de datos.")
            return []
        try:
            self.cursor.execute("SELECT fecha, cpu_local, disco_local, info_remota FROM audits WHERE hostname = ? ORDER BY fecha ASC", (hostname,))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error al obtener historial de auditoría para {hostname}: {e}")
            return []

