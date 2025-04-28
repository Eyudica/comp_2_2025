import os
import time

fifo_path = "canal_fifo"

with open(fifo_path, 'w') as fifo:
    print("[escritor] Enviando datos...")
    while True:
        mensaje = f"Productor 1\n"
        fifo.write(mensaje)
        fifo.flush()  # importante para que se envíe al instante, para limpiar el buffer del proceso
        time.sleep(1)
print("[escritor] Listo.")
