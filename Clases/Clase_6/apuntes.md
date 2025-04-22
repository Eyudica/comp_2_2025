# Con O_NONBLOCK, es posible evitar que el proceso quede bloqueado si no hay otro extremo abierto todavía.

# en un FIFO los datos se consumen en la lectura. Esto significa que no pueden ser leídos nuevamente por otro proceso, aunque cada uno tenga su propio descriptor de archivo
# la diferencia entre le fifo y pipe es que el fifo se crea en el sistema y el pipe dentro del proceso.El pipe tiene persistencia en el disco, mientras que el fifo no.
# si un proceso abre el FIFO para leer y no hay nadie escribiendo, queda bloqueado (y viceversa).
# si hay 2 escritores, se intercalan , de forma atomica. No se solapan
# pero si los datos escritos son mas grandes que el pipe pueden intercalarse entre si 
# y no garantiza atomicidad
#Error | Causa | Solución
#FileNotFoundError | El FIFO no existe al intentar abrirlo | Usar os.path.exists() antes o crear con #os.mkfifo()
#Bloqueo indefinido al abrir | No hay proceso en el otro extremo | Lanzar los procesos en orden correcto (lector primero)
#No se reciben datos | El escritor no hace flush() o no cierra el FIFO | Usar flush() o cerrar el #archivo
#BrokenPipeError | El lector cerró y el escritor intentó seguir escribiendo | Controlar errores con #try/except