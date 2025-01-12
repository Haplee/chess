import tkinter as tk
from tkinter import ttk, messagebox
import os
import datetime
import logging
from pathlib import Path
from typing import Union

# Configuración inicial
BANCO_INICIAL = 50000
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class MoneyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestión de Monedas")
        self.geometry("400x500")
        self.configure(bg="#f0f0f0")
        
        # Inicialización de variables de control
        self.v_operacion = 0
        self.total_ingresos = 0
        self.banco = BANCO_INICIAL
        self.create_widgets()

    def create_widgets(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', font=('Arial', 10), padding=5)
        style.configure('TLabel', font=('Arial', 12), background="#f0f0f0")
        style.configure('TEntry', font=('Arial', 10))

        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text="Cuenta del Cliente:").grid(row=0, column=0, sticky="w", pady=5)
        self.entrada_cliente = ttk.Entry(main_frame)
        self.entrada_cliente.grid(row=0, column=1, sticky="ew", pady=5)

        ttk.Label(main_frame, text="Dinero Recibido:").grid(row=1, column=0, sticky="w", pady=5)
        self.entrada_dinero = ttk.Entry(main_frame)
        self.entrada_dinero.grid(row=1, column=1, sticky="ew", pady=5)

        ttk.Button(main_frame, text="Calcular Cambio", command=self.f_camb).grid(row=2, column=0, columnspan=2, sticky="ew", pady=10)
        ttk.Button(main_frame, text="Generar Informe", command=self.f_caja).grid(row=3, column=0, columnspan=2, sticky="ew", pady=10)
        ttk.Button(main_frame, text="Listar Informes", command=self.f_list_informe).grid(row=4, column=0, columnspan=2, sticky="ew", pady=10)

        self.resultado = tk.StringVar()
        ttk.Label(main_frame, textvariable=self.resultado, wraplength=350).grid(row=5, column=0, columnspan=2, sticky="ew", pady=10)

        main_frame.columnconfigure(1, weight=1)

    def get_user_input(self, value: str) -> Union[float, None]:
        try:
            return float(value.replace(',', '.'))
        except ValueError:
            logging.error("Entrada no válida")
            return None

    def validate_positive_number(self, value: Union[float, None]) -> bool:
        if value is None or value <= 0:
            logging.error("El valor debe ser positivo")
            return False
        return True

    def f_camb(self):
        v_cliente = self.get_user_input(self.entrada_cliente.get())
        v_dinero_cliente = self.get_user_input(self.entrada_dinero.get())

        if not self.validate_positive_number(v_cliente) or not self.validate_positive_number(v_dinero_cliente):
            self.resultado.set("Error: Los valores deben ser positivos")
            return

        if v_cliente > v_dinero_cliente:
            self.resultado.set("Error: El dinero recibido no puede ser menor que la cuenta del cliente")
            return

        v_result = v_dinero_cliente - v_cliente
        self.resultado.set(f"El cambio es: {v_result:.2f}" if v_result > 0 else "No hay cambio")

        self.v_operacion += 1
        self.total_ingresos += v_cliente
        with open(self.get_working_directory() / "registro_diario.txt", 'a') as registro:
            registro.write(f"Operación {self.v_operacion}: Cliente pagó {v_cliente:.2f}, Cambio: {v_result:.2f}\n")

    def f_caja(self):
        fecha_actual = datetime.datetime.now().strftime('%Y-%m-%d')
        archivo_informe = self.get_working_directory() / f"informe_{fecha_actual}.txt"
        
        with open(archivo_informe, 'w') as f:
            f.write(f"\n\tInforme diario de operaciones - {fecha_actual}\n")
            f.write("\n\t=========================================\n")
            f.write(f"\n\tResumen:\n\tTotal de operaciones: {self.v_operacion}\n\tTotal de ingresos: {self.total_ingresos:.2f}\n")
            f.write(f"\n\tSaldo actual en banco: {self.banco + self.total_ingresos:.2f}\n")
            f.write("\n\tDetalle de operaciones:\n\t------------------------\n")
            
            if (self.get_working_directory() / "registro_diario.txt").exists():
                with open(self.get_working_directory() / "registro_diario.txt", 'r') as registro:
                    f.write(registro.read())
            else:
                f.write("\n\tNo hay operaciones registradas para hoy.\n")
            
            f.write("\n\nFin del informe\n")
        
        logging.info(f"Informe diario generado: {archivo_informe}")
        self.resultado.set(f"Informe generado: {archivo_informe}")

    def f_list_informe(self):
        dir_act = self.get_working_directory()
        informes = list(dir_act.glob("informe_*.txt"))
        if not informes:
            self.resultado.set(f"No se encontraron informes en el directorio {dir_act}")
            return

        informes.sort(key=lambda x: x.stat().st_ctime, reverse=True)
        informe_text = "Informes disponibles:\n" + "\n".join(f"{i}. {informe.name}" for i, informe in enumerate(informes, 1))
        self.resultado.set(informe_text)

    @staticmethod
    def get_working_directory():
        return Path(__file__).parent

    def eliminar_archivos(self):
        try:
            informe_actual = self.get_working_directory() / f"informe_{datetime.datetime.now().strftime('%Y-%m-%d')}.txt"
            if informe_actual.exists():
                informe_actual.unlink()
                logging.info(f"Archivo eliminado: {informe_actual}")
            registro_diario = self.get_working_directory() / "registro_diario.txt"
            if registro_diario.exists():
                registro_diario.unlink()
                logging.info("Archivo eliminado: registro_diario.txt")
        except Exception as e:
            logging.error(f"Error al eliminar archivos: {e}")

    def on_closing(self):
        if messagebox.askokcancel("Salir", "¿Deseas salir de la aplicación?"):
            self.eliminar_archivos()
            self.destroy()

if __name__ == "__main__":
    app = MoneyApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
