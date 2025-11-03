import argparse
if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser = argparse.ArgumentParser(description="Servidor de Procesamiento Distribuido")
    parser.add_argument("--ip","-ip",required=True,help="Direccion de escucha")
    parser.add_argument("--port","-p",required=True,type=int,help="Puerto de escucha")
    parser.add_argument("--processes","-n",required=True,type=int,help="Numero de procesos en el pool (default: CPU count)")

    args=parser.parse_args()