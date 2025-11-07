## Emanuel Yudica

### Instalacion de dependencias
```bash
pip install -r requirements.txt
```
# Uso de la aplicación


### Cliente

```bash
python cliente.py --ip 127.0.0.1 --port 8080
```

### Servidor de procesamiento

```bash
python server_processing.py --ip 127.0.0.1 --port 8081 --processes 4
```

### Servidor de scrapping

```bash
python server_scraping.py --ip 127.0.0.1 --port 8080 --workers 4
```

