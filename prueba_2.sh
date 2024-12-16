#!/bin/bash
#Prueba 2 

# Variables 
#banco=50000
v_operacion=0
fecha=$(date '+%d:%m:%Y')


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



function f_caja(){
    #Falta funcion que guarda todas las operaciones en el dia a dia y genera un documeto donde se guarda
    fecha_actual=$(date '+%Y-%m-%d')
    archivo_informe="informe_${fecha_actual}.txt"

    echo -e '\n\t' "Informe diario de operaciones - $fecha_actual" > "$archivo_informe"
    echo -e '\n\t' "=========================================" >> "$archivo_informe"
    echo -e '\n\t' "" >> "$archivo_informe"
    echo -e '\n\t' "Resumen:" >> "$archivo_informe"
    echo -e '\n\t' "  Total de operaciones: $v_operacion" >> "$archivo_informe"
    echo -e '\n\t' "  Total de ingresos: $total_ingresos" >> "$archivo_informe"
    echo -e '\n\t' "  Saldo actual en banco: $(echo "$banco + $total_ingresos" | bc)" >> "$archivo_informe"
    echo -e '\n\t' "" >> "$archivo_informe"
    echo -e '\n\t' "Detalle de operaciones:" >> "$archivo_informe"
    echo -e '\n\t' "------------------------" >> "$archivo_informe"
    cat registro_diario.txt >> "$archivo_informe"
    echo "" >> "$archivo_informe"
    echo "Fin del informe" >> "$archivo_informe"

    echo -e '\n\t' "Informe diario generado: $archivo_informe"
    
    # Limpiar el registro diario para el siguiente día
    > registro_diario.txt


}

function menu(){
    echo -e '\n\t' "(A) Introducir Operacion"
    echo -e '\n\t' "(B) Contar dia actual"
    echo -e '\n\t' "(C) Salir"
    echo -en '\n\t' "Introduce la opcion: "
    read v_opc 
    v_opc=$(echo "$v_opc" | tr '[:upper:]' '[:lower:]')
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
            f_caja
            read -p "Pulsa ENTER para continuar"
            ;;
        c)
            clear
            echo "Saliendo..."
            exit
            ;;
        *)
            clear
            echo "$v_opc No es valida"
            ;;
    esac
done
