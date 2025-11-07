import socket
import json
import argparse
import re

def get_urls():
    urls = []
    print("Introduce las URLs a analizar (una por línea, enter para terminar):")
    while True:
        url = input()
        if not url:
            break
        if re.search(r"https?://(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)", url):
            urls.append(url)
        else:
            print(f"URL inválida: {url}")
    return urls

def main(ip, port):
    urls = get_urls()
    if not urls:
        print("No se ingresaron URLs.")
        return

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((ip, port))
            print(f"Conectado al servidor en {ip}:{port}")

            s.sendall(json.dumps(urls).encode('utf-8'))

            buffer = ""
            while True:
                data = s.recv(4096)
                if not data:
                    break
                buffer += data.decode('utf-8')
                
                while "\n" in buffer:
                    message_str, buffer = buffer.split('\n', 1)
                    if message_str:
                        try:
                            message = json.loads(message_str)
                            if isinstance(message, dict) and message.get("status") == "DONE":
                                print("\nAnálisis completado.")
                                return
                            
                            print(json.dumps(message, indent=2))

                        except json.JSONDecodeError:
                            print(f"Error decodificando JSON: {message_str}")

        except ConnectionRefusedError:
            print(f"Error: No se pudo conectar al servidor en {ip}:{port}. ¿Está corriendo?")
        except Exception as e:
            print(f"Ocurrió un error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cliente para el servidor de análisis web.")
    parser.add_argument("--ip", required=True, help="Dirección IP del servidor")
    parser.add_argument("--port", type=int, required=True, help="Puerto del servidor")
    args = parser.parse_args()
    
    main(args.ip, args.port)
