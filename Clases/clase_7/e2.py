import signal,time,os,random

def handler(sig,frame):
    print("Señal {} recibida del proceso {}".format(sig,os.getpid())) 
    exit()
def make_fork(number,sig):
    pid=os.fork()
    if pid==0:
        signal.signal(sig,handler)
        print(f"Proceso hijo {number} y lanzando señal {sig}")
        while True:
            time.sleep(1)
    
    else:
        print("Proceso padre",number)
        return pid


if __name__=="__main__":
    pid1= make_fork(1,signal.SIGUSR1)
    pid2=make_fork(2,signal.SIGUSR2)
    pid3=make_fork(3,signal.SIGTERM)
    time.sleep(1)
    os.kill(pid1, signal.SIGUSR1)
    os.kill(pid2, signal.SIGUSR2)
    os.kill(pid3, signal.SIGTERM)

    # Esperar que todos los hijos terminen
    for _ in range(3):
        os.wait()