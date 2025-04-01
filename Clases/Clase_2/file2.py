#programa que genere 5 hijos pero que un padre solo tiene un hijo
import os
import time

def crear_hijo(child_number):
    child_number+=1
    pid = os.fork()
    if pid == 0:
        print(f"Hijo {child_number} pid: {os.getpid()} padre: {os.getppid()}")
        time.sleep(1)
        if child_number < 5:
            crear_hijo(child_number)
        os._exit(0)
# tambien se puede hacer anidando if y else
if __name__ == "__main__":
    crear_hijo(0)
    os.wait()
    print("Padre termino")