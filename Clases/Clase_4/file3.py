import os,random
def main():
    p1_r, p1_w = os.pipe()
    p2_r,p2_w=os.pipe()
    pid = os.fork()

    if pid > 0:  # Padre (P1)
        os.close(p1_r)  # No lee
        number = random.randint(0, 100)
        os.write(p1_w, str(number).encode())
        os.close(p1_w)  # Cerrás escritura
        print("P1 envía el número:", number)
        os.wait()

    else:  # Hijo (P2)
        os.close(p1_w)  # No escribe
        response = os.read(p1_r, 10).decode()
        os.close(p1_r)  # Cerrás lectura
        print("P2 recibe el número:", response)
        if int(response) % 2 == 0:
            os.write(p2_w, str(response).encode())
            os.close(p2_w)  # Cerrás escritura
            print("P2 envía el número:", response)
        else:
            os.write(p2_w, str(0).encode())
            os.close(p2_w)  # Cerrás escritura
            print("P2 envía el número por ser impar:", 0)
        pid2=os.fork()
        if pid2==0:
            response = os.read(p2_r, 10).decode()
            os.close(p2_r)  # Cerrás lectura
            print("P3 recibe el número:", response)
            print(f"P3 realiza la potencia",response*2)
        
######Pid


if __name__ == "__main__":
    main()