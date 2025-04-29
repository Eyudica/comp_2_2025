import signal,time

def handler(sig,frame):
    atexit()
def atexit():
    print("Programa terminado")
    exit()

signal.signal(signal.SIGTERM,handler)
while True:
    time.sleep(1)