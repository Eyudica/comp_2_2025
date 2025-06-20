import signal,time,os
def handler(sig,frame):
    print("Se ha recibido la señal")


signal.signal(signal.SIGUSR1,handler)
print(os.getpid())
time.sleep(100)