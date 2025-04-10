import os

def main():
    p1_to_p2_r, p1_to_p2_w = os.pipe()
    p2_to_p1_r, p2_to_p1_w = os.pipe()
    pid = os.fork()
    if pid > 0:
        os.close(p1_to_p2_r)
        msg=input("Escribe un mensaje para P2: ")
        os.write(p1_to_p2_w, msg.encode())
        response = os.read(p2_to_p1_r, 100).decode()
        os.close(p1_to_p2_w)
        print(f"P1 recibe el mensaje: {response}")
        os.close(p2_to_p1_r)
        os.wait()
    else:
        os.close(p1_to_p2_w)
        os.close(p2_to_p1_r)
        message = os.read(p1_to_p2_r, 100).decode()
        os.close(p1_to_p2_r)
        print(f"P2 recibe el mensaje: {message}")
        continuar=input("continuar?(s/n)")
 
        if continuar=="s":
            msg2=input("Escribe un mensaje para P1: ")
            os.write(p2_to_p1_w, msg2.encode())
            os.close(p2_to_p1_w)

main()
        

