
import datetime
import random
import multiprocessing
import json
import math
import time
import os
from hashlib import sha256
PAQUETES = 60

def generar_muestra():
    return {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "frecuencia": random.randint(60,180),
        "presion": [random.randint(110,180), random.randint(70,110)],
        "oxigeno": random.randint(90,100)
    }

def make_math(conn,clave,queue):
    valores=[]
    media=0
    desviacion=0
    

    for _ in range(PAQUETES):
        try:
            data = conn.recv()
            valor=data.get(clave)
            if isinstance(valor,list):
                promedio=round(sum(valor)/len(valor),2) #por el tema de la presion
                valores.append(promedio)
            else:
                valores.append(valor)
        except EOFError:
            break    
    media=round(sum(valores)/PAQUETES,2)

    desviacion=round(math.sqrt(sum((valor-media)**2 for valor in valores) /PAQUETES),2) 
    resultado= {
        "tipo":clave,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "media": media,
        "desviacion": desviacion
    }
    queue.put(resultado)

def make_muestra(conn):
    for _ in range(PAQUETES):
        conn.send(generar_muestra())
       # time.sleep(1)

def validar(queue):
    resultados={}
    while not queue.empty():
        dato=queue.get()
        resultados[dato['tipo']]=dato
    timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    alerta=False
    frecuencia = resultados['frecuencia']['media']
    oxigeno = resultados['oxigeno']['media']
    presion = resultados['presion']['media']
    if frecuencia > 200 or oxigeno < 90 or presion > 200:
        alerta=True

    datos_str = f"frecuencia:{frecuencia},oxigeno:{oxigeno},presion:{presion}"
    prev_hash = sha256(datos_str.encode('utf-8')).hexdigest() 
        
    bloque = prev_hash + datos_str + timestamp
    current_hash = sha256(bloque.encode('utf-8')).hexdigest()

    return {
        "timestamp": timestamp,
        "datos": {
            "frecuencia": frecuencia,
            "presion": presion,
            "oxigeno": oxigeno
        },
        "alerta": alerta,
        "prev_hash": prev_hash,
        "hash": current_hash
    }
def iniciar_procesos(tipo,queue):
    parent_conn, child_conn = multiprocessing.Pipe()
    send = multiprocessing.Process(target=make_muestra, args=(parent_conn,))
    send.start()
    send.join()
    receptor = multiprocessing.Process(target=make_math, args=(child_conn,tipo,queue))
    receptor.start()
    receptor.join()

def guardar_resultados(resultados, archivo="resultados.json"):
    with open(archivo, "w") as f:
        json.dump(resultados, f, indent=4)

def main():
    queue=multiprocessing.Queue() #funciona como fifo

    for tipo in ["frecuencia", "presion", "oxigeno"]:
        iniciar_procesos(tipo,queue)
    resultados_validacion=validar(queue)
    guardar_resultados(resultados_validacion)
if __name__ == "__main__":
    main()
   # receptor_presion.join()
  #  receptor_oxigeno.join()
    
    
    
