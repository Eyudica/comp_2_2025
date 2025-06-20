import sys
import argparse,os
parser=argparse.ArgumentParser(description="Ejercicio 1")
parser.add_argument("--num",required=True,help="Cantidad de procesos hijos a crear")
parser.add_argument("--verbose",required=False,action="store_true",help="Mostrar informacion extra")


args=parser.parse_args()


def make_child(num):
    for i in range(num):
        pid=os.fork()
        if pid==0:
            if args.verbose:
                print("Hijo",i)
                sys.exit()
        else:
            print("Padre",i)
    for i in range(num):
        os.wait()
        print("Hijo",i,"terminado")
make_child(int(args.num))