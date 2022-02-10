import os
import json

NOM_PROYECTO = None
LLAVE_MAESTRA = None

# Obtenemos el nombre del proyecto de la cuenta de servicio
with open(os.environ['GOOGLE_APPLICATION_CREDENTIALS']) as llave:
    NOM_PROYECTO = "projects/" + json.load(llave)['project_id']

with open(os.getcwd() + '/resources/keys/api_listomx_auth_str.json') as arch:
    LLAVE_MAESTRA = json.load(arch)

with open(os.getcwd() + '/resources/keys/datos_conn_pg.json') as arch:
    DATOS_CONN_PG = json.load(arch)