import os,time

fd=os.open("e6.txt",os.O_RDONLY)
data=os.read(fd,10)
print(data)
os.close(fd)