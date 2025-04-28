import os

output_path = "output.txt"
fifo_path="test_fifo"
with open(fifo_path, 'r') as fifo, open(output_path,'w') as output_file:
    print("[lector] Esperando datos...")
    while True:
        data = fifo.readline()
        output_file.write(data)
        output_file.flush()
        if len(data) == 0:
            break 
        print(f"[lector] Recibido: {data.strip()}")
