#! /usr/bin/env python

import requests
import csv
from datetime import datetime, timedelta
import itertools
import time
import sys


def process_row(row):
    numero_origen = row[0].split(';')[0]
    print(numero_origen)
    url = 'http://104.243.32.219:8088/ari/channels'
    headers = {'Content-Type': 'application/json'}
    auth = ('itelvox', 'rt6Fh61D9iMs')
    data = {
        'endpoint': 'PJSIP/10002' + numero_destino + '@dgtk',
        'extension': '10002' + numero_destino,
        'context': 'interno',
        'priority': '1',
        'ring_timeout': '5',
        'callerId': numero_origen
    }
    response = requests.post(url, headers=headers, auth=auth, json=data)
    print(response.text)
    if response.status_code == 200:
        channel_id = response.json()['id']
        print('Llamada saliente creada con ID: {}'.format(channel_id))
    else:
        print('Error al crear la llamada saliente: {}'.format(response.status_code))
    time.sleep(1)


today = datetime.now()
id_fecha = datetime.strftime(today, '%Y%m%d')
#id_fecha = "20230218"
print(id_fecha)

numero_destino = '51983434724'
if len(sys.argv) >= 2:
    file_name = sys.argv[1]
    numero_destino = sys.argv[2]

#file_404 = '/spark/filebrowser/reports/truecaller/portavox_%s.csv' % id_fecha
file_404 = '/spark/filebrowser/reports/truecaller/' + file_name
with open(file_404, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    # skip the header row if present
    next(csvreader, None)
    limited_reader = itertools.islice(csvreader, 5)
    # iterate over the remaining rows and execute the function for each row
    #for row in limited_reader:
    for row in csvreader:
        process_row(row)
