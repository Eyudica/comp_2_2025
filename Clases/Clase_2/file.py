#dos hijos que hagan un sleep y que printeen su pid y cuando el padre termine diga soy el padre estoy terminando sin wait

import os
import time

def create_hijo(tiempo):
    pid = os.fork()
    if pid == 0:
        time.sleep(tiempo)
        print(f"Soy el hijo --> {os.getpid()} y mi padre {os.getppid()}")
        os._exit(0)


if __name__ == "__main__":
    create_hijo(2)
    create_hijo(3)
    # time.sleep(1)
   # os.wait() # lo mismo(hay que hacerlo tantas veces como hijo)
   # os.wait() # ahi espera  los 2
    os.waitpid(-1)
    print(f"Soy el padre --> {os.getpid()}") # padre termina antes que el hijo, haciendolo huerfano
    # el abuelo se hace cargo del nieto(systemd)