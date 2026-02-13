#!/bin/bash
#
# Script de configuración de claves SSH para SentinelPy
# Ejecutar en el SERVIDOR para configurar acceso a los nodos
#

set -e

echo "=========================================="
echo "  SentinelPy - Configuración SSH"
echo "=========================================="
echo ""

SSH_KEY_PATH="$HOME/.ssh/id_rsa_sentinelpy"

# Generar clave SSH si no existe
if [ -f "$SSH_KEY_PATH" ]; then
    echo "ℹ️  La clave SSH ya existe en: $SSH_KEY_PATH"
else
    echo "🔑 Generando clave SSH..."
    ssh-keygen -t rsa -b 4096 -f "$SSH_KEY_PATH" -N "" -C "sentinelpy@$(hostname)"
    echo "✅ Clave SSH generada"
fi

echo ""
echo "📋 Clave pública generada:"
echo "---"
cat "${SSH_KEY_PATH}.pub"
echo "---"
echo ""

# Leer IPs de los nodos desde inventario.json
echo "📡 Nodos detectados en inventario.json:"
if [ -f "inventario.json" ]; then
    # Extraer IPs del inventario (simple parsing)
    grep '"ip"' inventario.json | sed 's/.*"ip": "\([^"]*\)".*/\1/' | while read -r NODE_IP; do
        USER=$(grep -B2 "\"ip\": \"$NODE_IP\"" inventario.json | grep '"user"' | sed 's/.*"user": "\([^"]*\)".*/\1/')
        echo "  - $USER@$NODE_IP"
    done
else
    echo "⚠️  No se encontró inventario.json"
fi

echo ""
echo "📋 Para completar la configuración SSH:"
echo ""
echo "1. Copia la clave pública a cada nodo:"
echo "   ssh-copy-id -i ${SSH_KEY_PATH}.pub monitor@10.100.100.11"
echo "   ssh-copy-id -i ${SSH_KEY_PATH}.pub monitor@10.100.100.12"
echo ""
echo "2. Verifica la conexión:"
echo "   ssh -i $SSH_KEY_PATH monitor@10.100.100.11"
echo ""
echo "3. Actualiza auditor.py para usar esta clave:"
echo "   auditor = SystemAuditor(ssh_key_path=\"$SSH_KEY_PATH\")"
echo ""
