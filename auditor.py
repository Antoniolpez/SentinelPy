
import platform
import psutil
import subprocess
import paramiko
import json

class SystemAuditor:
    """
    Realiza auditorías del sistema, tanto locales como remotas vía SSH.
    """

    def __init__(self, ssh_key_path="~/.ssh/id_rsa_sentinelpy"):
        """
        Inicializa el auditor del sistema.

        Args:
            ssh_key_path (str): Ruta a la clave privada SSH.
        """
        self.ssh_key_path = ssh_key_path

    def get_local_metrics(self):
        """
        Obtiene métricas de uso de CPU y disco del sistema local.

        Returns:
            tuple: (uso_cpu, uso_disco) o (None, None) si hay un error.
        """
        try:
            cpu_usage = psutil.cpu_percent(interval=1)
            disk_usage = psutil.disk_usage("/").percent
            return cpu_usage, disk_usage
        except Exception as e:
            print(f"Error al obtener métricas locales: {e}")
            return None, None

    def get_remote_uptime(self, hostname, ip, user):
        """
        Obtiene el uptime de un sistema remoto vía SSH.

        Args:
            hostname (str): Nombre del host remoto.
            ip (str): Dirección IP del host remoto.
            user (str): Usuario para la conexión SSH.

        Returns:
            str: El uptime del sistema remoto o un mensaje de error.
        """
        try:
            client = paramiko.SSHClient()
            client.load_system_host_keys()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            # Cargar la clave privada
            private_key = paramiko.RSAKey.from_private_key_file(self.ssh_key_path)

            client.connect(hostname=ip, username=user, pkey=private_key, timeout=10)

            stdin, stdout, stderr = client.exec_command("uptime")
            output = stdout.read().decode().strip()
            error = stderr.read().decode().strip()

            client.close()

            if error:
                return f"Error SSH en {hostname} ({ip}): {error}"
            return output
        except paramiko.AuthenticationException:
            return f"Fallo de autenticación SSH para {user}@{hostname} ({ip}). Verifique la clave SSH."
        except paramiko.SSHException as e:
            return f"Error SSH en {hostname} ({ip}): {e}"
        except Exception as e:
            return f"Error de conexión a {hostname} ({ip}): {e}"

    def audit_system(self, inventory_file="inventario.json"):
        """
        Realiza la auditoría completa de los sistemas definidos en el inventario.

        Args:
            inventory_file (str): Ruta al archivo JSON de inventario.

        Returns:
            list: Una lista de diccionarios con los resultados de la auditoría.
        """
        audit_results = []
        try:
            with open(inventory_file, "r") as f:
                inventory = json.load(f)
        except FileNotFoundError:
            print(f"Error: Archivo de inventario '{inventory_file}' no encontrado.")
            return []
        except json.JSONDecodeError:
            print(f"Error: El archivo '{inventory_file}' no es un JSON válido.")
            return []

        for server in inventory:
            hostname = server.get("hostname", "N/A")
            ip = server.get("ip", "N/A")
            user = server.get("user", "N/A")

            cpu_local, disco_local = self.get_local_metrics()
            info_remota = self.get_remote_uptime(hostname, ip, user)

            audit_results.append({
                "hostname": hostname,
                "ip": ip,
                "cpu_local": cpu_local,
                "disco_local": disco_local,
                "info_remota": info_remota
            })
        return audit_results

