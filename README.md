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

## 🚀 Instalación Rápida

### En el Servidor (Ubuntu Server)

```bash
# Clonar repositorio
git clone https://github.com/Antoniolpez/SentinelPy.git
cd SentinelPy

# Ejecutar script de instalación (instala todo automáticamente)
bash scripts/install_server.sh
```

### En los Nodos (Ubuntu Desktop)

```bash
# Clonar repositorio
git clone https://github.com/Antoniolpez/SentinelPy.git
cd SentinelPy

# Ejecutar script de instalación para nodos
bash scripts/install_node.sh
```

### Instalación Manual

Si prefieres instalar manualmente:

```bash
# Dependencias del sistema (Ubuntu/Debian)
sudo apt update
sudo apt install -y \
    python3 \
    python3-pip \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    shared-mime-info

# Dependencias Python
pip3 install -r requirements.txt
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

## 🔧 Troubleshooting

### Error: libpango no encontrado

Si ves errores como `cannot load library 'libpango-1.0-0'`:

```bash
# Instalar dependencias del sistema para WeasyPrint
sudo apt install -y libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0
```

O simplemente ejecuta el script de instalación:
```bash
bash scripts/install_server.sh
```

### Error de permisos SSH

Si no puedes conectar por SSH:
```bash
# Verificar permisos de claves
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_rsa
chmod 644 ~/.ssh/id_rsa.pub

# En el nodo, verificar authorized_keys
sudo chmod 600 /home/monitor/.ssh/authorized_keys
```

## 📄 Licencia

MIT License
