#!/bin/bash
#
# Script de instalación de SentinelPy para Ubuntu Server
# Instala todas las dependencias necesarias del sistema y Python
#

set -e  # Salir si hay algún error

echo "=========================================="
echo "  SentinelPy - Instalación en Servidor"
echo "=========================================="
echo ""

# Verificar que estamos en Ubuntu/Debian
if ! command -v apt &> /dev/null; then
    echo "❌ Error: Este script solo funciona en sistemas Ubuntu/Debian"
    exit 1
fi

echo "📦 Actualizando repositorios..."
sudo apt update

echo ""
echo "📚 Instalando dependencias del sistema para WeasyPrint..."
sudo apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    shared-mime-info

echo ""
echo "🐍 Instalando dependencias Python..."
pip3 install --user -r requirements.txt

echo ""
echo "✅ Instalación completada!"
echo ""
echo "📋 Próximos pasos:"
echo "1. Edita 'inventario.json' con tus servidores"
echo "2. Configura claves SSH (ver scripts/ssh_setup.sh)"
echo "3. Ejecuta: python3 main.py"
echo ""
