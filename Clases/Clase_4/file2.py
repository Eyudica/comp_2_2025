import os

def main():
    padre_a_hijo_r, padre_a_hijo_w = os.pipe()
    hijo_a_padre_r, hijo_a_padre_w = os.pipe()

    pid = os.fork()

    if pid > 0:  # PADRE
        os.close(padre_a_hijo_r)
        os.close(hijo_a_padre_w)

        archivo=open("file.txt","r").read().splitlines()
        for linea in archivo:
            os.write(padre_a_hijo_w, (linea+'\n ').encode())

        os.close(padre_a_hijo_w)
        
        # respuesta = os.read(hijo_a_padre_r, 1024)
        # print("PADRE: Recibi del hijo ->", respuesta)
        # print(respuesta.decode())
        # os.close(hijo_a_padre_r)
    else:  # HIJO
        os.close(padre_a_hijo_w)
        os.close(hijo_a_padre_r)                    
        respuesta = os.read(padre_a_hijo_r, 1024)
        texto=respuesta.decode()
        lineas=texto.split('\n')
        letras_lista=[]
        for i in lineas:
            letras=len(i.replace(' ',''))
            print(letras) 
            letras_lista.append(letras)
        os.close(padre_a_hijo_r)
        os.close(hijo_a_padre_w)
if __name__ == '__main__':

    main()