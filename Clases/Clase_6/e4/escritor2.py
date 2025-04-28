import os
import time

fifo_path = "canal_fifo"

with open(fifo_path, 'w') as fifo:
    print("[escritor] Enviando datos...")
    while True:
        mensaje = f"Productor 2\n"
        fifo.write(mensaje)
        fifo.flush()  # importante para que se envíe al instante, para limpiar el buffer del proceso
        time.sleep(5)
    print("[escritor] Listo.")
