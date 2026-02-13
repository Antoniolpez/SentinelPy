# SentinelPy

Herramienta de auditoría automatizada de red para monitorización de sistemas Linux.

## 🎯 Características

- ✅ Auditoría de métricas locales (CPU, disco)
- ✅ Monitorización remota vía SSH (uptime)
- ✅ Almacenamiento en base de datos SQLite
- ✅ Generación de informes PDF con gráficos históricos
- ✅ Soporte para múltiples servidores

## 📋 Requisitos

- Python 3.8+
- Ubuntu Server/Desktop para las VMs
- Acceso SSH entre máquinas

## 🚀 Instalación

```bash
# Instalar dependencias
pip install psutil paramiko matplotlib weasyprint

# Clonar repositorio
git clone https://github.com/Antoniolpez/SentinelPy.git
cd SentinelPy
```

## 🔧 Configuración

1. Edita `inventario.json` con tus servidores:
```json
[
    {
        "hostname": "servidor1",
        "ip": "10.100.100.11",
        "user": "monitor"
    }
]
```

2. Configura claves SSH para acceso sin contraseña

3. Ejecuta la auditoría:
```bash
python3 main.py
```

## 📁 Estructura del Proyecto

```
SentinelPy/
├── main.py              # Punto de entrada principal
├── auditor.py           # Auditoría de sistemas
├── database.py          # Gestión de base de datos
├── reporter.py          # Generación de informes
├── inventario.json      # Configuración de servidores
├── netplan/             # Configuraciones de red
└── scripts/             # Scripts de automatización
```

## 🏗️ Entorno Proxmox

Este proyecto incluye configuraciones para desplegar en Proxmox:
- 1 Ubuntu Server (SentinelPy Master)
- 2 Ubuntu Desktop (Nodos monitorizados)
- Red 10.100.100.0/24

Ver `netplan/README.md` para configuración de red.

## 📊 Uso

```bash
# Ejecución básica
python3 main.py

# Con parámetros personalizados
python3 main.py --inventory mi_inventario.json --report_name informe.pdf
```

## 📄 Licencia

MIT License
