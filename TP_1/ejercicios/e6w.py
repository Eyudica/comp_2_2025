import os,time

fd=os.open("e6.txt",os.O_WRONLY)
data=os.write(fd,b"hola")
os.close(fd)
