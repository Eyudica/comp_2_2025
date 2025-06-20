import time,sys,os,signal

def main():
    print("ejecutando")
    print(os.getpid())
    time.sleep(100)

def handler(sig,frame):
    print("Se ha recibido la señal")
    sys.exit()
signal.signal(signal.SIGTERM,handler)
main()

