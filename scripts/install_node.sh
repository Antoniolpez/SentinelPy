#!/bin/bash
#
# Script de instalación de SentinelPy para Ubuntu Desktop (Nodos monitorizados)
# Solo instala lo mínimo necesario para ser monitorizados
#

set -e

echo "=========================================="
echo "  SentinelPy - Instalación en Nodo"
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
echo "🔐 Instalando SSH Server..."
sudo apt install -y openssh-server

echo ""
echo "🔧 Habilitando SSH..."
sudo systemctl enable ssh
sudo systemctl start ssh

echo ""
echo "👤 Creando usuario 'monitor'..."
if id "monitor" &>/dev/null; then
    echo "ℹ️  El usuario 'monitor' ya existe"
else
    sudo useradd -m -s /bin/bash monitor
    echo "✅ Usuario 'monitor' creado"
fi

echo ""
echo "📂 Preparando directorio para claves SSH..."
sudo mkdir -p /home/monitor/.ssh
sudo touch /home/monitor/.ssh/authorized_keys
sudo chmod 700 /home/monitor/.ssh
sudo chmod 600 /home/monitor/.ssh/authorized_keys
sudo chown -R monitor:monitor /home/monitor/.ssh

echo ""
echo "✅ Nodo configurado!"
echo ""
echo "📋 Próximos pasos:"
echo "1. Añade la clave pública del servidor a /home/monitor/.ssh/authorized_keys"
echo "2. Verifica conectividad SSH desde el servidor"
echo ""
