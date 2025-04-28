import os

fifo_path = "/tmp/test_fifo"

with open(fifo_path, 'r') as fifo:
    print("[lector] Esperando datos...")
    while True:
        data = fifo.readline()
        if len(data) == 0:
            break  # EOF
        print(f"[lector] Recibido: {data.strip()}")
