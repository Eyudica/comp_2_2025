
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
from tqdm import tqdm
PAQUETES = 60
#Genera una muestra aleatoria
def generar_muestra():
    return {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "frecuencia": random.randint(60,180),
        "presion": random.randint(110,180),# random.randint(70,110)],
        "oxigeno": random.randint(90,100)
    }
#Calcula la media y desviacion de cada tipo de dato, enviando los resultados al queue para el proceso verificador
def make_math(conn,clave,queue):

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

        
#Genera las 60 muestras y las envia al pipe que esta conectado cada proceso que haga los calculos
#de la media y de la desviacion (make_math).Muestra una barra de progreso a medida que se generan las muestras
def make_muestra(conns):
   # print("Generando muestras.Espera 60 segundos")
    for _ in tqdm(range(PAQUETES),desc="Generando muestras"):
        muestra=generar_muestra()
        for conn in conns:
            conn.send(muestra)
        time.sleep(1)
#Tiene un queue de entrada para recibir las muestras y un queue de salida para enviar los bloques analizados
def validar(queue_entrada,queue_salida):

    bloques = []
    bloques_por_timestamp = {}
    prev_hash = "00000000000000000000000000000000000000000000000000000000000000000"
    bloques_procesados = 0
    #Esto se va a ejecutar en este caso 60 veces
    while bloques_procesados < PAQUETES:
        resultado = queue_entrada.get()
        ts = resultado["timestamp"]
        #Por timestamp guarda los datos en el diccionario
        #si el timestamp es nuevo crea una nueva entrada en el diccioniario
        if ts not in bloques_por_timestamp:
            bloques_por_timestamp[ts] = {}
        bloques_por_timestamp[ts][resultado["tipo"]] = resultado
        #Si estan los 3 tipos de datos arma el bloque
        if len(bloques_por_timestamp[ts]) == 3:
            datos = bloques_por_timestamp[ts]
            #Calcula si hay alerta o no
            alerta = (
                datos["frecuencia"]["media"] > 200 or
                (90>=datos["oxigeno"]["media"] >=100 )or
                datos["presion"]["media"] > 200
            )
            #Arma los datos en formato json
            datos_str = json.dumps({
                "frecuencia": datos["frecuencia"],
                "presion": datos["presion"],
                "oxigeno": datos["oxigeno"]
            }, sort_keys=True)
            #Calcula el hash de la cadena
            bloque_raw = prev_hash + datos_str + ts
            current_hash = sha256(bloque_raw.encode("utf-8")).hexdigest()
            #Arma el bloque para meterlo en la lista que despues se va a enviar al queue de salida
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

#Sirve para escribir los bloques en el archivo .json y que si existe no lo sobreescriba
def guardar_bloque(bloque, archivo="blockchain.json"):
    if os.path.exists(archivo):
        with open(archivo, "r") as f:
            cadena = json.load(f)
    else:
        cadena = []

    cadena.append(bloque)

    with open(archivo, "w") as f:
        json.dump(cadena, f, indent=4)

#Inicia los procesos y sus respectivos pipes
def iniciar_procesos(tipo,queue):
    parent_conn, child_conn = multiprocessing.Pipe()
    send = multiprocessing.Process(target=make_muestra, args=(parent_conn,))
    send.start()
    send.join()
    receptor = multiprocessing.Process(target=make_math, args=(child_conn,tipo,queue))
    receptor.start()
    receptor.join()
#Para atrapar el ctrl+c
def handler(sig,frame):
    os._exit(1)

def main():
    #para que los hijos no hereden el handler
    if multiprocessing.current_process().name=="MainProcess":
        signal.signal(signal.SIGINT, handler)
    #crealos pipes para  los procesos
    pipes=[]
    for _ in range(3):
        pipes.append(multiprocessing.Pipe())
    queue=multiprocessing.Queue()
    queue_resultados_validados=multiprocessing.Queue()
    #Genera las muestras y los envia a cada pipe
    generador_p=multiprocessing.Process(target=make_muestra, args=([p[0] for p in pipes],),daemon=True)
    generador_p.start()
    
    tipos=["frecuencia", "presion", "oxigeno"]
    analizadores=[]
    #Lanza los 3 procesos y  le pasa el pipe hijo al  proceso hijo
    for i,tipo in enumerate(tipos):
        p=multiprocessing.Process(target=make_math, args=(pipes[i][1],tipo,queue),daemon=True)
        p.start()
        analizadores.append(p)#--> se usa analizadores para guardar los procesos  hijos
    verificador_p=multiprocessing.Process(target=validar, args=(queue,queue_resultados_validados),daemon=True)
    verificador_p.start()
    procesos = [generador_p] + analizadores + [verificador_p]

    try:
        generador_p.join()
        #espera a que terminen los hijos
        for p in analizadores:
            p.join()
        verificador_p.join()
    #para que si el usuario hace  ctrl+c corte todo y que no queden hijos huerfanos
    except KeyboardInterrupt:
        print("Ctrl+C detectado. Terminando todos los procesos hijos...")
        for p in procesos:
            if p.is_alive():
                p.terminate()
        for p in procesos:
            p.join()
        sys.exit(1)
    #Obtiene los bloques del queue de salida
    bloques=queue_resultados_validados.get()
    #Cierra los  queues
    queue.close()
    queue_resultados_validados.close()

    return bloques

if __name__ == "__main__":
    
    bloques=main()
    for bloque in bloques:
        guardar_bloque(bloque)
#
    
    
    
