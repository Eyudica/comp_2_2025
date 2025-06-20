import os

pid = os.fork()
if pid == 0:
    os.execlp("ls", "ls", "-l")  # reemplaza al proceso hijo con 'ls'
else:
    os.wait()