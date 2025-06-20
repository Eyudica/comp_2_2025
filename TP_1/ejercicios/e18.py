import os,time

r,w=os.pipe()
print(os.getpid())
os.write(w,b"hola")
time.sleep(100)
