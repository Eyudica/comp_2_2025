import os,re

def main():
    p1_to_p2_r, p1_to_p2_w = os.pipe()
    p2_to_p1_r, p2_to_p1_w = os.pipe()
    pid = os.fork()
    if pid > 0:
        os.close(p1_to_p2_r)
        msg=input("Escribe una operacion para P2: ")\
        
        if re.search(r"[A-Za-z]", msg): # como para sanitizar el input, con re.fulsearch __import__('os').listdir('.') si funciona
        
            print("Deja de probar hackearme")
        else:
            os.write(p1_to_p2_w, str(msg).encode())
            os.close(p1_to_p2_w)
            os.close(p2_to_p1_r)
            os.wait()
            
    else:
        os.close(p1_to_p2_w)
        os.close(p2_to_p1_r)
        message = os.read(p1_to_p2_r, 100).decode()
        os.close(p1_to_p2_r)
        try:
            evaluacion=eval(message) ###### No deberia usar eval por su riesgo
            
            print(evaluacion)
        except:
            print("No se pudo evaluar el mensaje")


main()
        

