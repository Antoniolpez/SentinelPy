
import matplotlib.pyplot as plt
from weasyprint import HTML
import datetime
import base64
from io import BytesIO

class ReportGenerator:
    """
    Genera informes de auditoría en formato PDF, incluyendo tablas y gráficas.
    """

    def __init__(self, report_filename="sentinelpy_report.pdf"):
        """
        Inicializa el generador de informes.

        Args:
            report_filename (str): Nombre del archivo PDF de salida.
        """
        self.report_filename = report_filename

    def generate_graph(self, history_data, hostname):
        """
        Genera una gráfica de uso de CPU y disco a lo largo del tiempo.

        Args:
            history_data (list): Datos históricos de auditoría para un host.
            hostname (str): Nombre del host para el título de la gráfica.

        Returns:
            str: La ruta a la imagen de la gráfica guardada.
        """
        if not history_data:
            return None

        dates = [row[0] for row in history_data]
        cpu_usage = [row[1] for row in history_data]
        disk_usage = [row[2] for row in history_data]

        plt.style.use('seaborn-v0_8-darkgrid')
        fig, ax1 = plt.subplots(figsize=(12, 6))

        color = 'tab:cyan'
        ax1.set_xlabel('Fecha y Hora')
        ax1.set_ylabel('Uso de CPU (%)', color=color)
        ax1.plot(dates, cpu_usage, color=color, marker='o', linestyle='-', label='CPU')
        ax1.tick_params(axis='y', labelcolor=color)
        ax1.tick_params(axis='x', rotation=45)

        ax2 = ax1.twinx()
        color = 'tab:green'
        ax2.set_ylabel('Uso de Disco (%)', color=color)
        ax2.plot(dates, disk_usage, color=color, marker='x', linestyle='--', label='Disco')
        ax2.tick_params(axis='y', labelcolor=color)

        plt.title(f'Historial de Métricas para {hostname}', fontsize=16)
        fig.tight_layout()

        # Guardar la gráfica en un buffer en memoria
        buf = BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        image_base64 = base64.b64encode(buf.read()).decode('utf-8')
        plt.close(fig)

        return f"data:image/png;base64,{image_base64}"

    def generate_html_report(self, audit_results, graphs):
        """
        Genera el contenido HTML del informe de auditoría.

        Args:
            audit_results (list): Lista de tuplas con los resultados de la auditoría.
            graphs (dict): Diccionario con los nombres de host como clave y las imágenes de las gráficas en base64 como valor.

        Returns:
            str: El contenido HTML del informe.
        """
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        html = f"""
        <html>
            <head>
                <style>
                    body {{ font-family: sans-serif; margin: 2em; }}
                    h1 {{ color: #333; }}
                    table {{ width: 100%; border-collapse: collapse; margin-bottom: 2em; }}
                    th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                    th {{ background-color: #f2f2f2; }}
                    .error {{ color: red; font-weight: bold; }}
                    .graph {{ text-align: center; margin-top: 2em; }}
                </style>
            </head>
            <body>
                <h1>Informe de Auditoría - SentinelPy</h1>
                <p>Generado el: {now}</p>
                <h2>Resultados de la Auditoría</h2>
                <table>
                    <tr>
                        <th>ID</th>
                        <th>Fecha</th>
                        <th>Hostname</th>
                        <th>IP</th>
                        <th>CPU Local (%)</th>
                        <th>Disco Local (%)</th>
                        <th>Info Remota</th>
                    </tr>
        """

        for row in audit_results:
            error_class = "class='error'" if "Fallo" in str(row[6]) or "Error" in str(row[6]) else ""
            html += f"""
            <tr>
                <td>{row[0]}</td>
                <td>{row[1]}</td>
                <td>{row[2]}</td>
                <td>{row[3]}</td>
                <td>{row[4]}</td>
                <td>{row[5]}</td>
                <td {error_class}>{row[6]}</td>
            </tr>
            """

        html += """
                </table>
                <h2>Gráficas de Historial</h2>
        """

        for hostname, graph_base64 in graphs.items():
            if graph_base64:
                html += f"""
                <div class='graph'>
                    <h3>{hostname}</h3>
                    <img src='{graph_base64}' alt='Gráfica de historial para {hostname}'>
                </div>
                """

        html += """
            </body>
        </html>
        """
        return html

    def generate_pdf_report(self, html_content):
        """
        Genera el informe en PDF a partir del contenido HTML.

        Args:
            html_content (str): El contenido HTML del informe.
        """
        try:
            html = HTML(string=html_content)
            html.write_pdf(self.report_filename)
            print(f"Informe PDF generado: {self.report_filename}")
        except Exception as e:
            print(f"Error al generar el informe PDF: {e}")

