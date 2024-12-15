#!/bin/bash
#Prueba 2 

# Variables 
banco=50000
v_operacion=0

#Funciones

#Funcion para comprobar si los datos se pasan por parametros
#function comp_param(){
#    if [ -z "$v_1" ]; then
#        echo -e '\n\t' "ERROR-1001: Entrada vacia"
#        exit 1
#    fi
#}

function f_camb(){
    echo -en '\n\t' "Cuenta del Cliente: " 
    read v_cliente
    echo -en '\n\t' "Dinero Recibido del Cliente: " 
    read v_dinero_cliente


    if [ -z "$v_cliente" ] || [ -z "$v_dinero_cliente" ]; then
        echo -e '\n\t' "ERROR-1001: Entrada vacia"
        echo -e '\n\t' "Vuelva a introducir los datos"
        return  # Salir de la función si hay error
    elif (( v_cliente > v_dinero_cliente )); then
        echo -e '\n\t' "ERROR-1002: Entrada no valida"
        return  # Salir de la función si hay error
    fi

    v_result=$((v_dinero_cliente - v_cliente))
    if (( v_result == 0 )); then
        echo -e '\n\t' "No hay cambio"
    else 
        echo -e '\n\t' "El cambio es: $v_result"
    fi
}

function caja(){
    # Función vacía, añadir lógica según sea necesario
    echo "Función caja no implementada"
}

function menu(){
    echo -e '\n\t' "(A) Introducir Operacion"
    echo -e '\n\t' "(B) Contar dia actual"
    echo -e '\n\t' "(C) Salir"
    echo -en '\n\t' "Introduce la opcion: "
    read v_opc 
    v_opc=$(echo "$v_opc" | tr '[:upper:]' '[:lower:]' | cut -c1)
}

# Programa Principal
while true; do
clear
    menu
    case "$v_opc" in 
        a)
            clear
            f_camb
            ((v_operacion++))
            read -p "Pulsa ENTER para continuar"
            ;;
        b)
            clear
            caja
            read -p "Pulsa ENTER para continuar"
            ;;
        c)
            clear
            echo "Saliendo..."
            exit
            ;;
        *)
            clear
            echo "Opcion no valida: $v_opc"
            ;;
    esac
done
