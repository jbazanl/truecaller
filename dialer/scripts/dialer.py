#!/usr/bin/env python
import requests
import csv
from datetime import datetime, timedelta
import itertools
import time
import sys

# detalles de autenticación para ARI
ari_client = "http://104.243.32.219:8088/ari"
username = "itelvox"
password = "rt6Fh61D9iMs"

def hacer_llamada(row, timeout=15):
    numero = row[0].split(';')[0]
    print(numero)
    # definir los detalles del canal a usar
    endpoint = ari_client + "/channels"
    data = {
        "endpoint": "PJSIP/10002{}@dgtk".format(numero_destino),
        "extension": numero_destino,
        "context": "interno",
        'callerId': numero,
        "priority": 1
    }
    
    # enviar solicitud POST para iniciar la llamada
    r = requests.post(endpoint, auth=(username, password), json=data)
    print(f"Llamada a {numero_destino} iniciada con respuesta {r.status_code}")
    
    # esperar por la respuesta
    response = None
    for i in range(timeout):
        endpoint = ari_client + "/channels"
        r = requests.get(endpoint, auth=(username, password))
   
        channels = r.json()
        print(channels)
        for channel in channels:
            if channel["state"] == "Ringing":
                endpoint = ari_client + f"/channels/{channel['id']}"
                print(endpoint)
                requests.delete(endpoint, auth=(username, password))
                print(f"Llamada a {numero} colgada.")
                response = channel
                break
        if response is not None:
            break
        time.sleep(1)
    
    # si no se obtiene respuesta, colgar la llamada
    if response is None:
        endpoint = ari_client + f"/channels/{r.json()['id']}"
        requests.delete(endpoint, auth=(username, password))
        print(f"Llamada a {numero} no respondida, se ha colgado la llamada.")
        return
    
    # imprimir información del canal respondido
    print(f"Llamada a {numero_destino} de origen {numero} respondida por canal {response['id']}.")
    
numero_destino = '51999999999'
if len(sys.argv) >= 2:
    file_name = sys.argv[1]
    numero_destino = sys.argv[2]

# iterar por la lista de números y hacer una llamada por cada uno
file_404 = '/spark/filebrowser/reports/truecaller/' + file_name
with open(file_404, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    # skip the header row if present
    next(csvreader, None)
    for row in csvreader:
        hacer_llamada(row)
