import os
import time


def main():
    fifo_pathw="/tmp/chat_a"
    fifo_pathr="/tmp/chat_b"

    if not os.path.exists(fifo_pathw):
        os.mkfifo(fifo_pathw)

    with open(fifo_pathw, 'w') as fifo_write:
        mensaje = input("Que queres escribir?\n> ")
        fifo_write.write(mensaje)
        fifo_write.flush() 
    with open(fifo_pathr,'r') as fifo_read:
        
        data_read=fifo_read.readline()
        if data_read:
            print(f"Mensaje {str(data_read)}") 
        else:
            time.sleep(1)
        
        
main()