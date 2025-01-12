import os
import datetime
import logging
from typing import Union

# Constantes
DEFAULT_DIR = "/c/Users/Fran/Proyectos"
BANCO_INICIAL = 50000

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Variables globales
v_operacion = 0
total_ingresos = 0
banco = BANCO_INICIAL

def get_user_input(prompt: str) -> Union[float, None]:
    try:
        return float(input(prompt).replace(',', '.'))
    except ValueError:
        logging.error("Entrada no válida")
        return None

def validate_positive_number(value: Union[float, None]) -> bool:
    if value is None or value <= 0:
        logging.error("El valor debe ser positivo")
        return False
    return True

def f_camb():
    global v_operacion, total_ingresos
    v_cliente = get_user_input('\n\tCuenta del Cliente: ')
    if not validate_positive_number(v_cliente):
        return

    v_dinero_cliente = get_user_input('\n\tDinero Recibido del Cliente: ')
    if not validate_positive_number(v_dinero_cliente):
        return

    if v_cliente > v_dinero_cliente:
        logging.error("El dinero recibido no puede ser menor que la cuenta del cliente")
        return

    v_result = v_dinero_cliente - v_cliente
    if v_result == 0:
        print('\n\tNo hay cambio')
    else:
        print(f'\n\tEl cambio es: {v_result:.2f}')

    v_operacion += 1
    total_ingresos += v_cliente

    with open("registro_diario.txt", 'a') as registro:
        registro.write(f"Operación {v_operacion}: Cliente pagó {v_cliente:.2f}, Cambio: {v_result:.2f}\n")

def f_caja():
    global banco, total_ingresos
    fecha_actual = datetime.datetime.now().strftime('%Y-%m-%d')
    archivo_informe = f"informe_{fecha_actual}.txt"

    with open(archivo_informe, 'w') as f:
        f.write(f"\n\tInforme diario de operaciones - {fecha_actual}\n")
        f.write("\n\t=========================================\n")
        f.write("\n\tResumen:\n")
        f.write(f"\n\t  Total de operaciones: {v_operacion}\n")
        f.write(f"\n\t  Total de ingresos: {total_ingresos:.2f}\n")
        
        saldo_actual = banco + total_ingresos
        f.write(f"\n\t  Saldo actual en banco: {saldo_actual:.2f}\n")
        
        f.write("\n\tDetalle de operaciones:\n")
        f.write("\n\t------------------------\n")
        
        if os.path.exists("registro_diario.txt"):
            with open("registro_diario.txt", 'r') as registro:
                f.write(registro.read())
        else:
            f.write("\n\tNo hay operaciones registradas para hoy.\n")
        
        f.write("\n\nFin del informe\n")

    logging.info(f"Informe diario generado: {archivo_informe}")

def f_list_informe():
    dir_act = os.getcwd() or DEFAULT_DIR

    if not os.path.isdir(dir_act):
        logging.error(f"El directorio {dir_act} no existe")
        return

    os.chdir(dir_act)
    informes = [f for f in os.listdir() if f.lower().startswith("informe_")]
    if not informes:
        logging.info(f"No se encontraron informes en el directorio {dir_act}")
        return

    # Ordenar los informes por fecha de creación
    informes.sort(key=lambda x: os.path.getctime(x), reverse=True)

    # Mostrar los informes numerados
    for i, informe in enumerate(informes, 1):
        print(f"{i}. {informe}")

    # Solicitar al usuario que seleccione un informe por número
    while True:
        try:
            seleccion = int(input('\n\tEscoge el número del informe a leer: '))
            if 1 <= seleccion <= len(informes):
                informe_elegido = informes[seleccion - 1]
                break
            else:
                print(f"Por favor, elige un número entre 1 y {len(informes)}")
        except ValueError:
            print("Por favor, introduce un número válido")

    if os.path.isfile(informe_elegido):
        with open(informe_elegido, 'r') as f:
            print(f.read())
    else:
        logging.error("El informe seleccionado no existe o no es válido.")

def menu():
    opciones = {
        'a': 'Introducir Operación',
        'b': 'Contar día actual',
        'c': 'Mostrar informes',
        'd': 'Salir'
    }
    for key, value in opciones.items():
        print(f'\n\t({key.upper()}) {value}')
    return input('\n\tIntroduce la opción: ').lower()

def eliminar_archivos():
    # Eliminar archivos de informe y registro si existen
    try:
        informe_actual = f"informe_{datetime.datetime.now().strftime('%Y-%m-%d')}.txt"
        
        if os.path.exists(informe_actual):
            os.remove(informe_actual)
            logging.info(f"Archivo eliminado: {informe_actual}")
        
        if os.path.exists("registro_diario.txt"):
            os.remove("registro_diario.txt")
            logging.info("Archivo eliminado: registro_diario.txt")
    
    except Exception as e:
        logging.error(f"Error al eliminar archivos: {e}")

def main():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        opcion = menu()

        if opcion == 'a':
            os.system('cls' if os.name == 'nt' else 'clear')
            f_camb()
        elif opcion == 'b':
            os.system('cls' if os.name == 'nt' else 'clear')
            f_caja()
        elif opcion == 'c':
            os.system('cls' if os.name == 'nt' else 'clear')
            f_list_informe()
        elif opcion == 'd':
            os.system('cls' if os.name == 'nt' else 'clear')
            eliminar_archivos()  # Llamar a la función para eliminar archivos antes de salir
            logging.info("Saliendo...")
            break
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            logging.warning(f"{opcion} no es válida")

        input('\n\tPulsa ENTER para continuar ...')

if __name__ == "__main__":
    main()
