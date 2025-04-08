#saben que proceso esta pidiendo datos, esta bloqueado hasta que le llegue la informacion. Es mucho mas eficiente porque esta en kernel
# Es lo mismo pero mejor implementado.Son unidireccionales
#conectar la salida de un proceso directamente a la entrada de otro, sin necesidad de archivos intermedio. Es como en bash |
#l puntero de escritura indica dónde se deben escribir los nuevos datos, mientras que el puntero de lectura indica de dónde se deben leer los datos
#La creación de un pipe con os.pipe(), que devuelve dos descriptores de archivo: uno para lectura y otro para escritura.
#PRIMERo se crea el pipe y despues el fork , para que los 2 procesos sepan  hacia donde apuntar
#la idea seria siempre cerrar el pipe al terminar el proceso 
#el kernel monitoriza el buffere los procesos se bloquean mientras realizan la operacion y se libera cuando termina el otro proceso
# se cierran para evitar fugas y un deadlock
# en /proc/$PID/fd estan los descriptores de archivo no son archivos son un buffer de memoria, no estan en el disco pero lo maneja coomo si fuese un archivo 
# en los pipes uno tiene el permiso de lectura y otro  de escritura
import os
import sys

def main():
    read,write = os.pipe()
    pid = os.fork()
    if pid == 0:
        os.close(write)
        data=os.read(read,10)
        print(f"Hijo lee: {data}")
    else:
        os.close(read)
        os.write(write,b"Pipe")
        os.close(write)
if __name__ == "__main__":
    main()