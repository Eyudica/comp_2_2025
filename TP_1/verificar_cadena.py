from hashlib import sha256
import json
#Abre el archivo .json
def open_file():
    with open("blockchain.json") as f:
       
        return json.load(f)
def check_total_blocks():
    with open("blockchain.json") as f:
        data = json.load(f)
        return len(data)
#Recalcula el hash y se fija que sean iguales que el del archivo json
def validar(data):
    cadenas_corruptas=0
    hashes_corruptos=[]
    for posicion,lista_blockchain in enumerate(data):
        current_hash=lista_blockchain['hash']
        prev_hash = lista_blockchain['prev_hash']
        datos = lista_blockchain['datos']
        timestamp = lista_blockchain['timestamp']
        
        # Convertir los datos a string con json.dumps
        datos_str = json.dumps(datos, sort_keys=True)
        bloque_raw = prev_hash + datos_str + timestamp
        hash_recalculado = sha256(bloque_raw.encode("utf-8")).hexdigest()
        if current_hash!=hash_recalculado:
            cadenas_corruptas+=1
            hashes_corruptos.append(f"Cadena corrupta: {current_hash} no es igual a {hash_recalculado} en el bloque {posicion+1}")
    return hashes_corruptos
#Calcula la media y desviacion total de cada tipo
def calcular_totales(cadena,tipo):
    media_valores=[]
    desviacion_valores=[]
    for lista_blockchain in cadena:
        media_valores.append(lista_blockchain["datos"][tipo]["media"])
        desviacion_valores.append(lista_blockchain["datos"][tipo]["desviacion"])
    
    media=round(sum(media_valores)/len(media_valores),2)
    desviacion=round(sum(desviacion_valores)/len(desviacion_valores),2)
    return media,desviacion #primero la media y despues la desviacion

if __name__ == "__main__":
    
    cadena = open_file()
    corruptos=validar(cadena)
    len_data=check_total_blocks()
    #Arma el archivo .txt y muestra que bloques estan corruptos si es que hubieron
    with open("resultados.txt","w") as f:
        if len(corruptos)==0:
            f.write(f"No hubo bloques corruptos de {len_data} analizados\n")
        else:
            f.write(f"Hubieron un total de {len(corruptos)} bloques corruptos de {len_data} analizados\n")
            for cadena_corrupta in corruptos:
                f.write(cadena_corrupta+"\n")
            
        for tipo in ["frecuencia","presion","oxigeno"]:
            valores_finales=calcular_totales(cadena,tipo)
            f.write("-"*40+"\n")

            f.write(f"Media total de {tipo}: {valores_finales[0]}\n")
            f.write(f"Desviacion total de {tipo}: {valores_finales[1]}\n")
    print("Programa finalizado")