#!/bin/bash
#Prueba 2 

# Variables 
#banco=50000
v_operacion=0
fecha=$(date '+%d:%m:%Y')

#Debe cambiarse si el directorio de trabajo cambia 
dir_act=$(echo $PWD)



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



function f_caja() {
    fecha_actual=$(date '+%Y-%m-%d')
    archivo_informe="informe_${fecha_actual}.txt"

    # Crear el archivo de informe
    {
        echo -e "\n\tInforme diario de operaciones - $fecha_actual"
        echo -e "\n\t========================================="
        echo -e "\n\tResumen:"
        echo -e "\n\t  Total de operaciones: ${v_operacion:-0}"
        echo -e "\n\t  Total de ingresos: ${total_ingresos:-0}"
        
        # Calcular saldo sin usar bc
        saldo_actual=$((${banco:-0} + ${total_ingresos:-0}))
        echo -e "\n\t  Saldo actual en banco: $saldo_actual"
        
        echo -e "\n\tDetalle de operaciones:"
        echo -e "\n\t------------------------"
        
        # Verificar si existe el archivo registro_diario.txt
        if [ -f "registro_diario.txt" ]; then
            cat registro_diario.txt
        else
            echo -e "\n\tNo hay operaciones registradas para hoy."
        fi
        
        echo -e "\n\nFin del informe"
    } > "$archivo_informe"

    echo -e "\n\tInforme diario generado: $archivo_informe"
    
    # Limpiar o crear el registro diario para el siguiente día
    > registro_diario.txt
}

function f_list_informe(){
    if [ -z "$dir_act" ]; then
        dir_act="/c/Users/Fran/Proyectos"
    fi

    if [ -d "$dir_act" ]; then
        cd "$dir_act"
        ls | grep -i "informe_*"
        echo -en '\n\t' "Escoge el informe a leer"
        read informe_elegido
        if [  ]; then
    else
        echo -en '\n\t' "El directorio $dir_act no existe"
    fi

}


function menu(){
    echo -e '\n\t' "(A) Introducir Operacion"
    echo -e '\n\t' "(B) Contar dia actual"
    echo -e '\n\t' "(C) Mostrar informes"
    echo -e '\n\t' "(D) Salir"
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
            echo -en '\n\t' "Pulsa ENTER para continuar ..."
            read 
            ;;
        b)
            clear
            f_caja
            echo -en '\n\t' "Pulsa ENTER para continuar ..."
            read
            ;;
        c)
            clear 
            f_list_informe
            echo -en '\n\t' "Pulsa ENTER para continuar ..."
            read
            ;;
        d)
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
