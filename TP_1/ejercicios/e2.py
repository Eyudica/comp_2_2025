import time,os

def make_child():
    pid=os.fork()
    if pid==0:
        print("Hijo")
        print("Hijo zombie ",pid)
    else:
        time.sleep(10)
        os.wait()
        print("Proceso hijo terminado")

make_child()
