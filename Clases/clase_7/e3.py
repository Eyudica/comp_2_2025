import time,os,signal
signal.signal(signal.SIGINT,signal.SIG_IGN)
time.sleep(5)
signal.signal(signal.SIGINT,signal.SIG_DFL)

while True:
    print("Ahora si funciona el ctrl+c")
    time.sleep(5)