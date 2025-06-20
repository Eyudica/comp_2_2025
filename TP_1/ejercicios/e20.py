import time,os,signal
def handler_1(sig,frame):
    print("Se ha recibido la señal")
    print("Se recibio una senal SIGUSR1")

def handler_2(sig,frame):
    print("Se ha recibido la señal")
    print("Se recibio una senal SIGUSR2")
signal.signal(signal.SIGUSR1,handler_1)
signal.signal(signal.SIGUSR2,handler_2)
print(os.getpid())
time.sleep(100)