import requests
from bs4 import BeautifulSoup
from PIL import Image, UnidentifiedImageError
from io import BytesIO
import os
import time
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import multiprocessing
import json
import shutil
import base64
import socket
import argparse
import signal
import sys

import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def analizar_rendimiento(url, q):
    try:
        inicio = time.time()
        response = requests.get(url, timeout=30)
        response.raise_for_status()  # Lanza una excepción para códigos de error HTTP (4xx o 5xx)
        duracion = time.time() - inicio

        soup = BeautifulSoup(response.text, "html.parser")

        recursos = []
        for tag in soup.find_all(["img", "script", "link"]):
            src = tag.get("src") or tag.get("href")
            if src:
                recursos.append(urljoin(url, src))

        total_size = 0
        for r in recursos:
            try:
                resp = requests.head(r, timeout=5)
                size = int(resp.headers.get("Content-Length", 0))
                total_size += size
            except:
                pass  # Ignora recursos individuales que fallen

        q.put(("rendimiento", {
            "url": url,
            "tiempo_carga_seg": round(duracion, 2),
            "total_recursos": len(recursos),
            "tamaño_total_kb": round(total_size / 1024, 2)
        }))
    except requests.RequestException as e:
        q.put(("rendimiento", {"url": url, "error": f"No se pudo acceder a la URL: {e}"}))




def analizar_imagenes(url, q, carpeta_destino="imagenes", max_imagenes=5):
    try:
        webpage = url.replace("https://", "").replace("http://", "").replace("www.", "")
        webpage = webpage.replace("/", "_").replace("\\", "_").replace(":", "_").replace("?", "_").replace("@", "_")

        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")

        driver = webdriver.Chrome(options=options)
        driver.get(url)
        time.sleep(5)
        html = driver.page_source
        driver.quit()

        soup = BeautifulSoup(html, "html.parser")
        imagenes = [urljoin(url, img.get("src")) for img in soup.find_all("img") if img.get("src")]
        imagenes = imagenes[:max_imagenes]

        thumbnails_base64 = []

        for idx, img_url in enumerate(imagenes, start=1):
            try:
                img_data = requests.get(img_url, timeout=10).content
                img = Image.open(BytesIO(img_data))

                if img.mode in ("RGBA", "LA"):
                    img = img.convert("RGB")

                extension = img.format.lower() if img.format else "jpg"
                if extension not in ["jpg", "jpeg", "png", "webp"]:
                    extension = "jpg"

                nombre = f"imagen_{idx}_{webpage}.{extension}"
                ruta = os.path.join(carpeta_destino, nombre)
                img.save(ruta)

                thumbnail = img.copy()
                thumbnail.thumbnail((150, 150))
                thumb_path = os.path.join(carpeta_destino, f"thumb_{idx}_{webpage}.{extension}")
                thumbnail.save(thumb_path, optimize=True, quality=70)

                with open(thumb_path, "rb") as f:
                    thumb_base64 = base64.b64encode(f.read()).decode("utf-8")
                    thumbnails_base64.append(thumb_base64)

            except (UnidentifiedImageError, OSError, requests.RequestException) as e:
                print(f"Error procesando imagen {img_url}: {e}")

        q.put((
            "imagenes",
            {
                "url": url,
                "processing_data": {
                    "thumbnails": thumbnails_base64
                },
                "status": "success"
            }
        ))
    except Exception as e:
        q.put(("imagenes", {"url": url, "error": f"No se pudo procesar la URL para imágenes: {e}"}))


def take_screenshot(url, q):
    try:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")

        driver = webdriver.Chrome(options=options)
        driver.get(url)

        scroll_height = driver.execute_script("return document.body.scrollHeight")
        driver.set_window_size(1920, scroll_height)
        directorio="imagenes"
        nombre = f"screenshot_{url.replace('https://', '').replace('http://', '').replace('/', '_')}.png"
        driver.save_screenshot(os.path.join(directorio,nombre))
        driver.quit()
        print(f"Captura guardada como {nombre} en imagenes/")
        q.put(("screenshot", {"url": url, "status": "success"}))
    except Exception as e:
        q.put(("screenshot", {"url": url, "error": f"No se pudo tomar la captura: {e}"}))



def ejecutar_tarea(args):
    funcion, *params = args
    return funcion(*params)

def handler(signum, frame):
    print("Saliendo del servidor...")
    sys.exit(0)


def main(ip, port, processes):
    signal.signal(signal.SIGINT, handler)
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((ip, port))
        s.listen()
        print(f"Servidor escuchando en {ip}:{port}")

        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Conectado con {addr}")
                while True:
                    data = conn.recv(4096)
                    if not data:
                        break

                    urls = json.loads(data.decode())
                    
                    if len(urls)==0:
                        conn.send((json.dumps({"status": "No hay URLs para analizar"}) + "\n").encode())
                        break
                    conn.send((json.dumps({"status": "Realizando scrapping..."}) + "\n").encode())
                    print(f"URLs recibidas: {urls}")
                    manager = multiprocessing.Manager()
                    q = manager.Queue()
                    tareas = []

                    for url in urls:
                        tareas.extend([
                            (analizar_rendimiento, url, q),
                            (analizar_imagenes, url, q),
                            (take_screenshot, url, q)
                        ])

                    with multiprocessing.Pool(processes=processes) as pool:
                        pool.map(ejecutar_tarea, tareas)

                    resultados = {}
                    while not q.empty():
                        tipo, data = q.get()
                        url = data.get("url")
                        
                        if url not in resultados:
                            resultados[url] = {}
                        
                        resultados[url][tipo] = data

                    conn.send((json.dumps(resultados) + "\n").encode())
                    conn.send((json.dumps({"status": "DONE"}) + "\n").encode())
                    print("Datos enviados al cliente\n")
            conn.close()
            print("Conexión cerrada, esperando una nueva...")




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Servidor de Procesamiento Distribuido")
    parser.add_argument("--ip", "-ip", required=True, help="Direccion de escucha")
    parser.add_argument("--port", "-p", required=True, type=int, help="Puerto de escucha")
    parser.add_argument("--processes", "-n", required=False,default=multiprocessing.cpu_count() ,type=int, help="Numero de procesos del pool")
    args = parser.parse_args()

    main(args.ip, args.port, args.processes)