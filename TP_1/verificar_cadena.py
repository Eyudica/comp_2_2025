from hashlib import sha256
import json

def open_file():
    with open("blockchain.json") as f:
       
        return json.load(f)
def validar(data):
    #prev_hash="00000000000000000000000000000000000000000000000000000000000000000"
    cadenas_corruptas=0
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
            print(f"Cadena corrupta: {current_hash} no es igual a {hash_recalculado} en el bloque {posicion+1}")
    print("Validacion finalizada")
    return cadenas_corruptas
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
    with open("resultados.txt","w") as f:
        if corruptos==0:
            f.write("No hubo bloques corruptos de 60 analizados\n")
        else:
            f.write(f"Hubieron un total de {corruptos} bloques corruptos de 60 analizados\n")
        for tipo in ["frecuencia","presion","oxigeno"]:
            valores_finales=calcular_totales(cadena,tipo)
            f.write("-"*40+"\n")

            f.write(f"Media total de {tipo}: {valores_finales[0]}\n")
            f.write(f"Desviacion total de {tipo}: {valores_finales[1]}\n")
    print("Programa finalizado")