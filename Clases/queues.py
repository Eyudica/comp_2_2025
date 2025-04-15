#cola de mensaje: orientado a mensajes y no a bytes
#No es bloqueante por default (usa mecanismos internos para que el programa no quede colgado).

#Puede ser bidireccional, dependiendo de cómo se configure o use.

##Permite sincronización segura porque usa locks y semáforos internos.
#los locks permite proteger el acceso concurrente y los semaforos para saber cuandos elementos hay
#la data dse gurada En memoria compartida por el sistema operativo, no dentro del proceso Python.
#FIFO:  el orden importa, como una fila de espera bien organizada

#no hace falata ir cerrando los procesos
from multiprocessing import Process, Queue
import time

def productor(q):
    for i in range(5):
        print(f"[Productor] Produciendo {i}")
        q.put(i)
        time.sleep(0.5)

def consumidor(q):
    for i in range(5):
        item = q.get()
        print(f"[Consumidor] Consumió {item}")
        time.sleep(1)

if __name__ == '__main__':
    q = Queue()

    p1 = Process(target=productor, args=(q,))
    p2 = Process(target=consumidor, args=(q,))

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    q.close()
    q.join_thread()
