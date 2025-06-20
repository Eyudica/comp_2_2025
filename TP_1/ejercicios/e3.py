import os,time

def make_child():
    pid=os.fork()
    if pid==0:
        print("Hijo")
        print("Hijo huerfano ",pid)
        time.sleep(10)
    else:
       #os.wait()
       print("Padre",pid)

make_child()