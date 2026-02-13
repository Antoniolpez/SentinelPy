# Configuración de Red - Netplan

Este directorio contiene las configuraciones de Netplan para todas las VMs del entorno SentinelPy.

## Archivos de Configuración

- **server-netplan.yaml** - Servidor SentinelPy (10.100.100.10)
- **node1-netplan.yaml** - Nodo Desktop 1 (10.100.100.11)
- **node2-netplan.yaml** - Nodo Desktop 2 (10.100.100.12)

## Instrucciones de Aplicación

### 1. Identificar la interfaz de red

En cada VM, primero identifica el nombre de tu interfaz de red:

```bash
ip a
```

Busca la interfaz principal (normalmente `ens18`, `ens19`, `enp0s3`, etc.)

### 2. Editar el archivo si es necesario

Si tu interfaz NO es `ens18`, edita el archivo correspondiente y cambia:

```yaml
ethernets:
  ens18:  # <-- Cambia esto por tu interfaz
```

### 3. Verificar la puerta de enlace (gateway)

Verifica que `10.100.100.1` sea tu gateway correcto. Si no, cámbialo en:

```yaml
routes:
  - to: default
    via: 10.100.100.1  # <-- Cambia esto si es necesario
```

### 4. Aplicar la configuración

En cada VM, copia el archivo correspondiente y aplícalo:

```bash
# Backup de la configuración actual (recomendado)
sudo cp /etc/netplan/00-installer-config.yaml /etc/netplan/00-installer-config.yaml.backup

# Copiar el nuevo archivo
sudo cp server-netplan.yaml /etc/netplan/00-installer-config.yaml

# Probar la configuración (se revertirá automáticamente si hay error)
sudo netplan try

# Si todo funciona, aplicar permanentemente
sudo netplan apply
```

### 5. Verificar conectividad

```bash
# Verificar IP asignada
ip a

# Verificar conectividad local
ping 10.100.100.1

# Verificar conectividad internet
ping 8.8.8.8
```

## Tabla de IPs

| VM | Hostname | IP | Archivo |
|----|----------|-----|---------|
| Servidor | sentinelpy-server | 10.100.100.10/24 | server-netplan.yaml |
| Desktop 1 | sentinelpy-node1 | 10.100.100.11/24 | node1-netplan.yaml |
| Desktop 2 | sentinelpy-node2 | 10.100.100.12/24 | node2-netplan.yaml |

## Notas

- Todas las IPs están en la red **10.100.100.0/24**
- Gateway por defecto: **10.100.100.1**
- DNS: Google DNS (8.8.8.8, 8.8.4.4) - puedes cambiarlos por tu DNS local
- La configuración desactiva DHCP (`dhcp4: no`) para usar IPs estáticas
