#from urllib import response
import pandas as pd
import numpy as np
import json
from urllib import request
import requests

token = '45230497b3db99fb5690da68634bb1d467bac951d590c8e5a66828d6b6500914'
url ='https://www.banxico.org.mx/SieAPIRest/service/v1/series/SF43718/datos/oportuno'
headers = {'Bmx-Token':token}
response = requests.get(url, headers=headers)
datos_crudos = response.json()
print(datos_crudos['bmx']['series'][0]['datos'][0]['dato'])


#respuesta = request.urlopen(url)
#contenido = respuesta.read()
#json_obtenido = json.loads(contenido.decode('uft-8'))
#print(json_obtenido)


