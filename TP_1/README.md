# TP_1 Emanuel Yudica

## Descripción

El tp esta compuesto por 2 archivos:

1. generador.py
2. verificar_cadena.py

### Generador.py

Este archivo se encarga de generar 60 simulaciones de 60 muestras de datos aleatorios, cada una con su respectivo hash.

 Esta compuesto del proceso principal (generador) que esta conectados con pipes a 3 procesos hijos para calcular la media y desviacion de cada tipo de dato.

 Cada proceso hijo se encarga de calcular la media y desviacion de cada tipo de dato enviando los resultados a un queue que conecta con el proceso verificador calculando el hash de cada muestra en base al timestamp, al hash previo y a los datos de cada simulacion.Finalmente almacenando el bloque en el archivo blockchain.json.

### Verificar_cadena.py

Este archivo se encarga de verificar que los datos de cada simulación sean iguales a los que se encuentran en el archivo blockchain.json.
Finalmente se calcula la media y desviacion de cada tipo de dato, exportando todos los resultados en un archivo resultados.txt.

## Ejecución

Para ejecutar el programa es necesario tener instalado python 3.7 en el sistema.

Para ejecutar el programa se debe correr el siguiente comando desde la carpeta donde se encuentra el archivo generador.py:

```bash
python generador.py
```

Una vez que se ejecuta el programa se debe correr el siguiente comando desde la carpeta donde se encuentra el archivo verificar_cadena.py:

```bash
python verificar_cadena.py
```

Finalmente se debe correr el siguiente comando desde la carpeta donde se encuentra el archivo resultados.txt:

```bash
cat resultados.txt
```

## Resultados

Los resultados se encuentran en el archivo resultados.txt

