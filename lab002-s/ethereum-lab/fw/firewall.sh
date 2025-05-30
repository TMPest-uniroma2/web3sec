#!/usr/bin/env bash

# Network and ports configuration
mapfile -t DOCKER_SUBNETS < <(sudo docker network ls | awk '{print $1}' | grep -v NETWORK | xargs -I{}  sudo docker network inspect {} | grep -i subnet | grep -oP "[\d\.\/]+")
NGINX_PORT=443
SERVICES_PORTS=(3000 8545)  # React, Ganache

# Helper function to add rules
apply_rules() {
    echo "Applying iptables rules to DOCKER-USER chain..."

    # Flush existing rules in DOCKER-USER chain
    sudo iptables -F DOCKER-USER

    # Allow NGINX port
    sudo iptables -A DOCKER-USER -p tcp --dport "$NGINX_PORT" -j ACCEPT
    echo "Allowed external access to NGINX on port $NGINX_PORT"

    # Drop access to all service ports
    for port in "${SERVICES_PORTS[@]}"; do
        sudo iptables -A DOCKER-USER -p tcp --dport "$port" -j DROP
        echo "Blocked external access to service port $port"
    done

    # Allow Docker subnet access for inter-container communication
    for DOCKER_SUBNET in "${DOCKER_SUBNETS[@]}"; do
      sudo iptables -A DOCKER-USER -s "$DOCKER_SUBNET" -j ACCEPT
      echo "Allowed internal Docker network access for subnet $DOCKER_SUBNET"
    done

    # Set default DROP rule for DOCKER-USER chain
    sudo iptables -A DOCKER-USER -j RETURN
    echo "Default policy set to RETURN for DOCKER-USER chain"
}


# Helper function to remove rules
remove_rules() {
    echo "Removing iptables rules..."

    sudo iptables -F DOCKER-USER
    echo "Reset default DOCKER-USER policy to ACCEPT"
}

# Main script logic
if [ "$1" == "on" ]; then
    apply_rules
elif [ "$1" == "off" ]; then
    remove_rules
else
    echo "Usage: $0 {on|off}"
    echo "  on  - Apply iptables rules to restrict access to Docker services"
    echo "  off - Remove iptables rules and allow all access"
    exit 1
fi
