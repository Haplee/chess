#!/bin/bash

# Inicializar el dinero en caja (en céntimos)
caja=2000000  # 20000€ en céntimos

# Función para convertir céntimos a formato de euros
format_euros() {
    printf "%.2f€" "$(echo "scale=2; $1/100" | bc)"
}

# Bucle principal del programa
while true; do
    # Mostrar el menú principal
    echo "Dinero en caja: $(format_euros $caja)"
    echo "1. Realizar venta" 
    echo "2. Terminar día"
    read -p "Opción: " opcion

    case $opcion in
        1)  # Opción para realizar una venta
            # Solicitar datos de la venta
            read -p "Cuenta total (€): " cuenta_total
            read -p "Dinero recibido (€): " dinero_cliente

            # Convertir a céntimos y validar entradas
            cuenta_total_cent=$(echo "$cuenta_total * 100" | awk '{print int($1)}')
            dinero_cliente_cent=$(echo "$dinero_cliente * 100" | awk '{print int($1)}')

            if [[ ! $cuenta_total_cent =~ ^[0-9]+$ ]] || [[ ! $dinero_cliente_cent =~ ^[0-9]+$ ]] || (( cuenta_total_cent <= 0 )) || (( dinero_cliente_cent <= 0 )); then
                echo "Error: Entrada inválida"
                continue
            fi

            # Calcular el cambio
            cambio_cent=$((dinero_cliente_cent - cuenta_total_cent))

            # Verificar si el pago es suficiente y si hay cambio disponible
            if (( cambio_cent < 0 )); then
                echo "Error: Dinero insuficiente"
            elif (( cambio_cent > caja )); then
                echo "Error: No hay suficiente cambio"
            else
                # Actualizar la caja y mostrar el resumen de la transacción
                caja=$((caja - cambio_cent))
                echo "Total: $(format_euros $cuenta_total_cent) | Recibido: $(format_euros $dinero_cliente_cent) | Cambio: $(format_euros $cambio_cent) | Caja: $(format_euros $caja)"
                read -p "Presiona Enter para continuar..."
            fi
            ;;
        2)  # Opción para terminar el día
            echo "Día terminado. Caja final: $(format_euros $caja)"
            exit 0
            ;;
        *)  # Opción inválida
            echo "Opción inválida"
            ;;
    esac
done