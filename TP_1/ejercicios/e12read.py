import argparse,sys
parser = argparse.ArgumentParser("Menu de argumentos")
parser.add_argument("-m","--min",required=True,help="",type=int)
args=parser.parse_args()
def reader(min):
    for line in sys.stdin:
        if int(line)>min:
            print(line.strip())
    
reader(args.min)

