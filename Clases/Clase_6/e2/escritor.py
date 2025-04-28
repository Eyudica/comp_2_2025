import os
import time
if os.path.exists("/tmp/test_fifo"):
    os.remove("/tmp/test_fifo")
fifo_path = "/tmp/test_fifo"

with open(fifo_path, 'w') as fifo:
    print("[escritor] Enviando datos...")
    for i in range(100):
        mensaje = f"Mensaje {i}-->{time.time()}\n"
        fifo.write(mensaje)
        fifo.flush()  # importante para que se envíe al instante, para limpiar el buffer del proceso
        time.sleep(0.1)  # osea para que no se escriba cuando se cierre el archivo, sino en el momento

    print("[escritor] Listo.")
