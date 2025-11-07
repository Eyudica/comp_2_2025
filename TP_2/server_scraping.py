from bs4 import BeautifulSoup
import argparse
import socket
import json
import re
import aiohttp
import asyncio
import sys

# --- Funciones de Análisis de Scraping (sin cambios) ---

async def analizar_url(url, sem):
    async with sem:
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=30)) as session:
                async with session.get(url) as response:
                    html = await response.text()
                    soup = BeautifulSoup(html, "html.parser")
                    page_data = extract_page_data(soup)
                    print(f"Análisis de scraping para {url} completado.")
                    return page_data
        except Exception as e:
            print(f"Error en scraping de {url}: {e}")
            return {"error": str(e)}

async def analizar_urls_concurrente(urls, workers):
    sem = asyncio.Semaphore(workers)
    tasks = [analizar_url(url, sem) for url in urls]
    results = await asyncio.gather(*tasks)
    return results

def get_title(soup):
    return soup.title.text if soup.title else "No title found"

def get_links(soup):
    return list(set(a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith('http')))

def meta_description(soup):
    tag = soup.find("meta", attrs={"name": "description"})
    return tag["content"] if tag else "No meta description found"

def meta_keywords(soup):
    tag = soup.find("meta", attrs={"name": "keywords"})
    return tag["content"] if tag else "No meta keywords found"

def open_graph(soup):
    return {tag.get("property"): tag.get("content", "") for tag in soup.find_all("meta", property=re.compile(r'^og:'))}

def count_images(soup):
    return len(soup.find_all('img'))

def count_headers(soup):
    return {f'h{i}': len(soup.find_all(f'h{i}')) for i in range(1, 7)}

def extract_page_data(soup):
    return {
        'title': get_title(soup),
        'links': get_links(soup),
        'meta_description': meta_description(soup),
        'meta_keywords': meta_keywords(soup),
        'open_graph': open_graph(soup),
        'images_count': count_images(soup),
        'headers_count': count_headers(soup)
    }

# --- Nueva Función para contactar a server_processing ---

def contact_processing_server(urls, processing_ip, processing_port):
    """Se conecta a server_processing, envía URLs y recibe los resultados."""
    print(f"Contactando a server_processing en {processing_ip}:{processing_port}...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((processing_ip, processing_port))
            s.sendall(json.dumps(urls).encode())

            buffer = ""
            results = None
            while True:
                data = s.recv(4096)
                if not data:
                    break
                buffer += data.decode('utf-8')
                while "\n" in buffer:
                    message_str, buffer = buffer.split('\n', 1)
                    if not message_str:
                        continue
                    
                    try:
                        message = json.loads(message_str)
                        if isinstance(message, dict) and message.get("status") == "DONE":
                            print("Transmisión de server_processing completada.")
                            return results or {"error": "No se recibieron resultados antes de DONE."}
                        else:
                            # Asumimos que este es el objeto principal de resultados
                            results = message
                            print("Datos de resultados recibidos de server_processing.")
                    except json.JSONDecodeError:
                        print(f"Mensaje no-JSON de server_processing ignorado: {message_str}")

            return results or {"error": "La conexión cerró antes de recibir DONE."}
            
        except ConnectionRefusedError:
            print(f"Error: No se pudo conectar a server_processing. ¿Está corriendo?")
        except Exception as e:
            print(f"Error contactando a server_processing: {e}")
    return {"error": "No se pudo obtener respuesta de server_processing."}


# --- Nuevo Servidor Principal (Gateway) ---

def main(ip, port, workers):
    # Dirección del servidor de procesamiento ahora está fija
    PROC_IP = "127.0.0.1"
    PROC_PORT = 8081

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((ip, port))
        s.listen()
        print(f"Servidor Gateway escuchando en {ip}:{port}")

        while True:
            print("\nEsperando nueva conexión de cliente...")
            conn, addr = s.accept()
            with conn:
                print(f"Conectado con cliente {addr}")
                try:
                    data = conn.recv(4096)
                    if not data:
                        continue

                    urls = json.loads(data.decode())
                    print(f"URLs recibidas de cliente: {urls}")

                    # 1. Obtener datos de scraping (asíncrono)
                    scraping_results = asyncio.run(analizar_urls_concurrente(urls, workers))
                    scraping_dict = {url: res for url, res in zip(urls, scraping_results) if res}

                    # 2. Obtener datos de procesamiento del otro servidor
                    processing_results = contact_processing_server(urls, PROC_IP, PROC_PORT)
                    
                    # 3. Combinar resultados
                    final_results = {}
                    for url in urls:
                        final_results[url] = {
                            "scraping_data": scraping_dict.get(url, {"error": "Sin datos"}),
                            "processing_data": processing_results.get(url, {"error": "Sin datos"})
                        }

                    # 4. Enviar resultado final al cliente
                    conn.sendall((json.dumps(final_results) + "\n").encode())
                    conn.sendall(json.dumps({"status": "DONE"}).encode())
                    print("Datos combinados enviados al cliente.")

                except (json.JSONDecodeError, ConnectionResetError) as e:
                    print(f"Error con el cliente {addr}: {e}. La conexión se cerrará.")
                except Exception as e:
                    print(f"Ocurrió un error inesperado con el cliente {addr}: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Servidor Gateway: Orquesta scraping y procesamiento.")
    parser.add_argument("--ip", required=True, help="Dirección IP para escuchar (ej: 127.0.0.1)")
    parser.add_argument("--port", type=int, required=True, help="Puerto para escuchar (ej: 8080)")
    parser.add_argument("--workers", type=int, default=4, help="Número de workers para scraping concurrente")
    args = parser.parse_args()

    main(args.ip, args.port, args.workers)
