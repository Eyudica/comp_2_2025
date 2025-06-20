import random,argparse,time
parser = argparse.ArgumentParser("Menu de argumentos")
parser.add_argument("-n","--numero",required=True,help="Numero de secuencia",type=int,default=10)

args = parser.parse_args()

def numbers():
    for i in range(args.numero):
        numbers=random.randint(1,args.numero)
        print(numbers)

numbers()