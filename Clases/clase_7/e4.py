import threading
import signal
import time
import os
# lo que hace el with lock entra en la seccion critica
paused = False
lock = threading.Lock()

def countdown():
    count = 30
    while count > 0:
        with lock:
            if paused:
                print("[HILO] Pausado.")
            else:
                print(f"[HILO] Cuenta regresiva: {count}")
                count -= 1

        time.sleep(1)

def handle_pause(sig, frame):
    global paused
    with lock:
        paused = True
    print(f"[SEÑAL] Señal SIGUSR1 recibida. Pausando cuenta.")

def handle_resume(sig, frame):
    global paused
    with lock:
        paused = False
    print(f"[SEÑAL] Señal SIGUSR2 recibida. Reanudando cuenta.")

if __name__ == "__main__":
    print(f"[INFO] PID del proceso: {os.getpid()} (usalo con kill -USR1 o -USR2)")

    # Instalar los signal handlers
    signal.signal(signal.SIGUSR1, handle_pause)
    signal.signal(signal.SIGUSR2, handle_resume)

    # Lanzar hilo contador
    t = threading.Thread(target=countdown)
    t.start()

    # Esperar a que el hilo termine
    t.join()
    print("[INFO] Cuenta finalizada.")
