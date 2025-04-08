#coodigo que use fork que lo que hable entre proceso padre y proceso hijo pero que busquen evidenciar los problemas que pueden ocurrir
import os
import time

archivo = "charla.txt"
#[+] El proceso hijo copia todos los recursos del padre(memoria,stack,coigo,variables y file descriptors!!!!)[+]
def create_child():
    pid = os.fork()
    # y tambien conviene trabajar con pipes por su velocidad u otros metodos
    if pid == 0:
        # Hijo
        time.sleep(1)  #este sleep es para que no se pisen
        if os.path.exists(archivo):
            with open(archivo, 'r+') as f:
               # mensaje = f.read()
                f.write(f"{os.getpid()}\n")
                f.read()
        else:
            print("Hijo dice: el archivo no existe ")
    else:
        # Padre
        with open(archivo, 'w') as f:
            f.write("Mensaje de padre\n") # no se escribe el mensaje completo
        
        print("Padre dice: listo")
        os.wait()
       
if __name__ == "__main__":
    create_child()
    create_child() 
   # os.remove(archivo)

##################################################################
## no conviene, se rompe todo y da errores.No es deterministico ##
##################################################################