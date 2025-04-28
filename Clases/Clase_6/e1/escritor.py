import os
import time

fifo_path = "canal_fifo"

with open(fifo_path, 'w') as fifo:
    print("[escritor] Enviando datos...")
    for i in range(5):
        mensaje = f"Mensaje {i}\n"
        fifo.write(mensaje)
        fifo.flush()  # importante para que se envíe al instante, para limpiar el buffer del proceso
        time.sleep(1)  # osea para que no se escriba cuando se cierre el archivo, sino en el momento

    print("[escritor] Listo.")
