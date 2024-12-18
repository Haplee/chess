import os
import datetime
import subprocess

# Variables
# banco = 50000
v_operacion = 0
fecha = datetime.datetime.now().strftime('%d:%m:%Y')

# Debe cambiarse si el directorio de trabajo cambia
dir_act = os.getcwd()

# Funciones
def f_camb():
    v_cliente = input('\n\tCuenta del Cliente: ')
    v_dinero_cliente = input('\n\tDinero Recibido del Cliente: ')

    if not v_cliente or not v_dinero_cliente:
        print('\n\tERROR-1001: Entrada vacía')
        print('\n\tVuelva a introducir los datos')
        return

    try:
        v_cliente = float(v_cliente)
        v_dinero_cliente = float(v_dinero_cliente)
    except ValueError:
        print('\n\tERROR-1002: Entrada no válida')
        return

    if v_cliente > v_dinero_cliente:
        print('\n\tERROR-1002: Entrada no válida')
        return

    v_result = v_dinero_cliente - v_cliente
    if v_result == 0:
        print('\n\tNo hay cambio')
    else:
        print(f'\n\tEl cambio es: {v_result}')

def f_caja():
    fecha_actual = datetime.datetime.now().strftime('%Y-%m-%d')
    archivo_informe = f"informe_{fecha_actual}.txt"

    with open(archivo_informe, 'w') as f:
        f.write(f"\n\tInforme diario de operaciones - {fecha_actual}\n")
        f.write("\n\t=========================================\n")
        f.write("\n\tResumen:\n")
        f.write(f"\n\t  Total de operaciones: {v_operacion}\n")
        f.write(f"\n\t  Total de ingresos: {total_ingresos}\n")
        
        saldo_actual = banco + total_ingresos
        f.write(f"\n\t  Saldo actual en banco: {saldo_actual}\n")
        
        f.write("\n\tDetalle de operaciones:\n")
        f.write("\n\t------------------------\n")
        
        if os.path.exists("registro_diario.txt"):
            with open("registro_diario.txt", 'r') as registro:
                f.write(registro.read())
        else:
            f.write("\n\tNo hay operaciones registradas para hoy.\n")
        
        f.write("\n\nFin del informe\n")

    print(f"\n\tInforme diario generado: {archivo_informe}")

def f_list_informe():
    global dir_act
    if not dir_act:
        dir_act = "/c/Users/Fran/Proyectos"

    if os.path.isdir(dir_act):
        os.chdir(dir_act)
        informes = [f for f in os.listdir() if f.lower().startswith("informe_")]
        if not informes:
            print(f"\n\tNo se encontraron informes en el directorio {dir_act}")
            return

        for informe in informes:
            print(informe)

        informe_elegido = input('\n\tEscoge el informe a leer: ')
        if informe_elegido and os.path.isfile(informe_elegido):
            with open(informe_elegido, 'r') as f:
                print(f.read())
        else:
            print("\n\tEl informe seleccionado no existe o no es válido.")
    else:
        print(f"\n\tEl directorio {dir_act} no existe")

def menu():
    print('\n\t(A) Introducir Operación')
    print('\n\t(B) Contar día actual')
    print('\n\t(C) Mostrar informes')
    print('\n\t(D) Salir')
    return input('\n\tIntroduce la opción: ').lower()

# Programa Principal
while True:
    os.system('cls' if os.name == 'nt' else 'clear')
    opcion = menu()

    if opcion == 'a':
        os.system('cls' if os.name == 'nt' else 'clear')
        f_camb()
        v_operacion += 1
        input('\n\tPulsa ENTER para continuar ...')
    elif opcion == 'b':
        os.system('cls' if os.name == 'nt' else 'clear')
        f_caja()
        input('\n\tPulsa ENTER para continuar ...')
    elif opcion == 'c':
        os.system('cls' if os.name == 'nt' else 'clear')
        f_list_informe()
        input('\n\tPulsa ENTER para continuar ...')
    elif opcion == 'd':
        os.system('cls' if os.name == 'nt' else 'clear')
        open('registro_diario.txt', 'w').close()  # Limpiar registro diario
        print("Saliendo...")
        break
    else:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{opcion} no es válida")
