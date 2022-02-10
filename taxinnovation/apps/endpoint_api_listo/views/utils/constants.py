import os
import json


NOM_PROYECTO = ""
ARBOL_MENSAJERIA = {}
DATOS_CONN_PG = {}

# Obtenemos el nombre del proyecto de la cuenta de servicio
with open(os.environ['GOOGLE_APPLICATION_CREDENTIALS']) as llave:
    NOM_PROYECTO = "projects/" + json.load(llave)['project_id']
# Cargamos el arbol de mensajería (Topic, Target y Action)
# Cargamos los datos para conectar a cloudsql
with open(os.getcwd() + '/resources/keys/datos_conn_pg.json') as arch:
    DATOS_CONN_PG = json.load(arch)
