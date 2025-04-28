import os
import time

fifo_path="test_fifo"
import os

fifo_path = "test_fifo"

# Verificamos si el FIFO ya existe, sino lo creamos
if not os.path.exists(fifo_path):
    os.mkfifo(fifo_path)

with open(fifo_path, 'w') as fifo:
    print("[escritor] Enviando datos...")
    while True:
        mensaje = input("Que queres escribir?\n> ")
        if mensaje == 'exit':
            break
        fifo.write(mensaje)
        fifo.flush()  

    print("[escritor] Listo.")
