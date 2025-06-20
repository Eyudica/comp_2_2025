
import datetime
import random
import multiprocessing
import json
import math
import time
import os
import collections
from hashlib import sha256
import sys
import signal
PAQUETES = 60

def generar_muestra():
    return {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "frecuencia": random.randint(60,180),
        "presion": random.randint(110,180),# random.randint(70,110)],
        "oxigeno": random.randint(90,100)
    }

def make_math(conn,clave,queue):
    signal.signal(signal.SIGINT, signal.SIG_IGN)

    ventana=collections.deque(maxlen=30)

    for _ in range(PAQUETES):
        try:
            
            data = conn.recv() 
            valor=data.get(clave)
            if isinstance(valor,list):
                valor=round(sum(valor)/len(valor),2)
            ventana.append(valor)
                

            media=round(sum(ventana)/len(ventana),2)
            desviacion=round(math.sqrt(sum((v-media)**2 for v in ventana) /len(ventana)),2) 

            resultado= {
                        "tipo":clave,
                        "timestamp": data.get("timestamp"),
                        "media": media,
                        "desviacion": desviacion
                    }
            queue.put(resultado)
        except EOFError:
            break    

       # if clave=="presion":

        

def make_muestra(conns):
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    print("Generando muestras.Espera 60")
    for _ in range(PAQUETES):
        muestra=generar_muestra()
        for conn in conns:
            conn.send(muestra)
        time.sleep(1)

def validar(queue_entrada,queue_salida):
    signal.signal(signal.SIGINT, signal.SIG_IGN)

    bloques = []
    bloques_por_timestamp = {}
    prev_hash = "00000000000000000000000000000000000000000000000000000000000000000"
    bloques_procesados = 0

    while bloques_procesados < PAQUETES:
        resultado = queue_entrada.get()
        ts = resultado["timestamp"]

        if ts not in bloques_por_timestamp:
            bloques_por_timestamp[ts] = {}
        bloques_por_timestamp[ts][resultado["tipo"]] = resultado

        if len(bloques_por_timestamp[ts]) == 3:
            datos = bloques_por_timestamp[ts]

            alerta = (
                datos["frecuencia"]["media"] > 200 or
                (90>=datos["oxigeno"]["media"] >=100 )or
                datos["presion"]["media"] > 200
            )

            datos_str = json.dumps({
                "frecuencia": datos["frecuencia"],
                "presion": datos["presion"],
                "oxigeno": datos["oxigeno"]
            }, sort_keys=True)

            bloque_raw = prev_hash + datos_str + ts
            current_hash = sha256(bloque_raw.encode("utf-8")).hexdigest()

            bloque = {
                "timestamp": ts,
                "datos": datos,
                "alerta": alerta,
                "prev_hash": prev_hash,
                "hash": current_hash
            }

            prev_hash = current_hash
            bloques_procesados += 1
            bloques.append(bloque)
    queue_salida.put(bloques)
    #print(f"Bloques procesados: {bloques}")
            #guardar_bloque(bloque)

            #print(f"Bloque {bloques_procesados} guardado. Alerta: {alerta}")
def guardar_bloque(bloque, archivo="blockchain.json"):
    if os.path.exists(archivo):
        with open(archivo, "r") as f:
            cadena = json.load(f)
    else:
        cadena = []

    cadena.append(bloque)

    with open(archivo, "w") as f:
        json.dump(cadena, f, indent=4)


def iniciar_procesos(tipo,queue):
    parent_conn, child_conn = multiprocessing.Pipe()
    send = multiprocessing.Process(target=make_muestra, args=(parent_conn,))
    send.start()
    send.join()
    receptor = multiprocessing.Process(target=make_math, args=(child_conn,tipo,queue))
    receptor.start()
    receptor.join()

def handler(sig,frame):
    print("\nEl usuario presiono la tecla CTRL+C")
    os._exit(1)

def main():
    if multiprocessing.current_process().name=="MainProcess":
        signal.signal(signal.SIGINT, handler)

    pipes=[]
    for _ in range(3):
        pipes.append(multiprocessing.Pipe())
    queue=multiprocessing.Queue()
    queue_resultados_validados=multiprocessing.Queue()
    generador_p=multiprocessing.Process(target=make_muestra, args=([p[0] for p in pipes],))
    generador_p.start()
    
    tipos=["frecuencia", "presion", "oxigeno"]
    analizadores=[]
    for i,tipo in enumerate(tipos):
        p=multiprocessing.Process(target=make_math, args=(pipes[i][1],tipo,queue))
        p.start()
        analizadores.append(p)
    verificador_p=multiprocessing.Process(target=validar, args=(queue,queue_resultados_validados))
    verificador_p.start()
    procesos = [generador_p] + analizadores + [verificador_p]

    try:
        generador_p.join()
        for p in analizadores:
            p.join()
        verificador_p.join()
    except KeyboardInterrupt:
        print("Ctrl+C detectado. Terminando todos los procesos hijos...")
        for p in procesos:
            if p.is_alive():
                p.terminate()
        for p in procesos:
            p.join()
        sys.exit(1)

    bloques=queue_resultados_validados.get()
    queue.close()
    queue_resultados_validados.close()

    return bloques

if __name__ == "__main__":
    
    bloques=main()
    for bloque in bloques:
        guardar_bloque(bloque)
#
    
    
    
