
import argparse
import datetime
import os
from database import DatabaseManager
from auditor import SystemAuditor
from reporter import ReportGenerator

def main():
    """
    Función principal para ejecutar la auditoría del sistema y generar informes.
    """
    parser = argparse.ArgumentParser(description="SentinelPy: Herramienta de Auditoría Automatizada de Red.")
    parser.add_argument("--inventory", default="inventario.json",
                        help="Ruta al archivo JSON de inventario de servidores (por defecto: inventario.json).")
    parser.add_argument("--db_name", default="sentinelpy.db",
                        help="Nombre de la base de datos SQLite (por defecto: sentinelpy.db).")
    parser.add_argument("--report_name", default="sentinelpy_report.pdf",
                        help="Nombre del archivo PDF del informe (por defecto: sentinelpy_report.pdf).")
    parser.add_argument("--ssh_key", default=os.path.expanduser("~/.ssh/id_rsa"),
                        help="Ruta a la clave privada SSH (por defecto: ~/.ssh/id_rsa).")

    args = parser.parse_args()

    # Inicializar gestores
    db_manager = DatabaseManager(args.db_name)
    auditor = SystemAuditor(args.ssh_key)
    reporter = ReportGenerator(args.report_name)

    # Conectar a la base de datos y crear tabla
    db_manager.connect()
    db_manager.create_table()

    # Realizar auditoría
    print("\nIniciando auditoría de sistemas...")
    audit_results = auditor.audit_system(args.inventory)

    # Procesar y guardar resultados
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for result in audit_results:
        db_manager.insert_audit_result(
            fecha=current_time,
            hostname=result["hostname"],
            ip=result["ip"],
            cpu_local=result["cpu_local"],
            disco_local=result["disco_local"],
            info_remota=result["info_remota"]
        )

    print("\nGenerando informe PDF...")
    # Obtener todos los resultados para el informe
    all_audits = db_manager.get_all_audits()

    # Generar gráficas de historial para cada host
    graphs = {}
    unique_hosts = set([audit[2] for audit in all_audits]) # audit[2] es el hostname
    for host in unique_hosts:
        history = db_manager.get_audit_history(host)
        graphs[host] = reporter.generate_graph(history, host)

    # Generar y guardar informe PDF
    html_content = reporter.generate_html_report(all_audits, graphs)
    reporter.generate_pdf_report(html_content)

    # Desconectar de la base de datos
    db_manager.disconnect()
    print("\nAuditoría completada y informe generado.")

if __name__ == "__main__":
    main()
