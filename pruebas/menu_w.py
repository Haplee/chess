import tkinter as tk

ventana = tk.Tk()
ventana.title("Mi Aplicación")
ventana.geometry("400x300")

etiqueta = tk.Label(ventana, text="Hola, mundo!")
etiqueta.pack()

boton = tk.Button(ventana, text="Haz clic", command=lambda: print("Botón presionado"))
boton.pack()

ventana.mainloop()
