import os

def main():
    padre_a_hijo_r, padre_a_hijo_w = os.pipe()
    hijo_a_padre_r, hijo_a_padre_w = os.pipe()

    pid = os.fork()

    if pid > 0:  # PADRE
        os.close(padre_a_hijo_r)
        os.close(hijo_a_padre_w)

        mensaje = b"Mensaje del padre al hijo"
        print("PADRE: Enviando mensaje al hijo...")
        os.write(padre_a_hijo_w, mensaje)
        os.close(padre_a_hijo_w)

        respuesta = os.read(hijo_a_padre_r, 100)
        print("PADRE: Recibi del hijo ->", respuesta.decode())
        os.close(hijo_a_padre_r)

    else:  # HIJO
        os.close(padre_a_hijo_w)
        os.close(hijo_a_padre_r)

        mensaje = os.read(padre_a_hijo_r, 100)
        print("HIJO: Recibi del padre ->", mensaje.decode())
        
        print("HIJO: Enviando eco al padre...")
        os.write(hijo_a_padre_w, mensaje)

        os.close(padre_a_hijo_r)
        os.close(hijo_a_padre_w)


if __name__ == '__main__':
    main()
