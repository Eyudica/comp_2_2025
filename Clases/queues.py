#cola de mensaje: orientado a mensajes y no a bytes
#No es bloqueante por default (usa mecanismos internos para que el programa no quede colgado).

#Puede ser bidireccional, dependiendo de cómo se configure o use.

##Permite sincronización segura porque usa locks y semáforos internos.
#la sincronización que tienen los queue es con semáforos y locks, en vez de implícita por bloqueo como pasa con los pipes
#los locks permite proteger el acceso concurrente y los semaforos para saber cuandos elementos hay
#la data dse gurada En memoria compartida por el sistema operativo, no dentro del proceso Python.
#FIFO:  el orden importa, como una fila de espera bien organizada

#no hace falata ir cerrando los procesos y crear un header o dar el final del archivo con un caracter especial
# si hay n consumidor, hay que escribir el mensaje n veces



#el tema son las condiciones de carrera, se puede hacer un quilombo si dos procesos estan ejecutandose al mismo tiempo, por falta de sincronizacion
# tambien puede haber deadlocks (2 procesos esperan recursos de otro)
#tambien si el buffer se llena porque el consumidor no lee, el productor no puede escribir mas y se bloqua
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
